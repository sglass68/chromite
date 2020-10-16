# -*- coding: utf-8 -*-
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the auto_updater_tranfer module.

The main parts of unittest include:
  1. test transfer methods in LocalTransfer.
  5. test retrials in LocalTransfer.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import os

import mock
import six

from chromite.lib import auto_updater_transfer
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import osutils
from chromite.lib import partial_mock
from chromite.lib import remote_access


_DEFAULT_ARGS = {
    'payload_dir': None, 'device_payload_dir': None, 'tempdir': None,
    'payload_name': None, 'cmd_kwargs': None,
}


# pylint: disable=protected-access


class CrOSLocalTransferPrivateMock(partial_mock.PartialCmdMock):
  """Mock out all transfer functions in auto_updater_transfer.LocalTransfer."""
  TARGET = 'chromite.lib.auto_updater_transfer.LocalTransfer'
  ATTRS = ('_TransferStatefulUpdate', '_TransferRootfsUpdate',
           '_TransferUpdateUtilsPackage', '_EnsureDeviceDirectory')

  def __init__(self):
    partial_mock.PartialCmdMock.__init__(self)

  def _TransferStatefulUpdate(self, _inst, *_args, **_kwargs):
    """Mock auto_updater_transfer.LocalTransfer._TransferStatefulUpdate."""

  def _TransferRootfsUpdate(self, _inst, *_args, **_kwargs):
    """Mock auto_updater_transfer.LocalTransfer._TransferRootfsUpdate."""

  def _TransferUpdateUtilsPackage(self, _inst, *_args, **_kwargs):
    """Mock auto_updater_transfer.LocalTransfer._TransferUpdateUtilsPackage."""

  def _EnsureDeviceDirectory(self, _inst, *_args, **_kwargs):
    """Mock auto_updater_transfer.LocalTransfer._EnsureDeviceDirectory."""


class CrosTransferBaseClassTest(cros_test_lib.MockTestCase):
  """Test whether Transfer's public transfer functions are retried correctly."""

  def CreateInstance(self, device, **kwargs):
    """Create auto_updater_transfer.LocalTransfer instance.

    Args:
      device: a remote_access.ChromiumOSDeviceHandler object.
      kwargs: contains parameter name and value pairs for any argument accepted
        by auto_updater_transfer.LocalTransfer. The values provided through
        kwargs will supersede the defaults set within this function.

    Returns:
      An instance of auto_updater_transfer.LocalTransfer.
    """
    default_args = copy.deepcopy(_DEFAULT_ARGS)

    default_args.update(kwargs)
    return auto_updater_transfer.LocalTransfer(device=device, **default_args)

  def testErrorTriggerRetryTransferUpdateUtils(self):
    """Test if _TransferUpdateUtilsPackage() is retried properly."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      self.PatchObject(auto_updater_transfer, '_DELAY_SEC_FOR_RETRY', 1)
      _MAX_RETRY = self.PatchObject(auto_updater_transfer, '_MAX_RETRY', 1)
      transfer_update_utils = self.PatchObject(
          auto_updater_transfer.LocalTransfer,
          '_TransferUpdateUtilsPackage',
          side_effect=cros_build_lib.RunCommandError('fail'))
      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer.TransferUpdateUtilsPackage)
      self.assertEqual(transfer_update_utils.call_count, _MAX_RETRY + 1)

  def testErrorTriggerRetryTransferStateful(self):
    """Test if _TransferStatefulUpdate() is retried properly."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      self.PatchObject(auto_updater_transfer, '_DELAY_SEC_FOR_RETRY', 1)
      _MAX_RETRY = self.PatchObject(auto_updater_transfer, '_MAX_RETRY', 2)
      transfer_stateful = self.PatchObject(
          auto_updater_transfer.LocalTransfer,
          '_TransferStatefulUpdate',
          side_effect=cros_build_lib.RunCommandError('fail'))
      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer.TransferStatefulUpdate)
      self.assertEqual(transfer_stateful.call_count, _MAX_RETRY + 1)

  def testErrorTriggerRetryTransferRootfs(self):
    """Test if _TransferRootfsUpdate() is retried properly."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      self.PatchObject(auto_updater_transfer, '_DELAY_SEC_FOR_RETRY', 1)
      _MAX_RETRY = self.PatchObject(auto_updater_transfer, '_MAX_RETRY', 3)
      transfer_rootfs = self.PatchObject(
          auto_updater_transfer.LocalTransfer,
          '_TransferRootfsUpdate',
          side_effect=cros_build_lib.RunCommandError('fail'))
      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer.TransferRootfsUpdate)
      self.assertEqual(transfer_rootfs.call_count, _MAX_RETRY + 1)


class CrosLocalTransferTest(cros_test_lib.MockTempDirTestCase):
  """Test whether LocalTransfer's transfer functions are retried."""

  def CreateInstance(self, device, **kwargs):
    """Create auto_updater_transfer.LocalTransfer instance.

    Args:
      device: a remote_access.ChromiumOSDeviceHandler object.
      kwargs: contains parameter name and value pairs for any argument accepted
        by auto_updater_transfer.LocalTransfer. The values provided through
        kwargs will supersede the defaults set within this function.

    Returns:
      An instance of auto_updater_transfer.LocalTransfer.
    """
    default_args = copy.deepcopy(_DEFAULT_ARGS)

    default_args.update(kwargs)
    return auto_updater_transfer.LocalTransfer(device=device, **default_args)

  def setUp(self):
    """Mock remote_access.RemoteDevice's functions for update."""
    self.PatchObject(remote_access.RemoteDevice, 'work_dir', '/test/work/dir')
    self.PatchObject(remote_access.RemoteDevice, 'CopyToWorkDir')
    self.PatchObject(remote_access.RemoteDevice, 'CopyToDevice')
    self._transfer_class = auto_updater_transfer.LocalTransfer

  def testTransferStatefulUpdateNeedsTransfer(self):
    """Test transfer functions for stateful update.

    Test whether _EnsureDeviceDirectory() are being called correctly.
    """
    self.PatchObject(self._transfer_class,
                     '_EnsureDeviceDirectory')
    self.PatchObject(auto_updater_transfer, 'STATEFUL_FILENAME',
                     'test_stateful.tgz')
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, cmd_kwargs={'test': 'args'}, payload_dir='/test/payload/dir')
      transfer._TransferStatefulUpdate()
      self.assertFalse(self._transfer_class._EnsureDeviceDirectory.called)

  def testCheckPayloadsError(self):
    """Test CheckPayloads() with raising exception.

    auto_updater_transfer.ChromiumOSTransferError is raised if it does not find
    payloads in its path.
    """
    self.PatchObject(os.path, 'exists', return_value=False)
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='does_not_exist',
          payload_dir='/test/payload/dir')
      self.assertRaises(
          auto_updater_transfer.ChromiumOSTransferError,
          transfer.CheckPayloads)

  def testCheckPayloads(self):
    """Test CheckPayloads() without raising exception.

    Test will fail if ChromiumOSTransferError is raised when payload exists.
    """
    self.PatchObject(os.path, 'exists', return_value=True)
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='exists', payload_dir='/test/payload/dir')
      transfer.CheckPayloads()

  def testGetPayloadProps(self):
    """Tests GetPayloadProps().

    Tests GetPayloadProps() when payload_name is in the
    format payloads/chromeos_xxxx.0.0_<blah>.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_dir=self.tempdir,
          payload_name='payloads/chromeos_12345.100.0_board_stable_'
                       'full_v4-1a3e3fd5a2005948ce8e605b66c96b2f.bin')
      self.PatchObject(os.path, 'getsize', return_value=100)
      expected = {'image_version': '12345.100.0', 'size': 100}
      self.assertDictEqual(transfer.GetPayloadProps(),
                           expected)

  def testGetPayloadPropsError(self):
    """Tests error thrown by GetPayloadProps().

    Test error thrown when payload_name is not in the expected format of
    payloads/chromeos_xxxx.0.0_<blah> or called update.gz.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_dir=self.tempdir, payload_name='wrong_format')
      self.PatchObject(os.path, 'getsize')
      self.assertRaises(ValueError, transfer.GetPayloadProps)

  def testGetPayloadPropsDefaultFilename(self):
    """Tests GetPayloadProps().

    Tests GetPayloadProps() when payload_name is named
    update.gz.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_dir=self.tempdir, payload_name='update.gz')
      self.PatchObject(os.path, 'getsize', return_value=101)
      expected = {'image_version': '99999.0.0', 'size': 101}
      self.assertDictEqual(transfer.GetPayloadProps(), expected)

class CrosLabEndToEndPayloadTransferTest(cros_test_lib.MockTempDirTestCase):
  """Test all methods in auto_updater_transfer.LabEndToEndPayloadTransfer."""

  def CreateInstance(self, device, **kwargs):
    """Create auto_updater_transfer.LabEndToEndPayloadTransfer instance.

    Args:
      device: a remote_access.ChromiumOSDeviceHandler object.
      kwargs: contains parameter name and value pairs for any argument accepted
        by auto_updater_transfer.LabEndToEndPayloadTransfer. The values provided
        through kwargs will supersede the defaults set within this function.

    Returns:
      An instance of auto_updater_transfer.LabEndToEndPayloadTransfer.
    """
    default_args = copy.deepcopy(_DEFAULT_ARGS)
    default_args['staging_server'] = 'http://0.0.0.0:8000'

    default_args.update(kwargs)
    return auto_updater_transfer.LabEndToEndPayloadTransfer(device=device,
                                                            **default_args)


  def setUp(self):
    """Mock remote_access.RemoteDevice/ChromiumOSDevice functions for update."""
    self.PatchObject(remote_access.RemoteDevice, 'work_dir', '/test/work/dir')
    self._transfer_class = auto_updater_transfer.LabEndToEndPayloadTransfer

  def testTransferUpdateUtilsCurlCalls(self):
    """Test methods calls of _TransferUpdateUtilsPackage().

    Test whether _GetCurlCmdForPayloadDownload() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected = [{'payload_dir': os.path.join(device.work_dir, 'src'),
                   'payload_filename': 'nebraska.py'}]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(self._transfer_class, '_GetCurlCmdForPayloadDownload')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')

      transfer._TransferUpdateUtilsPackage()
      self.assertListEqual(
          self._transfer_class._GetCurlCmdForPayloadDownload.call_args_list,
          [mock.call(**x) for x in expected])

  def testTransferUpdateUtilsRunCmdCalls(self):
    """Test methods calls of _TransferUpdateUtilsPackage().

    Test whether remote_access.ChromiumOSDevice.run() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      self._transfer_class = auto_updater_transfer.LabEndToEndPayloadTransfer
      expected = [['curl', '-o', '/test/work/dir/src/nebraska.py',
                   'http://0.0.0.0:8000/static/nebraska.py']]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')

      transfer._TransferUpdateUtilsPackage()
      self.assertListEqual(
          remote_access.ChromiumOSDevice.run.call_args_list,
          [mock.call(x) for x in expected])

  def testTransferUpdateUtilsEnsureDirCalls(self):
    """Test methods calls of _TransferUpdateUtilsPackage().

    Test whether _EnsureDeviceDirectory() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected = [os.path.join(device.work_dir, 'src'), device.work_dir]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')

      transfer._TransferUpdateUtilsPackage()
      self.assertListEqual(
          self._transfer_class._EnsureDeviceDirectory.call_args_list,
          [mock.call(x) for x in expected])

  def testErrorTransferUpdateUtilsServerError(self):
    """Test errors thrown by _TransferUpdateUtilsPackage()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, staging_server='http://wrong:server')
      self.PatchObject(self._transfer_class,
                       '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run',
                       side_effect=cros_build_lib.RunCommandError('fail'))
      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer._TransferUpdateUtilsPackage)

  def testErrorTransferStatefulServerError(self):
    """Test errors thrown by _TransferStatefulUpdate()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, staging_server='http://wrong:server')
      self.PatchObject(self._transfer_class,
                       '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run',
                       side_effect=cros_build_lib.RunCommandError('fail'))
      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer._TransferStatefulUpdate)

  def testTransferStatefulCurlCmdCalls(self):
    """Test methods calls of _TransferStatefulUpdate().

    Test whether _GetCurlCmdForPayloadDownload() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, device_payload_dir='/test/device/payload/dir',
          payload_dir='/test/payload/dir')

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(self._transfer_class, '_GetCurlCmdForPayloadDownload')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')
      expected = [
          {'payload_dir': device.work_dir,
           'payload_filename': 'stateful.tgz',
           'build_id': '/test/payload/dir'}]

      transfer._TransferStatefulUpdate()
      self.assertListEqual(
          self._transfer_class._GetCurlCmdForPayloadDownload.call_args_list,
          [mock.call(**x) for x in expected])

  def testTransferStatefulRunCmdCalls(self):
    """Test methods calls of _TransferStatefulUpdate().

    Test whether remote_access.ChromiumOSDevice.run() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected = [
          ['curl', '-o', '/test/work/dir/stateful.tgz',
           'http://0.0.0.0:8000/static/stateful.tgz']]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')

      transfer._TransferStatefulUpdate()
      self.assertListEqual(
          remote_access.ChromiumOSDevice.run.call_args_list,
          [mock.call(x) for x in expected])

  def testTransferStatefulEnsureDirCalls(self):
    """Test methods calls of _TransferStatefulUpdate().

    Test whether _EnsureDeviceDirectory() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, device_payload_dir='/test/device/payload/dir')
      expected = [transfer._device_payload_dir]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')

      transfer._TransferStatefulUpdate()
      self.assertListEqual(
          self._transfer_class._EnsureDeviceDirectory.call_args_list,
          [mock.call(x) for x in expected])

  def testErrorTransferRootfsServerError(self):
    """Test errors thrown by _TransferRootfsUpdate()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, staging_server='http://wrong:server',
          device_payload_dir='/test/device/payload/dir',
          payload_name='test_update.gz')
      self.PatchObject(self._transfer_class,
                       '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run',
                       side_effect=cros_build_lib.RunCommandError('fail'))
      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer._TransferRootfsUpdate)

  def testTransferRootfsCurlCmdCalls(self):
    """Test method calls of _TransferRootfsUpdate().

    Test whether _GetCurlCmdForPayloadDownload() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, device_payload_dir='/test/device/payload/dir',
          payload_dir='test/payload/dir', payload_name='test_update.gz',
          cmd_kwargs={'test': 'args'})
      expected = [
          {'payload_dir': transfer._device_payload_dir,
           'payload_filename': transfer._payload_name,
           'build_id': transfer._payload_dir}]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(self._transfer_class, '_GetCurlCmdForPayloadDownload')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')
      self.PatchObject(remote_access.ChromiumOSDevice, 'CopyToWorkDir')

      transfer._TransferRootfsUpdate()

      self.assertListEqual(
          self._transfer_class._GetCurlCmdForPayloadDownload.call_args_list,
          [mock.call(**x) for x in expected])

  def testTransferRootfsRunCmdCalls(self):
    """Test method calls of _TransferRootfsUpdate().

    Test whether remote_access.ChromiumOSDevice.run() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          device_payload_dir='/test/device/payload/dir',
          cmd_kwargs={'test': 'args'})
      expected = [['curl', '-o', '/test/device/payload/dir/test_update.gz',
                   'http://0.0.0.0:8000/static/test_update.gz']]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')
      self.PatchObject(remote_access.ChromiumOSDevice, 'CopyToWorkDir')

      transfer._TransferRootfsUpdate()
      self.assertListEqual(
          remote_access.ChromiumOSDevice.run.call_args_list,
          [mock.call(x) for x in expected])

  def testTransferRootfsRunCmdPayloadProps(self):
    """Test method calls of _TransferRootfsUpdate().

    Test whether remote_access.ChromiumOSDevice.run() is being called
    the correct number of times with the correct arguments when
    LocalPayloadPropsFile() is set to a valid local filepath.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          device_payload_dir='/test/device/payload/dir',
          cmd_kwargs={'test': 'args'})

      self.PatchObject(os.path, 'isfile', return_value=True)
      transfer.LocalPayloadPropsFile = '/existent/test.gz.json'
      expected = [
          ['curl', '-o', '/test/device/payload/dir/test_update.gz',
           'http://0.0.0.0:8000/static/test_update.gz']]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')
      self.PatchObject(remote_access.ChromiumOSDevice, 'CopyToWorkDir')

      transfer._TransferRootfsUpdate()
      self.assertListEqual(
          remote_access.ChromiumOSDevice.run.call_args_list,
          [mock.call(x) for x in expected])

  def testTransferRootfsEnsureDirCalls(self):
    """Test method calls of _TransferRootfsUpdate().

    Test whether _EnsureDeviceDirectory() is being called
    the correct number of times with the correct arguments.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, device_payload_dir='/test/device/payload/dir',
          payload_name='test_update.gz', cmd_kwargs={'test': 'args'})
      expected = [transfer._device_payload_dir]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')
      self.PatchObject(remote_access.ChromiumOSDevice, 'CopyToWorkDir')

      transfer._TransferRootfsUpdate()
      self.assertListEqual(
          self._transfer_class._EnsureDeviceDirectory.call_args_list,
          [mock.call(x) for x in expected])

  def testTransferRootfsCopyToWorkdirLocalPayloadProps(self):
    """Test method calls of _TransferRootfsUpdate().

    Test whether device.CopyToWorkDir() is being called
    the correct number of times with the correct arguments when
    LocalPayloadPropsFile() is set to a valid local filepath.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, cmd_kwargs={'test': 'test'},
          device_payload_dir='/test/device/payload/dir',
          payload_name='test_update.gz')

      transfer._local_payload_props_path = '/existent/test.gz.json'
      expected = [{'src': transfer._local_payload_props_path,
                   'dest': transfer.PAYLOAD_DIR_NAME,
                   'mode': transfer._payload_mode,
                   'log_output': True, 'test': 'test'}]

      self.PatchObject(self._transfer_class, '_EnsureDeviceDirectory')
      self.PatchObject(remote_access.ChromiumOSDevice, 'run')
      self.PatchObject(remote_access.ChromiumOSDevice, 'CopyToWorkDir')

      transfer._TransferRootfsUpdate()
      self.assertListEqual(
          remote_access.ChromiumOSDevice.CopyToWorkDir.call_args_list,
          [mock.call(**x) for x in expected])

  def testGetCurlCmdStandard(self):
    """Test _GetCurlCmdForPayloadDownload().

    Tests the typical usage of the _GetCurlCmdForPayloadDownload() method.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected_cmd = ['curl', '-o',
                      '/tmp/test_payload_dir/payload_filename.ext',
                      'http://0.0.0.0:8000/static/stable-channel/board/'
                      '12345.0.0/payloads/payload_filename.ext']
      cmd = transfer._GetCurlCmdForPayloadDownload(
          payload_dir='/tmp/test_payload_dir',
          payload_filename='payloads/payload_filename.ext',
          build_id='stable-channel/board/12345.0.0')
      self.assertEqual(cmd, expected_cmd)

  def testGetCurlCmdNoImageName(self):
    """Test _GetCurlCmdForPayloadDownload().

    Tests when the payload file is available in the static directory on the
    staging server.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected_cmd = ['curl', '-o',
                      '/tmp/test_payload_dir/payload_filename.ext',
                      'http://0.0.0.0:8000/static/payload_filename.ext']
      cmd = transfer._GetCurlCmdForPayloadDownload(
          payload_dir='/tmp/test_payload_dir',
          payload_filename='payload_filename.ext')
      self.assertEqual(cmd, expected_cmd)

  def testCheckPayloadsAllIn(self):
    """Test CheckPayloads().

    Test CheckPayloads() method when transfer_rootfs_update and
    transfer_stateful_update are both set to True.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='board-release/12345.6.7')
      self.PatchObject(auto_updater_transfer, 'STATEFUL_FILENAME',
                       'test_stateful.tgz')
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall')

      expected = [
          ['curl', '-I', 'http://0.0.0.0:8000/static/board-release/12345.6.7/'
                         'test_update.gz', '--fail'],
          ['curl', '-I', 'http://0.0.0.0:8000/static/board-release/12345.6.7/'
                         'test_update.gz.json', '--fail'],
          ['curl', '-I', 'http://0.0.0.0:8000/static/board-release/12345.6.7/'
                         'test_stateful.tgz', '--fail']]

      transfer.CheckPayloads()
      self.assertListEqual(
          self._transfer_class._RemoteDevserverCall.call_args_list,
          [mock.call(x) for x in expected])

  def testCheckPayloadsAllInRemoteDevserverCallError(self):
    """Test CheckPayloads().

    Test the exception thrown by CheckPayloads() method when
    transfer_rootfs_update and transfer_stateful_update are both set to True and
    _RemoteDevserver() throws an error.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='board-release/12345.6.7')

      self.PatchObject(auto_updater_transfer, 'STATEFUL_FILENAME',
                       'test_stateful.tgz')
      self.PatchObject(self._transfer_class,
                       '_RemoteDevserverCall',
                       side_effect=cros_build_lib.RunCommandError(msg=''))

      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer.CheckPayloads)

  def testCheckPayloadsNoStatefulTransfer(self):
    """Test CheckPayloads().

    Test CheckPayloads() method when transfer_rootfs_update is True and
    transfer_stateful_update is set to False.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='board-release/12345.6.7',
          transfer_stateful_update=False)

      self.PatchObject(self._transfer_class, '_RemoteDevserverCall')

      expected = [['curl', '-I', 'http://0.0.0.0:8000/static/board-release/'
                                 '12345.6.7/test_update.gz', '--fail'],
                  ['curl', '-I', 'http://0.0.0.0:8000/static/board-release/'
                                 '12345.6.7/test_update.gz.json', '--fail']]

      transfer.CheckPayloads()
      self.assertListEqual(
          self._transfer_class._RemoteDevserverCall.call_args_list,
          [mock.call(x) for x in expected])

  def testCheckPayloadsNoStatefulTransferRemoteDevserverCallError(self):
    """Test CheckPayloads().

    Test the exception thrown by CheckPayloads() method when
    transfer_rootfs_update is True and transfer_stateful_update is False
    and Lab_RemoteDevserver() throws an error.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='board-release/12345.6.7',
          transfer_stateful_update=False)
      self.PatchObject(self._transfer_class,
                       '_RemoteDevserverCall',
                       side_effect=cros_build_lib.RunCommandError(msg=''))

      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer.CheckPayloads)

  def testCheckPayloadsNoRootfsTransfer(self):
    """Test CheckPayloads.

    Test CheckPayloads() method when transfer_rootfs_update is False and
    transfer_stateful_update is set to True.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_dir='board-release/12345.6.7',
          transfer_rootfs_update=False)
      self.PatchObject(auto_updater_transfer, 'STATEFUL_FILENAME',
                       'test_stateful.tgz')
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall')

      expected = [['curl', '-I', 'http://0.0.0.0:8000/static/board-release/'
                                 '12345.6.7/test_stateful.tgz', '--fail']]
      transfer.CheckPayloads()
      self.assertListEqual(
          self._transfer_class._RemoteDevserverCall.call_args_list,
          [mock.call(x) for x in expected])

  def testCheckPayloadsNoRootfsTransferRemoteDevserverCallError(self):
    """Test CheckPayloads().

    Test exception thrown by CheckPayloads() method when
    transfer_rootfs_update is False and transfer_stateful_update is set to True
    and _RemoteDevserver() throws an error.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_dir='board-release/12345.6.7',
          transfer_rootfs_update=False)
      self.PatchObject(auto_updater_transfer, 'STATEFUL_FILENAME',
                       'test_stateful.tgz')
      self.PatchObject(self._transfer_class,
                       '_RemoteDevserverCall',
                       side_effect=cros_build_lib.RunCommandError(msg=''))

      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer.CheckPayloads)

  def testCheckPayloadsNoPayloadError(self):
    """Test auto_updater_transfer.CheckPayloads.

    Test CheckPayloads() for exceptions raised when payloads are not available
    on the staging server.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)

      self.PatchObject(self._transfer_class,
                       '_RemoteDevserverCall',
                       side_effect=cros_build_lib.RunCommandError(msg=''))

      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer.CheckPayloads)

  def testGetPayloadUrlStandard(self):
    """Test auto_updater_transfer._GetStagedUrl.

    Tests the typical usage of the _GetStagedUrl() method.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected_url = ('http://0.0.0.0:8000/static/board-release/12345.0.0/'
                      'payload_filename.ext')
      url = transfer._GetStagedUrl(
          staged_filename='payload_filename.ext',
          build_id='board-release/12345.0.0/')
      self.assertEqual(url, expected_url)

  def testGetPayloadUrlNoImageName(self):
    """Test auto_updater_transfer._GetStagedUrl.

    Tests when the build_id parameter is defaulted to None.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)
      expected_url = 'http://0.0.0.0:8000/static/payload_filename.ext'
      url = transfer._GetStagedUrl(
          staged_filename='payload_filename.ext')
      self.assertEqual(url, expected_url)

  def testGetPayloadPropsFile(self):
    """Test GetPayloadPropsFile()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      payload_props_path = os.path.join(self.tempdir, 'test_update.gz.json')
      output = ('{"appid": "{0BB3F9E1-A066-9352-50B8-5C1356D09AEB}", '
                '"is_delta": false, "metadata_signature": null, '
                '"metadata_size": 57053, '
                '"sha256_hex": "aspPgQRWLu5wPM5NucqAYVmVCvL5lxQJ/n9ckhZS83Y=", '
                '"size": 998103540, '
                '"target_version": "99999.0.0", "version": 2}')
      bin_op = six.ensure_binary(output)

      transfer = self.CreateInstance(
          device, tempdir=self.tempdir, payload_name='test_update.gz')
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall',
                       return_value=cros_build_lib.CommandResult(stdout=bin_op))
      transfer.GetPayloadPropsFile()
      props = osutils.ReadFile(payload_props_path)

      self.assertEqual(props, output)
      self.assertEqual(transfer._local_payload_props_path,
                       payload_props_path)

  def testGetPayloadPropsFileWrongFormat(self):
    """Test GetPayloadPropsFile().

    Test exception thrown when the payload is not in the correct json format.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      output = 'Not in Json format'

      transfer = self.CreateInstance(
          device, tempdir=self.tempdir, payload_name='test_update.gz')

      self.PatchObject(self._transfer_class, '_RemoteDevserverCall',
                       return_value=cros_build_lib.CommandResult(stdout=output))

      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer.GetPayloadPropsFile)

  def testGetPayloadPropsFileError(self):
    """Test GetPayloadPropsFile().

    Test when the payload is not available.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, tempdir=self.tempdir, payload_name='test_update.gz',
          payload_dir='/test/dir')
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall',
                       side_effect=cros_build_lib.RunCommandError(msg=''))
      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer.GetPayloadPropsFile)
      self.assertIsNone(transfer._local_payload_props_path)

  def test_GetPayloadSize(self):
    """Test _GetPayloadSize()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='/test/payload/dir')
      expected_size = 75810234
      output = 'Content-Length: %s' % str(expected_size)
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall',
                       return_value=cros_build_lib.CommandResult(stdout=output))
      size = transfer._GetPayloadSize()
      self.assertEqual(size, expected_size)

  def test_GetPayloadSizeRemoteDevserverError(self):
    """Test _GetPayloadSize().

    Test when _RemoteDevserverCall() throws an error.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='/test/payload/dir')
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall',
                       side_effect=cros_build_lib.RunCommandError(msg=''))
      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer._GetPayloadSize)

  def test_GetPayloadSizeNoRegexMatchError(self):
    """Test errors thrown by _GetPayloadSize().

    Test error thrown when the output received from the curl command does not
    contain expected fields.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(
          device, payload_name='test_update.gz',
          payload_dir='/test/payload/dir')
      output = 'No Match Output'
      self.PatchObject(self._transfer_class, '_RemoteDevserverCall',
                       return_value=cros_build_lib.CommandResult(stdout=output))
      self.assertRaises(auto_updater_transfer.ChromiumOSTransferError,
                        transfer._GetPayloadSize)

  def test_RemoteDevserverCall(self):
    """Test _RemoteDevserverCall()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)

      self.PatchObject(cros_build_lib, 'run')
      cmd = ['test', 'command']

      transfer._RemoteDevserverCall(cmd=cmd)
      self.assertListEqual(
          cros_build_lib.run.call_args_list,
          [mock.call(['ssh', '0.0.0.0'] + cmd, log_output=True, stdout=False)])

  def test_RemoteDevserverCallWithStdout(self):
    """Test _RemoteDevserverCall()."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)

      self.PatchObject(cros_build_lib, 'run')
      cmd = ['test', 'command']

      transfer._RemoteDevserverCall(cmd=cmd, stdout=True)
      self.assertListEqual(
          cros_build_lib.run.call_args_list,
          [mock.call(['ssh', '0.0.0.0'] + cmd, log_output=True, stdout=True)])

  def test_RemoteDevserverCallError(self):
    """Test _RemoteDevserverCall().

    Test method when error is thrown by cros_build_lib.run() method.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      transfer = self.CreateInstance(device)

      self.PatchObject(cros_build_lib, 'run',
                       side_effect=cros_build_lib.RunCommandError(msg=''))

      self.assertRaises(cros_build_lib.RunCommandError,
                        transfer._RemoteDevserverCall,
                        cmd=['test', 'command'])
