# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Command for managing branches of chromiumos.

See go/cros-release-faq for information on types of branches, branching
frequency, naming conventions, etc.
"""

from __future__ import print_function

import collections
import os
import re

from chromite.cbuildbot import manifest_version
from chromite.cli import command
from chromite.lib import cros_logging as logging
from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import git
from chromite.lib import repo_manifest
from chromite.lib import repo_util


# A ProjectBranch is, simply, a git branch on a project.
#
# Fields:
#  - project: The repo_manifest.Project associated with the git branch.
#  - branch: The name of the git branch.
ProjectBranch = collections.namedtuple('ProjectBranch', ['project', 'branch'])


class BranchError(Exception):
  """Raised whenever any branch operation fails."""


def BranchMode(project):
  """Returns the project's explicit branch mode, if specified."""
  return project.Annotations().get('branch-mode', None)


def CanBranchProject(project):
  """Returns true if the project can be branched.

  The preferred way to specify branchability is by adding a "branch-mode"
  annotation on the project in the manifest. Of course, only one project
  in the manifest actually does this.

  The legacy method is to peek at the project's remote.

  Args:
    project: The repo_manifest.Project in question.

  Returns:
    True if the project is not pinned or ToT.
  """
  site_params = config_lib.GetSiteParams()
  remote = project.Remote().GitName()
  explicit_mode = BranchMode(project)
  if not explicit_mode:
    return (remote in site_params.CROS_REMOTES and
            remote in site_params.BRANCHABLE_PROJECTS and
            re.match(site_params.BRANCHABLE_PROJECTS[remote], project.name))
  return explicit_mode == constants.MANIFEST_ATTR_BRANCHING_CREATE


def CanPinProject(project):
  """Returns true if the project can be pinned.

  Args:
    project: The repo_manifest.Project in question.

  Returns:
    True if the project is pinned.
  """
  explicit_mode = BranchMode(project)
  if not explicit_mode:
    return not CanBranchProject(project)
  return explicit_mode == constants.MANIFEST_ATTR_BRANCHING_PIN


class ManifestRepository(object):
  """Represents a git repository of manifest XML files."""

  def __init__(self, checkout, project):
    self._checkout = checkout
    self._project = project

  def AbsoluteManifestPath(self, path):
    """Returns the full path to the manifest.

    Args:
      path: Relative path to the manifest.

    Returns:
      Full path to the manifest.
    """
    return self._checkout.AbsoluteProjectPath(self._project, path)

  def ReadManifest(self, path):
    """Read the manifest at the given path.

    Args:
      path: Path to the manifest.

    Returns:
      repo_manifest.Manifest object.
    """
    return repo_manifest.Manifest.FromFile(
        path,
        allow_unsupported_features=True)

  def ListManifests(self, root_manifests):
    """Finds all manifests included directly or indirectly by root manifests.

    For convenience, the returned set includes the root manifests. If any
    manifest is not found on disk, it is ignored.

    Args:
      root_manifests: Names of manifests whose includes will be traversed.

    Returns:
      Set of paths to included manifests.
    """
    pending = list(root_manifests)
    found = set()
    while pending:
      path = self.AbsoluteManifestPath(pending.pop())
      if path in found or not os.path.exists(path):
        continue
      found.add(path)
      manifest = self.ReadManifest(path)
      pending.extend([inc.name for inc in manifest.Includes()])
    return found

  def RepairManifest(self, path, branches_by_path):
    """Reads the manifest at the given path and repairs it in memory.

    Because humans rarely read branched manifests, this function optimizes for
    code readability and explicitly sets revision on every project in the
    manifest, deleting any defaults.

    Args:
      path: Path to the manifest, relative to the manifest project root.
      branches_by_path: Dict mapping project paths to branch names.

    Returns:
      The repaired repo_manifest.Manifest object.
    """
    manifest = self.ReadManifest(path)

    # Delete the default revision if specified by original manifest.
    default = manifest.Default()
    if default.revision:
      del default.revision

    # Delete remote revisions if specified by original manifest.
    for remote in manifest.Remotes():
      if remote.revision:
        del remote.revision

    # Update all project revisions.
    for project in manifest.Projects():
      if CanBranchProject(project):
        branch = branches_by_path[project.Path()]
        project.revision = git.NormalizeRef(branch)
      elif CanPinProject(project):
        project.revision = self._checkout.GitRevision(project)
      else:
        project.revision = git.NormalizeRef('master')

      if project.upstream:
        del project.upstream

    return manifest

  def RepairManifestsOnDisk(self, branches):
    """Repairs the revision and upstream attributes of manifest elements.

    The original manifests are overwritten by the repaired manifests.
    Note this method is "deep" because it processes includes.

    Args:
      branches: List a ProjectBranches for each branched project.
    """
    manifest_paths = self.ListManifests(
        [constants.DEFAULT_MANIFEST, constants.OFFICIAL_MANIFEST])
    branches_by_path = {project.Path(): branch for project, branch in branches}
    for manifest_path in manifest_paths:
      logging.info('Repairing manifest file %s', manifest_path)
      manifest = self.RepairManifest(manifest_path, branches_by_path)
      manifest.Write(manifest_path)


class CrosCheckout(object):
  """Represents a checkout of chromiumos on disk."""

  def __init__(self, root, manifest=None, repo_url=None, manifest_url=None):
    """Read the checkout manifest.

    Args:
      root: The repo root.
      manifest: The checkout manifest. Read from `repo manifest` if None.
      repo_url: Repo repository URL. Uses default googlesource repo if None.
      manifest_url: Manifest repository URL. Uses manifest-internal if None.
    """
    self.root = root
    self.manifest = manifest or repo_util.Repository(root).Manifest()
    self.repo_url = repo_url
    self.manifest_url = manifest_url

  def _Sync(self, manifest_args):
    """Run repo_sync_manifest command.

    Args:
      manifest_args: List of args for manifest group of repo_sync_manifest.
    """
    cmd = [os.path.join(constants.CHROMITE_DIR, 'scripts/repo_sync_manifest'),
           '--repo-root', self.root] + manifest_args
    if self.repo_url:
      cmd += ['--repo-url', self.repo_url]
    if self.manifest_url:
      cmd += ['--manifest-url', self.manifest_url]
    cros_build_lib.RunCommand(cmd, print_cmd=True)
    self.manifest = repo_util.Repository(self.root).Manifest()

  def SyncBranch(self, branch):
    """Sync to the given branch.

    Args:
      branch: Name of branch to sync to.
    """
    self._Sync(['--branch', branch])

  def SyncVersion(self, version):
    """Sync to the given manifest version.

    Args:
      version: Version string to sync to.
    """
    site_params = config_lib.GetSiteParams()
    self._Sync([
        '--manifest-versions-int',
        self.AbsolutePath(site_params.INTERNAL_MANIFEST_VERSIONS_PATH),
        '--manifest-versions-ext',
        self.AbsolutePath(site_params.EXTERNAL_MANIFEST_VERSIONS_PATH),
        '--version', version
    ])

  def SyncFile(self, path):
    """Sync to the given manifest file.

    Args:
      path: Path to the manifest file.
    """
    self._Sync(['--manifest-file', path])

  def ReadVersion(self, **kwargs):
    """Returns VersionInfo for the current checkout."""
    return manifest_version.VersionInfo.from_repo(self.root, **kwargs)

  def BumpVersion(self, which, branch, message, dry_run=True):
    """Increment version in chromeos_version.sh and commit it.

    Args:
      which: Which version should be incremented. One of
          'chrome_branch', 'build', 'branch, 'patch'.
      branch: The branch to bump version on.
      message: The commit message for the version bump.
      dry_run: Whether to use git --dry-run.
    """
    logging.info(message)

    chromiumos_overlay = self.manifest.GetUniqueProject(
        'chromiumos/overlays/chromiumos-overlay')
    remote = chromiumos_overlay.Remote().GitName()
    ref = git.NormalizeRef(branch)

    # Check if we need to fetch the branch.
    needs_fetch = not git.DoesCommitExistInRepo(
        self.AbsoluteProjectPath(chromiumos_overlay), ref)
    if needs_fetch:
      self.RunGit(chromiumos_overlay, ['fetch', remote, ref])

    # Checkout the branch.
    self.RunGit(chromiumos_overlay, ['checkout', branch])

    # Do the push.
    new_version = self.ReadVersion(incr_type=which)
    new_version.IncrementVersion()
    remote_ref = git.RemoteRef(remote, ref)
    new_version.UpdateVersionFile(message, dry_run=dry_run, push_to=remote_ref)

  def AbsolutePath(self, *args):
    """Joins the path components with the repo root.

    Args:
      *paths: Arbitrary relative path components, e.g. 'chromite/'

    Returns:
      The absolute checkout path.
    """
    return os.path.join(self.root, *args)

  def AbsoluteProjectPath(self, project, *args):
    """Joins the path components to the project's root.

    Args:
      project: The repo_manifest.Project in question.
      *args: Arbitrary relative path components.

    Returns:
      The joined project path.
    """
    return self.AbsolutePath(project.Path(), *args)

  def RunGit(self, project, cmd):
    """Run a git command inside the given project.

    Args:
      project: repo_manifest.Project to run the command in.
      cmd: Command as a list of arguments. Callers should exclude 'git'.
    """
    git.RunGit(self.AbsoluteProjectPath(project), cmd, print_cmd=True)

  def GitBranch(self, project):
    """Returns the project's current branch on disk.

    Args:
      project: The repo_manifest.Project in question.
    """
    return git.GetCurrentBranch(self.AbsoluteProjectPath(project))

  def GitRevision(self, project):
    """Return the project's current git revision on disk.

    Args:
      project: The repo_manifest.Project in question.

    Returns:
      Git revision as a string.
    """
    return git.GetGitRepoRevision(self.AbsoluteProjectPath(project))

  def BranchExists(self, project, pattern):
    """Determines if any branch exists that matches the given pattern.

    Args:
      project: The repo_manifest.Project in question.
      pattern: Branch name pattern to search for.

    Returns:
      True if a matching branch exists on the remote.
    """
    matches = git.MatchBranchName(self.AbsoluteProjectPath(project), pattern)
    return len(matches) != 0


class Branch(object):
  """Represents a branch of chromiumos, which may or may not exist yet.

  Note that all local branch operations assume the current checkout is
  synced to the correct version.
  """

  def __init__(self, checkout, name):
    """Cache various configuration used by all branch operations.

    Args:
      checkout: The synced CrosCheckout.
      name: The name of the branch.
    """
    self.checkout = checkout
    self.name = name

  def _ProjectBranchName(self, branch, project, original=None):
    """Determine's the git branch name for the project.

    Args:
      branch: The base branch name.
      project: The repo_manfest.Project in question.
      original: Original branch name to remove from the branch suffix.

    Returns:
      The branch name for the project.
    """
    # If project has only one checkout, the base branch name is fine.
    checkouts = [p.name for p in self.checkout.manifest.Projects()]
    if checkouts.count(project.name) == 1:
      return branch

    # Otherwise, the project branch name needs a suffix. We append its
    # upstream or revision to distinguish it from other checkouts.
    suffix = '-' + git.StripRefs(project.upstream or project.Revision())

    # If the revision is itself a branch, we need to strip the old branch name
    # from the suffix to keep naming consistent.
    if original:
      suffix = re.sub('^-%s-' % original, '-', suffix)

    return branch + suffix

  def _ProjectBranches(self, branch, original=None):
    """Return a list of ProjectBranches: one for each branchable project.

    Args:
      branch: The base branch name.
      original: Branch from which this branch of chromiumos stems, if any.
    """
    return [
        ProjectBranch(proj, self._ProjectBranchName(branch, proj, original))
        for proj in filter(CanBranchProject, self.checkout.manifest.Projects())
    ]

  def _ValidateBranches(self, branches):
    """Validates that branches do not already exist.

    Args:
      branches: Collection of ProjectBranch objects to valdiate.

    Raises:
      BranchError if any branch exists.
    """
    for project, branch in branches:
      if self.checkout.BranchExists(project, branch):
        raise BranchError(
            'Branch %s exists for %s. '
            'Please rerun with --force to proceed.' % (branch, project.name))

  def _CreateLocalBranches(self, branches):
    """Create git branches for all branchable projects in the local checkout.

    The branch uses the HEAD commit as the branch point.

    Args:
      branches: List of ProjectBranches to create.
    """
    for project, branch in branches:
      self.checkout.RunGit(project, ['checkout', '-B', branch])

  def _RepairManifestRepositories(self, branches):
    """Repair all manifests in all manifest repositories on current branch.

    Args:
      branches: List of ProjectBranches describing the repairs needed.
    """
    for project_name in config_lib.GetSiteParams().MANIFEST_PROJECTS:
      manifest_project = self.checkout.manifest.GetUniqueProject(project_name)
      manifest_repo = ManifestRepository(self.checkout, manifest_project)
      manifest_repo.RepairManifestsOnDisk(branches)
      self.checkout.RunGit(
          manifest_project,
          ['commit', '-a', '-m',
           'Manifests point to branch %s.' % self.name])

  def _WhichVersionShouldBump(self):
    """Returns which version is incremented by builds on a new branch."""
    vinfo = self.checkout.ReadVersion()
    assert not int(vinfo.patch_number)
    return 'patch' if int(vinfo.branch_build_number) else 'branch'

  def _PushBranchesToRemote(self, branches, dry_run=True, force=False):
    """Push state of local git branches to remote.

    Args:
      branches: List of ProjectBranches to push.
      force: Whether or not to overwrite existing branches on the remote.
      dry_run: Whether or not to set --dry-run.
    """
    for project, branch in branches:
      branch = git.NormalizeRef(branch)

      # We push the local branch to the same ref on the remote.
      # So the refspec should look like 'refs/heads/branch:refs/heads/branch'.
      refspec = '%s:%s' % (branch, branch)
      remote = project.Remote().GitName()

      cmd = ['push', remote, refspec]
      if dry_run:
        cmd.append('--dry-run')
      if force:
        cmd.append('--force')

      self.checkout.RunGit(project, cmd)

  def _DeleteBranchesOnRemote(self, branches, dry_run=True):
    """Push deletions of this branch for all projects.

    Args:
      branches: List of ProjectBranches for which to push delete.
      dry_run: Whether or not to set --dry-run.
    """
    for project, branch in branches:
      branch = git.NormalizeRef(branch)
      cmd = ['push', project.Remote().GitName(), '--delete', branch]
      if dry_run:
        cmd.append('--dry-run')
      self.checkout.RunGit(project, cmd)

  def Create(self, push=False, force=False):
    """Creates a new branch from the given version.

    Branches are always created locally, even when push is true.

    Args:
      push: Whether to push the new branch to remote.
      force: Whether or not to overwrite an existing branch.
    """
    branches = self._ProjectBranches(self.name)

    if not force:
      self._ValidateBranches(branches)

    self._CreateLocalBranches(branches)
    self._RepairManifestRepositories(branches)
    self._PushBranchesToRemote(branches, dry_run=not push, force=force)

    # Must bump version last because of how VersionInfo is implemented. Sigh...
    which_version = self._WhichVersionShouldBump()
    self.checkout.BumpVersion(
        which_version,
        self.name,
        'Bump %s number after creating branch %s.' % (which_version, self.name),
        dry_run=not push)

  def Rename(self, original, push=False, force=False):
    """Create this branch by renaming some other branch.

    There is no way to atomically rename a remote branch. Therefore, this
    method creates a new branch and then deletes the original.

    Args:
      original: Name of the original branch.
      push: Whether to push changes to remote.
      force: Whether or not to overwrite an existing branch.
    """
    new_branches = self._ProjectBranches(self.name, original=original)

    if not force:
      self._ValidateBranches(new_branches)

    self._CreateLocalBranches(new_branches)
    self._RepairManifestRepositories(new_branches)
    self._PushBranchesToRemote(new_branches, dry_run=not push, force=force)

    old_branches = self._ProjectBranches(original, original=original)
    self._DeleteBranchesOnRemote(old_branches, dry_run=not push)

  def Delete(self, push=False, force=False):
    """Delete this branch.

    Args:
      push: Whether to push the deletion to remote.
      force: Are you *really* sure you want to delete this branch on remote?
    """
    if push and not force:
      raise BranchError('Must set --force to delete remote branches.')
    branches = self._ProjectBranches(self.name, original=self.name)
    self._DeleteBranchesOnRemote(branches, dry_run=not push)


class StandardBranch(Branch):
  """Branch with a standard name, meaning it is suffixed by version."""

  def __init__(self, checkout, *args):
    """Determine the name for this branch.

    By convention, standard branch names must end with the major version from
    which they were created, followed by '.B'.

    For example:
      - A branch created from 1.0.0 must end with -1.B
      - A branch created from 1.2.0 must end with -1-2.B

    Args:
      checkout: The synced CrosCheckout.
      *args: Additional name components, which will be joined by dashes.
    """
    vinfo = checkout.ReadVersion()
    version = '.'.join(str(comp) for comp in vinfo.VersionComponents() if comp)
    name = '-'.join(filter(None, args) + (version,)) + '.B'
    super(StandardBranch, self).__init__(checkout, name)


class ReleaseBranch(StandardBranch):
  """Represents a release branch.

  Release branches have a slightly different naming scheme. They include
  the milestone from which they were created. Example: release-R12-1.2.B.

  Additionally, creating a release branches requires updating the milestone
  (Chrome branch) in chromeos_version.sh on master.
  """

  def __init__(self, checkout, descriptor=None):
    super(ReleaseBranch, self).__init__(
        checkout,
        'release',
        descriptor,
        'R%s' % checkout.ReadVersion().chrome_branch)

  def Create(self, push=False, force=False):
    super(ReleaseBranch, self).Create(push=push, force=force)
    # When a release branch has been successfully created, we report it by
    # bumping the milestone on the master. Note this also bumps build number
    # as a workaround for crbug.com/213075
    self.checkout.BumpVersion(
        'chrome_branch',
        'master',
        'Bump milestone after creating release branch %s.' % self.name,
        dry_run=not push)


class FactoryBranch(StandardBranch):
  """Represents a factory branch."""

  def __init__(self, checkout, descriptor=None):
    super(FactoryBranch, self).__init__(checkout, 'factory', descriptor)


class FirmwareBranch(StandardBranch):
  """Represents a firmware branch."""

  def __init__(self, checkout, descriptor=None):
    super(FirmwareBranch, self).__init__(checkout, 'firmware', descriptor)


class StabilizeBranch(StandardBranch):
  """Represents a minibranch."""

  def __init__(self, checkout, descriptor=None):
    super(StabilizeBranch, self).__init__(checkout, 'stabilize', descriptor)


@command.CommandDecorator('branch')
class BranchCommand(command.CliCommand):
  """Create, delete, or rename a branch of chromiumos.

  Branch creation implies branching all git repositories under chromiumos and
  then updating metadata on the new branch and occassionally on master.

  Metadata is updated as follows:
    1. The new branch's manifest is repaired to point to the new branch.
    2. Chrome OS version increments on new branch (e.g., 4230.0.0 -> 4230.1.0).
    3. If the new branch is a release branch, Chrome major version increments
       the on source branch (e.g., R70 -> R71).

  Performing any of these operations remotely requires special permissions.
  Please see go/cros-release-faq for details on obtaining those permissions.
  """

  EPILOG = """
Create example: firmware branch 'firmware-nocturne-11030.B'
  cros branch --push create --descriptor nocturne --version 11030.0.0 --firmware

Create example: release branch 'release-R70-11030.B'
  cros branch --push create --version 11030.0.0 --release

Create example: custom branch 'my-branch'
  cros branch --push create --version 11030.0.0 --custom my-branch

Create example: local minibranch 'stabilize-test-11030.B'
  cros branch create --version 11030.0.0 --descriptor test --stabilize

Rename Examples:
  cros branch rename release-R70-10509.B release-R70-10508.B
  cros branch --force --push rename release-R70-10509.B release-R70-10508.B

Delete Examples:
  cros branch delete release-R70-10509.B
  cros branch --force --push delete release-R70-10509.B
"""

  @classmethod
  def AddParser(cls, parser):
    """Add parser arguments."""
    super(BranchCommand, cls).AddParser(parser)

    # Common flags.
    remote_group = parser.add_argument_group(
        'Remote options',
        description='Arguments determine how branch operations interact with '
                    'remote repositories.')
    remote_group.add_argument(
        '--push',
        action='store_true',
        help='Push branch modifications to remote repos. '
             'Before setting this flag, ensure that you have the proper '
             'permissions and that you know what you are doing. Ye be warned.')
    remote_group.add_argument(
        '--force',
        action='store_true',
        help='Required for any remote operation that would delete an existing '
             'branch. Also required when trying to branch from a perviously '
             'branched manifest version.')

    sync_group = parser.add_argument_group(
        'Sync options',
        description='Arguments relating to how the checkout is synced. '
                    'These options are primarily used for testing.')
    sync_group.add_argument(
        '--root',
        default=constants.SOURCE_ROOT,
        help='Repo root of local checkout to branch. If not specificed, this '
             'tool will branch the checkout from which it is run.')
    sync_group.add_argument('--repo-url', help='Repo repository location.')
    sync_group.add_argument(
        '--manifest-url', help='URL of the manifest to be checked out.')

    # Create subcommand and flags.
    subparser = parser.add_subparsers(dest='subcommand')
    create_parser = subparser.add_parser('create', help='Create a branch.')

    name_group = create_parser.add_argument_group(
        'Name options', description='Arguments for determining branch name.')
    name_group.add_argument(
        '--descriptor',
        help='Optional descriptor for this branch. Typically, this is a build '
             'target or a device, depending on the nature of the branch. Used '
             'to generate the branch name. Cannot be used with --custom.')

    manifest_group = create_parser.add_argument_group(
        'Manifest options', description='Which manifest should be branched?')
    manifest_ex_group = manifest_group.add_mutually_exclusive_group(
        required=True)
    manifest_ex_group.add_argument(
        '--version',
        help="Manifest version to branch off, e.g. '10509.0.0'."
             'You may not branch off of the same version twice unless you run '
             'with --force.')
    manifest_ex_group.add_argument(
        '--file', help='Path to manifest file to branch off.')

    kind_group = create_parser.add_argument_group(
        'Kind options',
        description='What kind of branch is this? '
                    'These flags affect how manifest metadata is updated and '
                    'how the branch is named.')
    kind_ex_group = kind_group.add_mutually_exclusive_group(required=True)
    kind_ex_group.add_argument(
        '--release',
        dest='cls',
        action='store_const',
        const=ReleaseBranch,
        help='The new branch is a release branch. '
             "Named as 'release-<descriptor>-R<Milestone>-<Major Version>.B'.")
    kind_ex_group.add_argument(
        '--factory',
        dest='cls',
        action='store_const',
        const=FactoryBranch,
        help='The new branch is a factory branch. '
             "Named as 'factory-<Descriptor>-<Major Version>.B'.")
    kind_ex_group.add_argument(
        '--firmware',
        dest='cls',
        action='store_const',
        const=FirmwareBranch,
        help='The new branch is a firmware branch. '
             "Named as 'firmware-<Descriptor>-<Major Version>.B'.")
    kind_ex_group.add_argument(
        '--stabilize',
        dest='cls',
        action='store_const',
        const=StabilizeBranch,
        help='The new branch is a minibranch. '
             "Named as 'stabilize-<Descriptor>-<Major Version>.B'.")
    kind_ex_group.add_argument(
        '--custom',
        dest='name',
        help='Use a custom branch type with an explicit name. '
             'WARNING: custom names are dangerous. This tool greps branch '
             'names to determine which versions have already been branched. '
             'Version validation is not possible when the naming convention '
             'is broken. Use this at your own risk.')

    # Rename subcommand and flags.
    rename_parser = subparser.add_parser('rename', help='Rename a branch.')
    rename_parser.add_argument('old', help='Branch to rename.')
    rename_parser.add_argument('new', help='New name for the branch.')

    # Delete subcommand and flags.
    delete_parser = subparser.add_parser('delete', help='Delete a branch.')
    delete_parser.add_argument('branch', help='Name of the branch to delete.')

  def Run(self):
    checkout = CrosCheckout(
        self.options.root,
        repo_url=self.options.repo_url,
        manifest_url=self.options.manifest_url)
    push = self.options.push
    force = self.options.force

    # TODO(evanhernandez): If branch a operation is interrupted, some artifacts
    # might be left over. We should check for this.
    if self.options.subcommand == 'create':
      # Start with quick, immediate validations.
      if self.options.name and self.options.descriptor:
        raise BranchError('--descriptor cannot be used with --custom.')

      if self.options.version and not self.options.version.endswith('0'):
        raise BranchError('Cannot branch version from nonzero patch number.')

      # Handle sync. Unfortunately, we cannot fully validate the version until
      # we have a copy of chromeos_version.sh.
      if self.options.file:
        checkout.SyncFile(self.options.file)
      else:
        checkout.SyncVersion(self.options.version)

      # Now to validate the version. First, double check that the checkout
      # has a zero patch number in case we synced from file.
      vinfo = checkout.ReadVersion()
      if int(vinfo.patch_number):
        raise BranchError('Cannot branch version with nonzero patch number.')

      # Second, check that we did not already branch from this version.
      # manifest-internal serves as the sentinel project.
      manifest_internal = checkout.manifest.GetUniqueProject(
          'chromeos/manifest-internal')
      pattern = '.*-%s\\.B$' % '\\.'.join(
          str(comp) for comp in vinfo.VersionComponents() if comp)
      if checkout.BranchExists(manifest_internal, pattern) and not force:
        raise BranchError(
            'Already branched %s. Please rerun with --force if you wish to '
            'proceed.' % vinfo.VersionString())

      # Determine if we are creating a custom branch or a standard branch.
      if self.options.cls:
        branch = self.options.cls(checkout, self.options.descriptor)
      else:
        branch = Branch(checkout, self.options.name)

      # Finally, double check the name with the user.
      proceed = cros_build_lib.BooleanPrompt(
          prompt='New branch will be named %s. Continue?' % branch.name,
          default=False)
      if proceed:
        branch.Create(push=push, force=force)

    elif self.options.subcommand == 'rename':
      checkout.SyncBranch(self.options.old)
      branch = Branch(checkout, self.options.new)
      branch.Rename(self.options.old, push=push, force=force)

    elif self.options.subcommand == 'delete':
      checkout.SyncBranch(self.options.branch)
      branch = Branch(checkout, self.options.branch)
      branch.Delete(push=push, force=force)

    else:
      raise BranchError('Unrecognized option.')
