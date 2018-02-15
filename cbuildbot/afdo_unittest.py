# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for afdo module."""

from __future__ import print_function

import os
import time

from chromite.cbuildbot import afdo
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import osutils
from chromite.lib import portage_util


class AfdoTest(cros_test_lib.MockTempDirTestCase):
  """Unit test of afdo module."""

  def testFindLatestProfile(self):
    versions = [[1, 0, 0, 0], [1, 2, 3, 4], [2, 2, 2, 2]]
    self.assertEqual(afdo.FindLatestProfile([0, 0, 0, 0], versions), None)
    self.assertEqual(afdo.FindLatestProfile([1, 0, 0, 0], versions),
                     [1, 0, 0, 0])
    self.assertEqual(afdo.FindLatestProfile([1, 2, 0, 0], versions),
                     [1, 0, 0, 0])
    self.assertEqual(afdo.FindLatestProfile([9, 9, 9, 9], versions),
                     [2, 2, 2, 2])

  def testPatchKernelEbuild(self):
    before = [
        'The following line contains the version:',
        'AFDO_PROFILE_VERSION="R63-9901.21-1506581597"',
        'It should be changed.'
    ]
    after = [
        'The following line contains the version:',
        'AFDO_PROFILE_VERSION="R12-3456.78-9876543210"',
        'It should be changed.'
    ]
    tf = os.path.join(self.tempdir, 'test.ebuild')
    osutils.WriteFile(tf, '\n'.join(before))
    afdo.PatchKernelEbuild(tf, [12, 3456, 78, 9876543210])
    x = osutils.ReadFile(tf).splitlines()
    self.assertEqual(after, x)

  def testGetAvailableKernelProfiles(self):
    def MockGsList(path):
      unused = {'content_length':None,
                'creation_time':None,
                'generation':None,
                'metageneration':None}
      path = path.replace('*', '%s')
      return [
          gs.GSListResult(
              url=(path % ('4.4', 'R63-9901.21-1506581597')), **unused),
          gs.GSListResult(
              url=(path % ('3.8', 'R61-9765.70-1506575230')), **unused),
      ]

    self.PatchObject(gs.GSContext, 'List',
                     lambda _, path, **kwargs: MockGsList(path))
    profiles = afdo.GetAvailableKernelProfiles()
    self.assertIn([63, 9901, 21, 1506581597], profiles['4.4'])
    self.assertIn([61, 9765, 70, 1506575230], profiles['3.8'])

  def testFindKernelEbuilds(self):
    ebuilds = [(os.path.basename(ebuild[0]), ebuild[1])
               for ebuild in afdo.FindKernelEbuilds()]
    self.assertIn(('chromeos-kernel-4_4-9999.ebuild', '4.4'), ebuilds)
    self.assertIn(('chromeos-kernel-3_8-9999.ebuild', '3.8'), ebuilds)

  def testProfileAge(self):
    self.assertEqual(
        0,
        afdo.ProfileAge([0, 0, 0, int(time.time())])
    )
    self.assertEqual(
        1,
        afdo.ProfileAge([0, 0, 0, int(time.time() - 86400)])
    )

  def testGetCWPProfile(self):
    profiles = ['chromeos-chrome-amd64-62.0.3202.43_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-63.0.3223.0_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-63.0.3239.20_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-63.0.3239.42_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-63.0.3239.50_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-63.0.3239.50_rc-r2.afdo.bz2',
                'chromeos-chrome-amd64-64.0.3280.5_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-64.0.3282.41_rc-r1.afdo.bz2',
                'chromeos-chrome-amd64-65.0.3299.0_rc-r1.afdo.bz2']

    def MockGsList(path):
      unused = {'content_length':None,
                'creation_time':None,
                'generation':None,
                'metageneration':None}
      return [gs.GSListResult(url=os.path.join(path, f),
                              **unused) for f in profiles]

    self.PatchObject(gs.GSContext, 'List',
                     lambda _, path, **kwargs: MockGsList(path))

    def _test(version, idx):
      unused = {'pv':None,
                'package':None,
                'version_no_rev':None,
                'rev':None,
                'category':None}
      cpv = portage_util.CPV(version=version, **unused)
      profile = afdo.GetCWPProfile(cpv, 'unused', 'unused', gs.GSContext())
      self.assertEqual(profile, profiles[idx][:-4])

    _test('66.0.3300.0_rc-r1', 8)
    _test('65.0.3283.0_rc-r1', 1)
    _test('65.0.3283.1_rc-r1', 1)
    _test('64.0.3282.42_rc-r1', 7)
    _test('63.0.3239.30_rc-r1', 2)
    _test('63.0.3239.42_rc-r0', 2)
    _test('63.0.3239.42_rc-r1', 3)
