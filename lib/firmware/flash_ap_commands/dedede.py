# -*- coding: utf-8 -*-
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""DeDeDe specific functions to get flash commands"""

from __future__ import print_function


def is_fast_required(use_futility, servo_version):
  """Returns true if --fast is necessary to flash successfully.

  The configurations in this function consistently fail on the verify step,
  adding --fast removes verification of the flash and allows these configs to
  flash properly. Meant to be a temporary hack until b/143240576 is fixed.

  Args:
    use_futility (bool): True if futility is to be used, False if
      flashrom.
    servo_version (str): The type name of the servo device being used.

  Returns:
    bool: True if fast is necessary, False otherwise.
  """
  # Does nothing but return false and get rid of the warning for unused
  # argument.
  del use_futility, servo_version
  return False


def get_commands(servo_version, serial):
  """Get specific flash commands for octopus

  Each board needs specific commands including the voltage for Vref, to turn
  on and turn off the SPI flash. The get_*_commands() functions provide a
  board-specific set of commands for these tasks. The voltage for this board
  needs to be set to 3.3 V.

  Args:
    servo_version (string): specifies what type of servo connects the
      host to the dut
    serial (string): serial number of the servo device connected to the
      dut used in formatting commands

  Returns:
    array: [dut_control_on, dut_control_off, flashrom_cmd, futility_cmd]
      dut_control*=2d arrays formmated like [["cmd1", "arg1", "arg2"],
                                             ["cmd2", "arg3", "arg4"]]
                   where cmd1 will be run before cmd2
      flashrom_cmd=command to flash via flashrom
      futility_cmd=command to flash via futility
  """
  dut_control_on = []
  dut_control_off = []
  if servo_version == 'c2d2':
    dut_control_on.append(['ap_flash_select:on'])
    dut_control_on.append(['spi2_vref:pp3300'])
    dut_control_off.append(['spi2_vref:off'])
    dut_control_off.append(['ap_flash_select:off'])
    programmer = 'raiden_debug_spi:serial=%s' % serial
  elif (servo_version == 'ccd_cr50' or
        servo_version == 'servo_v4_with_ccd_cr50'):
    programmer = 'raiden_debug_spi:target=AP,serial=%s ' % serial
  else:
    raise Exception('%s not recognized' % servo_version)

  flashrom_cmd = ['sudo', 'flashrom', '-p', programmer, '-w']
  futility_cmd = ['sudo', 'futility', 'update', '-p', programmer, '-i']

  return [dut_control_on, dut_control_off, flashrom_cmd, futility_cmd]
