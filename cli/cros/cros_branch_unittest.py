# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module tests the `cros branch` command."""

from __future__ import print_function

import os

from chromite.cbuildbot.manifest_version import VersionInfo
from chromite.cli import command_unittest
from chromite.cli.cros.cros_branch import Branch
from chromite.cli.cros.cros_branch import BranchCommand
from chromite.cli.cros.cros_branch import BranchError
from chromite.cli.cros.cros_branch import CanBranchProject
from chromite.cli.cros.cros_branch import CanPinProject
from chromite.cli.cros.cros_branch import CheckoutManager
from chromite.cli.cros.cros_branch import FactoryBranch
from chromite.cli.cros.cros_branch import FirmwareBranch
from chromite.cli.cros.cros_branch import ManifestRepository
from chromite.cli.cros.cros_branch import ReleaseBranch
from chromite.cli.cros.cros_branch import StabilizeBranch
from chromite.cli.cros.cros_branch import WhichVersionShouldBump
from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import cros_test_lib
from chromite.lib import git
from chromite.lib import osutils
from chromite.lib import partial_mock
from chromite.lib import repo_manifest
from chromite.lib import repo_util




def FileUrl(*args):
  """Map path components to a qualified local URL."""
  return 'file://%s' % os.path.join(*args)


def ParseManifestXml(xml):
  """Parse the XML into a repo_manifest.Manifest.

  Args:
    xml: Manifest XML as a string.

  Returns:
    The parsed repo_manifest.Manifest.
  """
  return repo_manifest.Manifest.FromString(
      xml, allow_unsupported_features=True)


def ManifestXml(*args):
  """Joins arbitrary XML and wraps it in a <manifest> element."""
  xml = '\n'.join(args)
  return '<?xml version="1.0" encoding="UTF-8"?><manifest>%s</manifest>' % xml


def DefaultXml(remote, revision):
  """Generates a <default> XML element as a string.

  Args:
    remote: Remote attribute.
    revision: Revision attribute.

  Returns:
    The default element as a string.
  """
  return '<default remote="%s" revision="%s" sync-j="8"/>' % (remote, revision)


def RemoteXml(name):
  """Generates a <remote> XML element as a string.

  Args:
    name: Name attribute.

  Returns:
    The remote element as a string.
  """
  return '<remote name="%s" fetch="%s-fetch"/>' % (name, name)


def ProjectXml(pid, host=None, name=None, root=None,
               remote=None, branch_mode=None):
  """Generates a <project> XML element as a string.

  Args:
    pid: Project ID. Used to generate most attributes not provided by caller.
    host: First element in name path. Significant for branching.
    name: Project name under the host. Generated by PID if not provided.
    root: Root of the project path. PID is always appended as leaf directory.
    remote: Remote attribute. Left blank if not provided.
    branch_mode: Value for branch-mode annotation.

  Returns:
    The project element as a string.
  """
  attrs = {
      'name': os.path.join(host or 'host', name or pid),
      'path': pid if not root else os.path.join(root, pid),
      'revision': git.NormalizeRef(pid),
  }
  if remote:
    attrs['remote'] = remote
  attrs_str = ' '.join('%s="%s"' % (k, v) for k, v in attrs.iteritems())
  xml = '<project %s>' % attrs_str
  if branch_mode:
    xml += '<annotation name="%s" value="%s"/>' % (
        constants.MANIFEST_ATTR_BRANCHING, branch_mode)
  return xml + '</project>'


def IncludeXml(name):
  """Generates a <include> XML element as a string.

  Args:
    name: Name attribute.

  Returns:
    The include element as a string.
  """
  return '<include name="%s"/>' % name


def AsAttrDict(*args):
  """Create AttrDict from string values, indexed by CAPS_CASE value."""
  return config_lib.AttrDict({v.upper().replace('-', '_'): v for v in args})


# A "project" in this dictionary is actually a project ID, which
# is used by helper functions to generate project name/path/revision/etc.
# If you add a project to this list, remember to update the categories below
# as well as PROJECTS_EXTERNAL_XML and its internal equivalent.
PROJECTS = AsAttrDict(
    'manifest',
    'manifest-internal',
    'chromite',
    'chromiumos-overlay',
    'multicheckout-a',
    'multicheckout-b',
    'implicit-pinned',
    'explicit-tot',
    'explicit-branch',
    'explicit-pinned')

# Categorize the projects above for use in testing.
PINNED_PROJECTS = (PROJECTS.EXPLICIT_PINNED, PROJECTS.IMPLICIT_PINNED)
TOT_PROJECTS = (PROJECTS.EXPLICIT_TOT,)
MULTI_CHECKOUT_PROJECTS = (PROJECTS.MULTICHECKOUT_A, PROJECTS.MULTICHECKOUT_B)
SINGLE_CHECKOUT_PROJECTS = (PROJECTS.CHROMIUMOS_OVERLAY,
                            PROJECTS.EXPLICIT_BRANCH,
                            PROJECTS.MANIFEST,
                            PROJECTS.MANIFEST_INTERNAL,
                            PROJECTS.CHROMITE)
BRANCHED_PROJECTS = SINGLE_CHECKOUT_PROJECTS + MULTI_CHECKOUT_PROJECTS
NON_BRANCHED_PROJECTS = PINNED_PROJECTS + TOT_PROJECTS
MANIFEST_PROJECTS = (PROJECTS.MANIFEST, PROJECTS.MANIFEST_INTERNAL)
EXTERNAL_PROJECTS = (PROJECTS.MANIFEST,
                     PROJECTS.CHROMITE,
                     PROJECTS.CHROMIUMOS_OVERLAY,
                     PROJECTS.IMPLICIT_PINNED,
                     PROJECTS.MULTICHECKOUT_A,
                     PROJECTS.MULTICHECKOUT_B)
INTERNAL_PROJECTS = (PROJECTS.MANIFEST_INTERNAL,
                     PROJECTS.EXPLICIT_TOT,
                     PROJECTS.EXPLICIT_BRANCH,
                     PROJECTS.EXPLICIT_PINNED)

# Define remotes. There is a public and an internal remote.
REMOTES = AsAttrDict('cros', 'cros-internal')

# Define hosts. These partly determine whether a project is branchable.
HOSTS = AsAttrDict('chromiumos', 'chromeos')

# Store commonly used values for convenience.
TOT = git.NormalizeRef('master')
SRC_PATH = 'src'
THIRD_PARTY_PATH = os.path.join(SRC_PATH, 'third_party')
EXTERNAL_FILE_NAME = 'external.xml'
INTERNAL_FILE_NAME = 'internal.xml'

# Create the raw XML using the above data. Note that by convention,
# the leaf directory of the project path MUST end with the project ID.
DEFAULT_XML = DefaultXml(REMOTES.CROS, TOT)
REMOTE_EXTERNAL_XML = RemoteXml(REMOTES.CROS)
REMOTE_INTERNAL_XML = RemoteXml(REMOTES.CROS_INTERNAL)
PROJECTS_EXTERNAL_XML = '\n'.join([
    ProjectXml(PROJECTS.MANIFEST, host=HOSTS.CHROMIUMOS),
    ProjectXml(PROJECTS.CHROMIUMOS_OVERLAY,
               host=HOSTS.CHROMIUMOS,
               name='overlays/chromiumos-overlay',
               root=THIRD_PARTY_PATH),
    ProjectXml(PROJECTS.CHROMITE, host=HOSTS.CHROMIUMOS),
    ProjectXml(PROJECTS.IMPLICIT_PINNED, root=SRC_PATH),
    ProjectXml(PROJECTS.MULTICHECKOUT_A,
               host=HOSTS.CHROMIUMOS,
               name='multicheckout',
               root=THIRD_PARTY_PATH),
    ProjectXml(PROJECTS.MULTICHECKOUT_B,
               host=HOSTS.CHROMIUMOS,
               name='multicheckout',
               root=THIRD_PARTY_PATH),
])
PROJECTS_INTERNAL_XML = '\n'.join([
    ProjectXml(PROJECTS.MANIFEST_INTERNAL,
               host=HOSTS.CHROMEOS,
               remote=REMOTES.CROS_INTERNAL),
    ProjectXml(PROJECTS.EXPLICIT_PINNED,
               host=HOSTS.CHROMEOS,
               root=SRC_PATH,
               remote=REMOTES.CROS_INTERNAL,
               branch_mode=constants.MANIFEST_ATTR_BRANCHING_PIN),
    ProjectXml(PROJECTS.EXPLICIT_BRANCH,
               host=HOSTS.CHROMEOS,
               root=SRC_PATH,
               remote=REMOTES.CROS_INTERNAL,
               branch_mode=constants.MANIFEST_ATTR_BRANCHING_CREATE),
    ProjectXml(PROJECTS.EXPLICIT_TOT,
               host=HOSTS.CHROMEOS,
               root=SRC_PATH,
               remote=REMOTES.CROS_INTERNAL,
               branch_mode=constants.MANIFEST_ATTR_BRANCHING_TOT),
])
INCLUDE_EXTERNAL_XML = IncludeXml(EXTERNAL_FILE_NAME)
INCLUDE_INTERNAL_XML = IncludeXml(INTERNAL_FILE_NAME)

# Combine the XML chunks above into meaningful files. Create files for
# both manifest and manifest-internal projects.
MANIFEST_FILES = {
    EXTERNAL_FILE_NAME: ManifestXml(DEFAULT_XML,
                                    REMOTE_EXTERNAL_XML,
                                    PROJECTS_EXTERNAL_XML),
    constants.OFFICIAL_MANIFEST: ManifestXml(INCLUDE_EXTERNAL_XML),
    constants.DEFAULT_MANIFEST: ManifestXml(INCLUDE_EXTERNAL_XML),
}
MANIFEST_INTERNAL_FILES = {
    EXTERNAL_FILE_NAME: MANIFEST_FILES[EXTERNAL_FILE_NAME],
    INTERNAL_FILE_NAME: ManifestXml(DEFAULT_XML,
                                    REMOTE_INTERNAL_XML,
                                    PROJECTS_INTERNAL_XML),
    constants.OFFICIAL_MANIFEST: ManifestXml(INCLUDE_INTERNAL_XML,
                                             INCLUDE_EXTERNAL_XML),
    constants.DEFAULT_MANIFEST: ManifestXml(INCLUDE_INTERNAL_XML,
                                            INCLUDE_EXTERNAL_XML),
}

# Finally, store the full, parsed manifest XML. Essentially the output
# of the command `repo manifest`.
FULL_XML = ManifestXml(DEFAULT_XML,
                       REMOTE_EXTERNAL_XML,
                       REMOTE_INTERNAL_XML,
                       PROJECTS_EXTERNAL_XML,
                       PROJECTS_INTERNAL_XML)


class ManifestTestCase(cros_test_lib.TestCase):
  """Test case providing valid manifest test data.

  This class generates a diverse collection of manifest XML strings, and
  provides convenience methods for reading from those manifests.
  """

  def NameFor(self, pid):
    """Return the test project's name.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay').

    Returns:
      Name of the project, e.g. 'chromeos/manifest-internal'.
    """
    return self.ProjectFor(pid).name

  def PathFor(self, pid):
    """Return the test project's path.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay').

    Returns:
      Path to the project, always of the form '<test path>/<project ID>'.
    """
    return self.ProjectFor(pid).Path()

  def PathListRegexFor(self, pid):
    """Return the test project's path as a ListRegex.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay').

    Returns:
      partial_mock.ListRegex for project path.
    """
    return partial_mock.ListRegex('.*/%s' % self.PathFor(pid))

  def RevisionFor(self, pid):
    """Return the test project's revision.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay')

    Returns:
      Reivision for the project, always of form 'refs/heads/<project ID>'.
    """
    return self.ProjectFor(pid).Revision()

  def ProjectFor(self, pid):
    """Return the test project's repo_manifest.Project.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay')

    Returns:
      Corresponding repo_manifest.Project.
    """
    # Project paths always end with the project ID, so use that as key.
    match = [p for p in self.full_manifest.Projects() if p.Path().endswith(pid)]
    assert len(match) == 1
    return match[0]

  def setUp(self):
    # Parse and cache the full manifest to take advantage of the
    # utility functions in repo_manifest.
    self.full_manifest = repo_manifest.Manifest.FromString(FULL_XML)


class UtilitiesTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for all top-level utility functions."""

  def SetVersion(self, version):
    """Mock VersionInfo.from_repo to always return the given version.

    Args:
      version: The version string to return.
    """
    self.PatchObject(VersionInfo, 'from_repo',
                     return_value=VersionInfo(version))

  def testCanBranchProjectAcceptsBranchableProjects(self):
    """Test CanBranchProject returns true when project is branchable."""
    for project in map(self.ProjectFor, BRANCHED_PROJECTS):
      self.assertTrue(CanBranchProject(project))

  def testCanBranchProjectRejectsNonBranchableProjects(self):
    """Test CanBranchProject returns false when project is not branchable."""
    for project in map(self.ProjectFor, NON_BRANCHED_PROJECTS):
      self.assertFalse(CanBranchProject(project))

  def testCanPinProjectAcceptsPinnedProjects(self):
    """Test CanPinProject returns true when project is pinned."""
    for project in map(self.ProjectFor, PINNED_PROJECTS):
      self.assertTrue(CanPinProject(project))

  def testCanPinProjectRejectsNonPinnedProjects(self):
    """Test CanPinProject returns false when project is not pinned."""
    for project in map(self.ProjectFor, BRANCHED_PROJECTS + TOT_PROJECTS):
      self.assertFalse(CanPinProject(project))

  def testTotMutualExclusivity(self):
    """Test CanBranch/PinProject both return false only when project is TOT."""
    for pid in PROJECTS.values():
      project = self.ProjectFor(pid)
      if not CanBranchProject(project) and not CanPinProject(project):
        self.assertIn(pid, TOT_PROJECTS)

  def testWhichVersionShouldBumpZeroBranchNumber(self):
    """Test WhichVersionShouldBump bumps branch number on X.0.0 version."""
    self.SetVersion('1.0.0')
    self.assertEqual(WhichVersionShouldBump(), 'branch')

  def testWhichVersionShouldBumpNonzeroBranchNumber(self):
    """Test WhichVersionShouldBump bumps patch number on X.X.0 version."""
    self.SetVersion('1.2.0')
    self.assertEqual(WhichVersionShouldBump(), 'patch')

  def testWhichVersionShouldBumpNonzeroPatchNumber(self):
    """Test WhichVersionShouldBump dies on X.X.X version."""
    self.SetVersion('1.2.3')
    with self.assertRaises(BranchError):
      WhichVersionShouldBump()


class CheckoutManagerTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for CheckoutManager functions."""

  def AssertCommandCalledInProject(self, cmd, expected=True):
    """Assert the command was called inside the git repo.

    Args:
      cmd: Command as a list of arguments.
      expected: True if the command should have been called.
    """
    self.rc_mock.assertCommandContains(
        cmd,
        cwd=partial_mock.ListRegex('.*/' + self.project.Path()),
        expected=expected)

  def SetCurrentBranch(self, branch):
    """Mock git.GetCurrentBranch to always return the given branch.

    Args:
      branch: Name of the branch to return.
    """
    self.PatchObject(git, 'GetCurrentBranch', return_value=branch)

  def setUp(self):
    self.project = self.ProjectFor(PROJECTS.CHROMIUMOS_OVERLAY)
    self.branch = self.project.Revision()
    self.remote = self.project.Remote().GitName()
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

  def testEnterNoCheckout(self):
    """Test __enter__ does not checkout when already on desired branch."""
    self.SetCurrentBranch(self.branch)
    with CheckoutManager(self.project):
      self.AssertCommandCalledInProject(['git', 'fetch'], expected=False)
      self.AssertCommandCalledInProject(['git', 'checkout'], expected=False)

  def testEnterWithCheckout(self):
    """Test __enter__ fetches and checkouts when not on desired branch."""
    self.SetCurrentBranch(TOT)
    with CheckoutManager(self.project):
      self.AssertCommandCalledInProject(
          ['git', 'fetch', self.remote, self.branch])
      self.AssertCommandCalledInProject(['git', 'checkout', 'FETCH_HEAD'])

  def testExitNoCheckout(self):
    """Test __exit__ does not checkout when already on desired branch."""
    self.SetCurrentBranch(self.branch)
    with CheckoutManager(self.project):
      pass
    self.AssertCommandCalledInProject(['git', 'checkout'], expected=False)

  def testExitWithCheckout(self):
    """Test __exit__ does checkouts old branch when not on desired branch."""
    self.SetCurrentBranch(TOT)
    with CheckoutManager(self.project):
      pass
    self.AssertCommandCalledInProject(['git', 'checkout', TOT])


class ManifestRepositoryTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for ManifestRepository functions."""

  def GetGitRepoRevisionMock(self, cwd):
    """Mock git.GetGitRepoRevision returning fake revision for given repo.

    Args:
      cwd: Path to the repo.

    Returns:
      The repo HEAD as a string.
    """
    return self.RevisionFor(os.path.basename(cwd))

  def FromFileMock(self, source, allow_unsupported_features=False):
    """Forward repo_manifest.FromFile to repo_manifest.FromString.

    Args:
      source: File name for internal manifest. Used to look up XML in a table.
      allow_unsupported_features: See repo_manifest.Manifest.

    Returns:
      repo_manifest.Manifest created from test data.
    """
    return repo_manifest.Manifest.FromString(
        MANIFEST_INTERNAL_FILES[source],
        allow_unsupported_features=allow_unsupported_features)

  def setUp(self):
    self.PatchObject(git, 'GetGitRepoRevision', self.GetGitRepoRevisionMock)
    self.PatchObject(repo_manifest.Manifest, 'FromFile', self.FromFileMock)

  def testManifestPath(self):
    """Test ManifestPath joins path with file name."""
    self.assertEqual(
        ManifestRepository('path/to').ManifestPath('manifest.xml'),
        'path/to/manifest.xml')

  def testListManifestsSingleFileNoIncludes(self):
    """Test ListManifests on a root file with no includes."""
    roots = expected = [EXTERNAL_FILE_NAME]
    actual = ManifestRepository('').ListManifests(roots)
    self.assertItemsEqual(actual, expected)

  def testListManifestsSingleFileWithIncludes(self):
    """Test ListManifests on a root file with unique includes."""
    roots = [constants.DEFAULT_MANIFEST]
    expected = roots + [EXTERNAL_FILE_NAME, INTERNAL_FILE_NAME]
    actual = ManifestRepository('').ListManifests(roots)
    self.assertItemsEqual(actual, expected)

  def testListManifestsMultipleFilesWithIncludes(self):
    """Test ListManifests on root files with shared includes."""
    roots = [constants.DEFAULT_MANIFEST, EXTERNAL_FILE_NAME]
    expected = roots + [INTERNAL_FILE_NAME]
    actual = ManifestRepository('').ListManifests(roots)
    self.assertItemsEqual(actual, expected)

  def testRepairManifestDeletesDefaultRevisions(self):
    """Test RepairManifest deletes revision attr on <default> and <remote>."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'beep',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'boop',
    }
    actual = ManifestRepository('').RepairManifest(INTERNAL_FILE_NAME, branches)
    self.assertIsNone(actual.Default().revision)
    self.assertIsNone(actual.GetRemote(REMOTES.CROS_INTERNAL).revision)

  def testRepairManifestUpdatesBranchedProjectRevisions(self):
    """Test RepairManifest updates revision=branch on branched projects."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'branch-a',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'branch-b'
    }
    actual = ManifestRepository('').RepairManifest(INTERNAL_FILE_NAME, branches)

    manifest_internal = actual.GetUniqueProject(
        self.NameFor(PROJECTS.MANIFEST_INTERNAL))
    self.assertEqual(manifest_internal.revision, 'refs/heads/branch-a')

    explicit_branch = actual.GetUniqueProject(
        self.NameFor(PROJECTS.EXPLICIT_BRANCH))
    self.assertEqual(explicit_branch.revision, 'refs/heads/branch-b')

  def testRepairManifestUpdatesPinnedProjectRevisions(self):
    """Test RepairManifest retains revision attr on pinned projects."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'irrelevant',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'should-not-matter'
    }
    actual = ManifestRepository('').RepairManifest(INTERNAL_FILE_NAME, branches)
    proj = actual.GetUniqueProject(self.NameFor(PROJECTS.EXPLICIT_PINNED))
    self.assertEqual(proj.revision, self.RevisionFor(PROJECTS.EXPLICIT_PINNED))

  def testRepairManifestUpdatesTotProjectRevisions(self):
    """Test RepairManifest sets revision=refs/heads/master on TOT projects."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'irrelevant',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'should-not-matter'
    }
    actual = ManifestRepository('').RepairManifest(INTERNAL_FILE_NAME, branches)
    proj = actual.GetUniqueProject(self.NameFor(PROJECTS.EXPLICIT_TOT))
    self.assertEqual(proj.revision, TOT)


class BranchTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests core functionality of Branch class."""

  def AssertProjectBranched(self, project, branch):
    """Assert branch created for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'checkout', '-B', branch, self.RevisionFor(project)],
        cwd=self.PathListRegexFor(project))

  def AssertBranchRenamed(self, project, branch):
    """Assert current branch renamed for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'branch', '-m', branch],
        cwd=self.PathListRegexFor(project))

  def AssertBranchDeleted(self, project, branch):
    """Assert given branch deleted for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'branch', '-D', branch],
        cwd=self.PathListRegexFor(project))

  def AssertProjectNotBranched(self, project):
    """Assert no branch was created for the given project.

    Args:
      project: Project ID.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'checkout', '-B'],
        cwd=self.PathListRegexFor(project),
        expected=False)

  def AssertBranchNotModified(self, project):
    """Assert no `git branch` calls for given project.

    Args:
      project: Project ID.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'branch'],
        cwd=self.PathListRegexFor(project),
        expected=False)

  def AssertManifestRepairsCommitted(self):
    """Assert commits made to all manifest repositories."""
    for manifest_project in MANIFEST_PROJECTS:
      self.rc_mock.assertCommandContains(
          ['git', 'commit', '-a'],
          cwd=partial_mock.ListRegex('.*/%s' % manifest_project))

  def setUp(self):
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

    # ManifestRepository and VersionInfo tested separately, so mock them.
    self.PatchObject(ManifestRepository, 'RepairManifestsOnDisk')
    self.PatchObject(VersionInfo, 'IncrementVersion')
    self.PatchObject(VersionInfo, 'UpdateVersionFile')
    self.PatchObject(
        VersionInfo, 'from_repo', return_value=VersionInfo('1.2.0'))

  def testCreateBranchesCorrectProjects(self):
    """Test Create branches the correct projects with correct branch names."""
    Branch('branch', self.full_manifest).Create()
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertProjectBranched(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertProjectBranched(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertProjectNotBranched(project)

  def testCreateRepairsManifests(self):
    """Test Create commits repairs to manifest repositories."""
    Branch('branch', self.full_manifest).Create()
    self.AssertManifestRepairsCommitted()

  def testRenameModifiesCorrectProjects(self):
    """Test Rename renames correct project branches to correct branch names."""
    Branch('branch', self.full_manifest).Rename()
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertBranchRenamed(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertBranchRenamed(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertBranchNotModified(project)

  def testRenameRepairsManifests(self):
    """Test Rename commits repairs to manifest repositories."""
    Branch('branch', self.full_manifest).Rename()
    self.AssertManifestRepairsCommitted()

  def testDeleteModifiesCorrectProjects(self):
    """Test Delete deletes correct project branches."""
    Branch('branch', self.full_manifest).Delete()
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertBranchDeleted(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertBranchDeleted(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertBranchNotModified(project)


class StandardBranchTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests branch logic specific to the standard branches."""

  def SetVersion(self, milestone, version):
    """Mock VersionInfo to always return the given versions.

    Args:
      milestone: The Chrome branch number, e.g. '47'
      version: The manifest version string, e.g. '1.2.0'
    """
    self.PatchObject(
        VersionInfo,
        'from_repo',
        return_value=VersionInfo(version, milestone))

  def testGenerateNameWithoutBranchVersion(self):
    """Test GenerateName on a X.0.0 version."""
    self.SetVersion('12', '3.0.0')
    branch_names = {
        'release-R12-3.B': ReleaseBranch,
        'factory-3.B': FactoryBranch,
        'firmware-3.B': FirmwareBranch,
        'stabilize-3.B': StabilizeBranch,
    }
    for branch_name, branch_type in branch_names.iteritems():
      self.assertEqual(branch_type(self.full_manifest).name, branch_name)

  def testGenerateNameWithBranchVersion(self):
    """Test GenerateName on a X.X.0 version."""
    self.SetVersion('12', '3.4.0')
    branch_names = {
        'release-R12-3.4.B': ReleaseBranch,
        'factory-3.4.B': FactoryBranch,
        'firmware-3.4.B': FirmwareBranch,
        'stabilize-3.4.B': StabilizeBranch,
    }
    for branch_name, cls in branch_names.iteritems():
      self.assertEqual(cls(self.full_manifest).name, branch_name)


class MockBranchCommand(command_unittest.MockCommand):
  """Mock out the `cros branch` command."""
  TARGET = 'chromite.cli.cros.cros_branch.BranchCommand'
  TARGET_CLASS = BranchCommand
  COMMAND = 'branch'


class BranchCommandTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for BranchCommand functions."""

  def RunCommandMock(self, args):
    """Patch the mock command and run it.

    Args:
      args: List of arguments for the command.
    """
    self.cmd = MockBranchCommand(args)
    self.StartPatcher(self.cmd)
    self.cmd.inst.Run()

  def AssertSynced(self, args):
    """Assert repo_sync_manifest was run with at least the given args.

    Args:
      args: Expected args for repo_sync_manifest.
    """
    self.cmd.rc_mock.assertCommandContains(
        [partial_mock.ListRegex('.*/repo_sync_manifest')] + args)

  def AssertNoDangerousOptions(self):
    """Assert that force and push were not set."""
    self.assertFalse(self.cmd.inst.options.force)
    self.assertFalse(self.cmd.inst.options.push)

  def setUp(self):
    self.cmd = None
    self.PatchObject(Branch, 'Create')
    self.PatchObject(Branch, 'Rename')
    self.PatchObject(Branch, 'Delete')
    self.PatchObject(repo_util.Repository, 'Manifest',
                     return_value=self.full_manifest)

  def testCreateReleaseCommandParses(self):
    """Test `cros branch create` parses with '--release' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--release'])
    self.assertIs(self.cmd.inst.options.cls, ReleaseBranch)
    self.AssertNoDangerousOptions()

  def testCreateFactoryCommandParses(self):
    """Test `cros branch create` parses with '--factory' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--factory'])
    self.assertIs(self.cmd.inst.options.cls, FactoryBranch)
    self.AssertNoDangerousOptions()

  def testCreateFirmwareCommandParses(self):
    """Test `cros branch create` parses with '--firmware' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--firmware'])
    self.assertIs(self.cmd.inst.options.cls, FirmwareBranch)
    self.AssertNoDangerousOptions()

  def testCreateStabilizeCommandParses(self):
    """Test `cros branch create` parses with '--stabilize' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--stabilize'])
    self.assertIs(self.cmd.inst.options.cls, StabilizeBranch)
    self.AssertNoDangerousOptions()

  def testCreateCustomCommandParses(self):
    """Test `cros branch create` parses with '--custom' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--custom', 'branch'])
    self.assertEqual(self.cmd.inst.options.name, 'branch')
    self.AssertNoDangerousOptions()

  def testCreateSyncsToFile(self):
    """Test `cros branch create` calls repo_sync_manifest to sync to file."""
    self.RunCommandMock(['create', '--file', 'manifest.xml', '--stabilize'])
    self.AssertSynced(['--manifest-file', 'manifest.xml'])

  def testCreateSyncsToVersion(self):
    """Test `cros branch create` calls repo_sync_manifest to sync to version."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--stabilize'])
    self.AssertSynced(['--version', '1.2.0'])

  def testRenameSyncsToBranch(self):
    """Test `cros branch rename` calls repo_sync_manifest to sync to branch."""
    self.RunCommandMock(['rename', 'branch', 'new-branch'])
    self.AssertSynced(['--branch', 'branch'])

  def testDeleteSyncsToBranch(self):
    """Test `cros branch delete` calls repo_sync_manifest to sync to branch."""
    self.RunCommandMock(['delete', 'branch'])
    self.AssertSynced(['--branch', 'branch'])


class FunctionalTest(ManifestTestCase, cros_test_lib.TempDirTestCase):
  """Test `cros branch` end to end on data generated from ManifestTestCase.

  This test creates external and internal "remotes" on disk using the test
  data generated by ManifestTestCase. A local checkout is also created by
  running `repo sync` on the fake internal remote. Projects on the remote
  are built from empty commits, with three exceptions: chromite, which
  contains the code under test, and manifest/manifest-internal, which contain
  test manifests.
  """

  def CreateTempDir(self, *args):
    """Create a temporary directory and return its absolute path.

    Args:
      args: Arbitrary subdirectories.

    Returns:
      Absolute path to new temporary directory.
    """
    path = os.path.join(self.tempdir, *args)
    osutils.SafeMakedirs(path)
    return path

  def CreateRef(self, git_repo, ref):
    """Create a ref in a git repository.

    The ref will point to a new commit containing all previously unstaged
    changes. If there are no active changes in the repo, the ref will point to a
    new, empty commit.

    Args:
      git_repo: Path to the repository.
      ref: Name of the ref to create.
    """
    git.RunGit(git_repo, ['add', '-A'])
    git.Commit(git_repo, 'Ref %s.' % ref, allow_empty=True)
    git.CreateBranch(git_repo, git.StripRefs(ref))

  def CreateProjectsOnRemote(self, remote, projects):
    """Create remote git repos for the given projects.

    This method creates two refs for each project: TOT, i.e. a master branch,
    and a project-specific branch. Any files in the project's directory will
    exist on both branches.

    Args:
      remote: Name of the remote.
      projects: List of projects IDs to be created on the remote.
    """
    for project in projects:
      repo_path = self.CreateTempDir(remote, self.NameFor(project))
      git.Init(repo_path)
      self.CreateRef(repo_path, TOT)
      self.CreateRef(repo_path, self.RevisionFor(project))

  def WriteManifestFiles(self, remote, project, files):
    """Write all manifest files to the given remote.

    Args:
      remote: Name of the remote.
      project: Manifest project ID.
      files: Dict mapping file name to string XML contents.

    Returns:
      Path to the created manifest project.
    """
    repo_path = self.CreateTempDir(remote, self.NameFor(project))
    for filename, xml in files.iteritems():
      manifest = ParseManifestXml(xml)
      for remote in manifest.Remotes():
        remote.fetch = (self.cros_root if remote.GitName() == REMOTES.CROS else
                        self.cros_internal_root)
      manifest.Write(os.path.join(repo_path, filename))
    return repo_path

  def setUp(self):
    # Create the remotes. We must create all root directories first
    # because remotes typically know about each other.
    self.cros_root = self.CreateTempDir(REMOTES.CROS)
    self.cros_internal_root = self.CreateTempDir(REMOTES.CROS_INTERNAL)

    self.WriteManifestFiles(REMOTES.CROS, PROJECTS.MANIFEST, MANIFEST_FILES)
    manifest_internal_root = self.WriteManifestFiles(REMOTES.CROS_INTERNAL,
                                                     PROJECTS.MANIFEST_INTERNAL,
                                                     MANIFEST_INTERNAL_FILES)

    self.CreateProjectsOnRemote(REMOTES.CROS, EXTERNAL_PROJECTS)
    self.CreateProjectsOnRemote(REMOTES.CROS_INTERNAL, INTERNAL_PROJECTS)

    # "Locally" checkout the internal remote.
    self.local_root = self.CreateTempDir('local')
    repo = repo_util.Repository.Initialize(
        root=self.local_root,
        manifest_url=manifest_internal_root,
        repo_url=FileUrl(constants.CHROOT_SOURCE_ROOT, '.repo/repo'),
        repo_branch='default')
    repo.Sync()

  def testSanity(self):
    """Validate code runs without dying."""
    pass
