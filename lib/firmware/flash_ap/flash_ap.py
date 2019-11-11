#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module to detect flashing infrastructure and flash ap firmware.

This script automatically detects the flashing infrastructure and uses that to
flash AP fw to the DUT. First it checks for the environment variable $IP, then
tries flash via ssh to that address if one is present. If not it looks up what
servo version is connected and uses that to flash the AP firmware. Right now
this script only works with octopus, grunt, wilco, and hatch devices but will
be extended to support more in the future.
"""

from __future__ import print_function
import argparse
import importlib
import os
import subprocess
import sys
import tempfile
from chromite.lib import cros_logging as logging


def dut_control_value(dut_ctrl_out):
  """Helper function to return meaningful part of dut-control command output

  Args:
    dut_ctrl_out (string): output from dut-control command
  Returns:
    string: substring of output from ':' to the end with any whitespace
      removed
  """

  return dut_ctrl_out[dut_ctrl_out.find(':') + 1:].strip()


def build_ssh_cmds(futility, ip, path, tmp_file_name, fast, verbose):
  """Helper function to build commands for flashing over ssh

  Args:
    futility (bool): if True then flash with futility, otherwise flash
      with flashrom.
    ip (string): ip address of dut to flash.
    path (string): path to BIOS image to be flashed.
    tmp_file_name (string): name of tempfile with copy of testing_rsa
      keys.
    fast (bool): if True pass through --fast (-n for flashrom) to
      flashing command.
    verbose (bool): if True set -v flag in flash command.
  Returns:
    scp_cmd ([string]):
    flash_cmd ([string]):
  """
  ssh_parameters = ['-o', 'UserKnownHostsFile=/dev/null',
                    '-o', 'StrictHostKeyChecking=no',
                    '-o', 'CheckHostIP=no']
  tmp = '/tmp'
  hostname = 'root@%s' % ip
  scp_cmd = (['scp', '-i', tmp_file_name] + ssh_parameters +
             [path, '%s:%s' % (hostname, tmp)])
  flash_cmd = ['ssh', hostname, '-i', tmp_file_name] + ssh_parameters
  if futility:
    flash_cmd += ['futility', 'update', '-p', 'host', '-i',
                  os.path.join(tmp, os.path.basename(path))]
    if fast:
      flash_cmd += ['--fast']
    if verbose:
      flash_cmd += ['-v']
  else:
    flash_cmd += ['flashrom', '-p', 'host', '-w',
                  os.path.join(tmp, os.path.basename(path))]
    if fast:
      flash_cmd += ['-n']
    if verbose:
      flash_cmd += ['-V']
  flash_cmd += ['&& reboot']
  return scp_cmd, flash_cmd


def ssh_flash(futility, path, verbose, ip, fast):
  """This function flashes AP firmware over ssh.

  Tries to ssh to ip address once. If the ssh connection is successful the
  file to be flashed is copied over to the DUT then flashed using either
  futility or flashrom.

  Args:
    futility (bool): if True then flash with futility, otherwise flash
      with flashrom.
    path (str): path to the BIOS image to be flashed.
    verbose (bool): if True to set -v flag in flash command and
      print other debug info, if False do nothing.
    ip (str): ip address of dut to flash.
    fast (bool): if True pass through --fast (-n for flashrom) to
      flashing command.
  Returns:
    bool: True on success, False on fail
  """
  logging.info('connecting to: %s\n', ip)
  id_filename = '/mnt/host/source/chromite/ssh_keys/testing_rsa'
  tmpfile = tempfile.NamedTemporaryFile()
  copy_cmd = ['cp', id_filename, tmpfile.name]
  try:
    subprocess.run(copy_cmd, check=True)
  except subprocess.CalledProcessError as e:
    logging.error('ERROR: copying failed with message:\n%s', e.output)
  scp_cmd, flash_cmd = build_ssh_cmds(futility, ip, path, tmpfile.name, fast,
                                      verbose)
  try:
    subprocess.run(scp_cmd, check=True)
  except subprocess.CalledProcessError:
    logging.error('ERROR: Could not copy image to dut.')
    return False
  logging.info('Flashing now, may take several minutes.')
  try:
    subprocess.run(flash_cmd, check=True)
  except subprocess.CalledProcessError as e:
    logging.error('ERROR: flashing failed with output:\n%s', e.output)
    return False
  return True


def flash(dut_cmd_on, dut_cmd_off, flash_cmd):
  """Runs subprocesses for setting dut controls and flashing the AP fw.

  Args:
    dut_cmd_on ([[str]]): 2d array of dut-control commands
      in the form [['dut-control', 'cmd1', 'cmd2'...],
      ['dut-control', 'cmd3'...]]
      that get executed before the flashing.
    dut_cmd_off ([[str]]): 2d array of dut-control commands
      in the same form that get executed after flashing.
    flash_cmd ([str]): array containing all arguments for
      the flash command.
  Returns:
    bool: True if flash was successful, otherwise False.
  """
  try:
    for cmd in dut_cmd_on:
      subprocess.run(cmd, check=True)
    subprocess.run(flash_cmd, check=True)
    for cmd in dut_cmd_off:
      subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    logging.error('ERROR: flashing failed with output:\n%s', e.output)
    return False
  return True


def get_servo_info(dut_control):
  """Get version and serialname of connected servo.

  This function returns the current version of the
  servo device connected to the host and the serialname
  of that device, throws error if no device or the
  device is not supported.

  Args:
    dut_control ([str]): either just ['dut-control']
      or ['dut-control', '--port=$PORT'] if the
      port being used is not 9999.
  Returns:
    serial (str): serial number of servo device
      listening on the specified port.
    servo_version (str): name of servo version
      being used.
  """
  out = ''
  try:
    out = subprocess.check_output(dut_control + ['servo_type'],
                                  encoding='utf-8')
  except subprocess.CalledProcessError:
    logging.error('ERROR: Could not establish servo connection. Verify servod '
                  'is running in background and servo is connected properly. '
                  'Exiting flash ap.')
    return -1, 'null'
  servo_version = dut_control_value(out)
  # Get the serial number.
  sn_ctl = 'serialname'
  if servo_version == 'servo_v4_with_servo_micro':
    sn_ctl = 'servo_micro_serialname'
  elif servo_version == 'servo_v4_with_ccd_cr50':
    sn_ctl = 'ccd_serialname'
  elif not (servo_version == 'servo_v2'
            or servo_version == 'ccd_cr50'
            or servo_version == 'servo_micro'):
    raise ValueError('Servo version: %s not recognized' % servo_version,
                     'verify connection and port number')
  serial_out = subprocess.check_output(dut_control + [sn_ctl],
                                       encoding='utf-8')
  serial = dut_control_value(serial_out)
  return serial, servo_version


def get_parser():
  """Helper function to get parser with all arguments added

  Args:
    None
  Returns:
    argparse.ArgumentParser: object used to check command line arguments
  """
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('board', type=str, help='board name')
  parser.add_argument('image', type=str, help='/path/to/BIOS_image.bin')
  parser.add_argument('-v', '--verbose', help='increase output verbosity',
                      action='store_true')
  parser.add_argument('--port', type=int, action='store',
                      default=os.getenv('SERVO_PORT', 9999),
                      help='number of the port being listened to by servo '
                      'device (defaults to $SERVO_PORT or 9999 if is not '
                      'present)')
  parser.add_argument('--flashrom', action='store_true',
                      help='use flashrom to flash instead of futility')
  parser.add_argument('--fast', action='store_true',
                      help='speed up flashing by not validating flash')
  return parser


def main(argv):
  """Main function for flashing ap firmware.

  Detects flashing infrastructure then fetches commands from get_*_commands
  and flashes accordingly.
  """
  parser = get_parser()
  opts = parser.parse_args(argv)
  if not os.path.exists(opts.image):
    logging.error('ERROR: %s does not exist, verify the path of your build and '
                  'try again', opts.image)
    return 1
  ip = os.getenv('IP')
  module_name = 'get_%s_commands' % opts.board
  try:
    module = importlib.import_module(module_name)
  except ImportError:
    logging.error('ERROR: %s not valid or supported. Please verify board name'
                  ' and try again ', opts.board)
    return 1

  if ip is not None:
    logging.info('Attempting to flash via ssh.')
    # TODO(b/143241417): Can't use flashrom over ssh on wilco.
    if (hasattr(module, 'use_futility_ssh') and module.use_futility_ssh and
        opts.flashrom):
      logging.warning('WARNING: flashing with flashrom over ssh on this device'
                      ' fails consistently, flashing with futility instead.')
      opts.flashrom = False
    if ssh_flash(not opts.flashrom, opts.image, opts.verbose, ip, opts.fast):
      logging.info('ssh flash successful. Exiting flash_ap')
      return 0
    logging.info('ssh failed, attempting to flash via servo connection.')
  # Dut_ctrl string specifies the port if it is not 9999
  dut_ctrl = ['dut-control']
  if opts.port != 9999:
    dut_ctrl.append('--port=%d' % opts.port)
  serial_num, servo_ver = get_servo_info(dut_ctrl)
  if serial_num == -1:
    # Error message was printed in get_servo_info but the script needs to exit
    return 1
  # TODO(b/143240576): Fast mode is sometimes necessary to flash successfully.
  if module.is_fast_required(not opts.flashrom, servo_ver) and not opts.fast:
    logging.warning('WARNING: there is a known error with the board and servo '
                    'type being used, enabling --fast to bypass this problem.')
    opts.fast = True
  dut_on, dut_off, flashrom_cmd, futility_cmd = module.get_commands(servo_ver,
                                                                    serial_num)
  dut_ctrl_on = [dut_ctrl + x for x in dut_on]
  dut_ctrl_off = [dut_ctrl + x for x in dut_off]
  flashrom_cmd += [opts.image]
  futility_cmd += [opts.image]
  futility_cmd += ['--force', '--wp=0']
  if opts.fast:
    futility_cmd += ['--fast']
    flashrom_cmd += ['-n']
  if opts.verbose:
    flashrom_cmd += ['-V']
    futility_cmd += ['-v']
  if not opts.flashrom:
    if flash(dut_ctrl_on, dut_ctrl_off, futility_cmd):
      logging.info('SUCCESS. Exiting flash_ap.')
    else:
      logging.error('ERROR: unable to complete flash, verify servo connection '
                    'is correct and servod is running in the background.')
  else:
    if flash(dut_ctrl_on, dut_ctrl_off, flashrom_cmd):
      logging.info('SUCCESS. Exiting flash_ap.')
    else:
      logging.error('ERROR: unable to complete flash, verify servo connection '
                    'is correct and servod is running in the background.')
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))