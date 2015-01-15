# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A library to generate and store the manifests for cros builders to use."""

from __future__ import print_function

import logging
import os
import re
import tempfile
from xml.dom import minidom

from chromite.cbuildbot import cbuildbot_config
from chromite.cbuildbot import constants
from chromite.cbuildbot import manifest_version
from chromite.lib import cros_build_lib
from chromite.lib import git
from chromite.lib import timeout_util


# Paladin constants for manifest names.
PALADIN_COMMIT_ELEMENT = 'pending_commit'
PALADIN_REMOTE_ATTR = 'remote'
PALADIN_GERRIT_NUMBER_ATTR = 'gerrit_number'
PALADIN_PROJECT_ATTR = 'project'
PALADIN_BRANCH_ATTR = 'branch'
PALADIN_PROJECT_URL_ATTR = 'project_url'
PALADIN_REF_ATTR = 'ref'
PALADIN_CHANGE_ID_ATTR = 'change_id'
PALADIN_COMMIT_ATTR = 'commit'
PALADIN_PATCH_NUMBER_ATTR = 'patch_number'
PALADIN_OWNER_EMAIL_ATTR = 'owner_email'
PALADIN_FAIL_COUNT_ATTR = 'fail_count'
PALADIN_PASS_COUNT_ATTR = 'pass_count'
PALADIN_TOTAL_FAIL_COUNT_ATTR = 'total_fail_count'

CHROME_ELEMENT = 'chrome'
CHROME_VERSION_ATTR = 'version'
LKGM_ELEMENT = 'lkgm'
LKGM_VERSION_ATTR = 'version'

MANIFEST_ELEMENT = 'manifest'
DEFAULT_ELEMENT = 'default'
PROJECT_ELEMENT = 'project'
PROJECT_NAME_ATTR = 'name'
PROJECT_REMOTE_ATTR = 'remote'


class PromoteCandidateException(Exception):
  """Exception thrown for failure to promote manifest candidate."""


class FilterManifestException(Exception):
  """Exception thrown when failing to filter the internal manifest."""


class _LKGMCandidateInfo(manifest_version.VersionInfo):
  """Class to encapsualte the chrome os lkgm candidate info

  You can instantiate this class in two ways.
  1)using a version file, specifically chromeos_version.sh,
  which contains the version information.
  2) just passing in the 4 version components (major, minor, sp, patch and
    revision number),
  Args:
      You can instantiate this class in two ways.
  1)using a version file, specifically chromeos_version.sh,
  which contains the version information.
  2) passing in a string with the 3 version components + revision e.g. 41.0.0-r1
  Args:
    version_string: Optional 3 component version string to parse.  Contains:
        build_number: release build number.
        branch_build_number: current build number on a branch.
        patch_number: patch number.
        revision_number: version revision
    chrome_branch: If version_string specified, specify chrome_branch i.e. 13.
    version_file: version file location.
  """
  LKGM_RE = r'(\d+\.\d+\.\d+)(?:-rc(\d+))?'

  def __init__(self, version_string=None, chrome_branch=None, incr_type=None,
               version_file=None):
    self.revision_number = 1
    if version_string:
      match = re.search(self.LKGM_RE, version_string)
      assert match, 'LKGM did not re %s' % self.LKGM_RE
      super(_LKGMCandidateInfo, self).__init__(match.group(1), chrome_branch,
                                               incr_type=incr_type)
      if match.group(2):
        self.revision_number = int(match.group(2))

    else:
      super(_LKGMCandidateInfo, self).__init__(version_file=version_file,
                                               incr_type=incr_type)

  def VersionString(self):
    """returns the full version string of the lkgm candidate"""
    return '%s.%s.%s-rc%s' % (self.build_number, self.branch_build_number,
                              self.patch_number, self.revision_number)

  def VersionComponents(self):
    """Return an array of ints of the version fields for comparing."""
    return map(int, [self.build_number, self.branch_build_number,
                     self.patch_number, self.revision_number])

  def IncrementVersion(self):
    """Increments the version by incrementing the revision #."""
    self.revision_number += 1
    return self.VersionString()

  def UpdateVersionFile(self, *args, **kwargs):
    """Update the version file on disk.

    For LKGMCandidateInfo there is no version file so this function is a no-op.
    """


class LKGMManager(manifest_version.BuildSpecsManager):
  """A Class to manage lkgm candidates and their states.

  Vars:
    lkgm_subdir:  Subdirectory within manifest repo to store candidates.
  """
  # Sub-directories for LKGM and Chrome LKGM's.
  LKGM_SUBDIR = 'LKGM-candidates'
  CHROME_PFQ_SUBDIR = 'chrome-LKGM-candidates'
  COMMIT_QUEUE_SUBDIR = 'paladin'

  # Set path in repository to keep latest approved LKGM manifest.
  LKGM_PATH = 'LKGM/lkgm.xml'

  def __init__(self, source_repo, manifest_repo, build_names, build_type,
               incr_type, force, branch, manifest=constants.DEFAULT_MANIFEST,
               dry_run=True, master=False):
    """Initialize an LKGM Manager.

    Args:
      source_repo: Repository object for the source code.
      manifest_repo: Manifest repository for manifest versions/buildspecs.
      build_names: Identifiers for the build. Must match cbuildbot_config
          entries. If multiple identifiers are provided, the first item in the
          list must be an identifier for the group.
      build_type: Type of build.  Must be a pfq type.
      incr_type: How we should increment this version - build|branch|patch
      force: Create a new manifest even if there are no changes.
      branch: Branch this builder is running on.
      manifest: Manifest to use for checkout. E.g. 'full' or 'buildtools'.
      dry_run: Whether we actually commit changes we make or not.
      master: Whether we are the master builder.
    """
    super(LKGMManager, self).__init__(
        source_repo=source_repo, manifest_repo=manifest_repo,
        manifest=manifest, build_names=build_names, incr_type=incr_type,
        force=force, branch=branch, dry_run=dry_run, master=master)

    self.lkgm_path = os.path.join(self.manifest_dir, self.LKGM_PATH)
    self.compare_versions_fn = _LKGMCandidateInfo.VersionCompare
    self.build_type = build_type
    # Chrome PFQ and PFQ's exist at the same time and version separately so they
    # must have separate subdirs in the manifest-versions repository.
    if self.build_type == constants.CHROME_PFQ_TYPE:
      self.rel_working_dir = self.CHROME_PFQ_SUBDIR
    elif cbuildbot_config.IsCQType(self.build_type):
      self.rel_working_dir = self.COMMIT_QUEUE_SUBDIR
    else:
      assert cbuildbot_config.IsPFQType(self.build_type)
      self.rel_working_dir = self.LKGM_SUBDIR

  def GetCurrentVersionInfo(self):
    """Returns the lkgm version info from the version file."""
    version_info = super(LKGMManager, self).GetCurrentVersionInfo()
    return _LKGMCandidateInfo(version_info.VersionString(),
                              chrome_branch=version_info.chrome_branch,
                              incr_type=self.incr_type)

  def _AddLKGMToManifest(self, manifest):
    """Write the last known good version string to the manifest.

    Args:
      manifest: Path to the manifest.
    """
    # Get the last known good version string.
    try:
      lkgm_filename = os.path.basename(os.readlink(self.lkgm_path))
      lkgm_version, _ = os.path.splitext(lkgm_filename)
    except OSError:
      return

    # Write the last known good version string to the manifest.
    manifest_dom = minidom.parse(manifest)
    lkgm_element = manifest_dom.createElement(LKGM_ELEMENT)
    lkgm_element.setAttribute(LKGM_VERSION_ATTR, lkgm_version)
    manifest_dom.documentElement.appendChild(lkgm_element)
    with open(manifest, 'w+') as manifest_file:
      manifest_dom.writexml(manifest_file)

  def _AddChromeVersionToManifest(self, manifest, chrome_version):
    """Adds the chrome element with version |chrome_version| to |manifest|.

    The manifest file should contain the Chrome version to build for
    PFQ slaves.

    Args:
      manifest: Path to the manifest
      chrome_version: A string representing the version of Chrome
        (e.g. 35.0.1863.0).
    """
    manifest_dom = minidom.parse(manifest)
    chrome = manifest_dom.createElement(CHROME_ELEMENT)
    chrome.setAttribute(CHROME_VERSION_ATTR, chrome_version)
    manifest_dom.documentElement.appendChild(chrome)
    with open(manifest, 'w+') as manifest_file:
      manifest_dom.writexml(manifest_file)

  def _AddPatchesToManifest(self, manifest, patches):
    """Adds list of |patches| to given |manifest|.

    The manifest should have sufficient information for the slave
    builders to fetch the patches from Gerrit and to print the CL link
    (see cros_patch.GerritFetchOnlyPatch).

    Args:
      manifest: Path to the manifest.
      patches: A list of cros_patch.GerritPatch objects.
    """
    manifest_dom = minidom.parse(manifest)
    for patch in patches:
      pending_commit = manifest_dom.createElement(PALADIN_COMMIT_ELEMENT)
      pending_commit.setAttribute(PALADIN_REMOTE_ATTR, patch.remote)
      pending_commit.setAttribute(
          PALADIN_GERRIT_NUMBER_ATTR, patch.gerrit_number)
      pending_commit.setAttribute(PALADIN_PROJECT_ATTR, patch.project)
      pending_commit.setAttribute(PALADIN_PROJECT_URL_ATTR, patch.project_url)
      pending_commit.setAttribute(PALADIN_REF_ATTR, patch.ref)
      pending_commit.setAttribute(PALADIN_BRANCH_ATTR, patch.tracking_branch)
      pending_commit.setAttribute(PALADIN_CHANGE_ID_ATTR, patch.change_id)
      pending_commit.setAttribute(PALADIN_COMMIT_ATTR, patch.commit)
      pending_commit.setAttribute(PALADIN_PATCH_NUMBER_ATTR, patch.patch_number)
      pending_commit.setAttribute(PALADIN_OWNER_EMAIL_ATTR, patch.owner_email)
      pending_commit.setAttribute(PALADIN_FAIL_COUNT_ATTR,
                                  str(patch.fail_count))
      pending_commit.setAttribute(PALADIN_PASS_COUNT_ATTR,
                                  str(patch.pass_count))
      pending_commit.setAttribute(PALADIN_TOTAL_FAIL_COUNT_ATTR,
                                  str(patch.total_fail_count))
      manifest_dom.documentElement.appendChild(pending_commit)

    with open(manifest, 'w+') as manifest_file:
      manifest_dom.writexml(manifest_file)

  @staticmethod
  def _GetDefaultRemote(manifest_dom):
    """Returns the default remote in a manifest (if any).

    Args:
      manifest_dom: DOM Document object representing the manifest.

    Returns:
      Default remote if one exists, None otherwise.
    """
    default_nodes = manifest_dom.getElementsByTagName(DEFAULT_ELEMENT)
    if default_nodes:
      if len(default_nodes) > 1:
        raise FilterManifestException(
            'More than one <default> element found in manifest')
      return default_nodes[0].getAttribute(PROJECT_REMOTE_ATTR)
    return None

  @staticmethod
  def _FilterCrosInternalProjectsFromManifest(
      manifest, whitelisted_remotes=constants.EXTERNAL_REMOTES):
    """Returns a path to a new manifest with internal repositories stripped.

    Args:
      manifest: Path to an existing manifest that may have internal
        repositories.
      whitelisted_remotes: Tuple of remotes to allow in the external manifest.
        Only projects with those remotes will be included in the external
        manifest.

    Returns:
      Path to a new manifest that is a copy of the original without internal
        repositories or pending commits.
    """
    temp_fd, new_path = tempfile.mkstemp('external_manifest')
    manifest_dom = minidom.parse(manifest)
    manifest_node = manifest_dom.getElementsByTagName(MANIFEST_ELEMENT)[0]
    projects = manifest_dom.getElementsByTagName(PROJECT_ELEMENT)
    pending_commits = manifest_dom.getElementsByTagName(PALADIN_COMMIT_ELEMENT)

    default_remote = LKGMManager._GetDefaultRemote(manifest_dom)
    internal_projects = set()
    for project_element in projects:
      project_remote = project_element.getAttribute(PROJECT_REMOTE_ATTR)
      project = project_element.getAttribute(PROJECT_NAME_ATTR)
      if not project_remote:
        if not default_remote:
          # This should not happen for a valid manifest. Either each
          # project must have a remote specified or there should
          # be manifest default we could use.
          raise FilterManifestException(
              'Project %s has unspecified remote with no default' % project)
        project_remote = default_remote
      if project_remote not in whitelisted_remotes:
        internal_projects.add(project)
        manifest_node.removeChild(project_element)

    for commit_element in pending_commits:
      if commit_element.getAttribute(
          PALADIN_PROJECT_ATTR) in internal_projects:
        manifest_node.removeChild(commit_element)

    with os.fdopen(temp_fd, 'w') as manifest_file:
      # Filter out empty lines.
      filtered_manifest_noempty = filter(
          str.strip, manifest_dom.toxml('utf-8').splitlines())
      manifest_file.write(os.linesep.join(filtered_manifest_noempty))

    return new_path

  def CreateNewCandidate(self, validation_pool=None,
                         chrome_version=None,
                         retries=manifest_version.NUM_RETRIES,
                         build_id=None):
    """Creates, syncs to, and returns the next candidate manifest.

    Args:
      validation_pool: Validation pool to apply to the manifest before
        publishing.
      chrome_version: The Chrome version to write in the manifest. Defaults
        to None, in which case no version is written.
      retries: Number of retries for updating the status. Defaults to
        manifest_version.NUM_RETRIES.
      build_id: Optional integer cidb id of the build that is creating
                this candidate.

    Raises:
      GenerateBuildSpecException in case of failure to generate a buildspec
    """
    self.CheckoutSourceCode()

    # Refresh manifest logic from manifest_versions repository to grab the
    # LKGM to generate the blamelist.
    version_info = self.GetCurrentVersionInfo()
    self.RefreshManifestCheckout()
    self.InitializeManifestVariables(version_info)

    self._GenerateBlameListSinceLKGM()
    new_manifest = self.CreateManifest()

    # For Chrome PFQ, add the version of Chrome to use.
    if chrome_version:
      self._AddChromeVersionToManifest(new_manifest, chrome_version)

    # For the Commit Queue, apply the validation pool as part of checkout.
    if validation_pool:
      # If we have nothing that could apply from the validation pool and
      # we're not also a pfq type, we got nothing to do.
      assert self.cros_source.directory == validation_pool.build_root
      if (not validation_pool.ApplyPoolIntoRepo() and
          not cbuildbot_config.IsPFQType(self.build_type)):
        return None

      self._AddPatchesToManifest(new_manifest, validation_pool.changes)

      # Add info about the last known good version to the manifest. This will
      # be used by slaves to calculate what artifacts from old builds are safe
      # to use.
      self._AddLKGMToManifest(new_manifest)

    last_error = None
    for attempt in range(0, retries + 1):
      try:
        # Refresh manifest logic from manifest_versions repository.
        # Note we don't need to do this on our first attempt as we needed to
        # have done it to get the LKGM.
        if attempt != 0:
          self.RefreshManifestCheckout()
          self.InitializeManifestVariables(version_info)

        # If we don't have any valid changes to test, make sure the checkout
        # is at least different.
        if ((not validation_pool or not validation_pool.changes) and
            not self.force and self.HasCheckoutBeenBuilt()):
          return None

        # Check whether the latest spec available in manifest-versions is
        # newer than our current version number. If so, use it as the base
        # version number. Otherwise, we default to 'rc1'.
        if self.latest:
          latest = max(self.latest, version_info.VersionString(),
                       key=self.compare_versions_fn)
          version_info = _LKGMCandidateInfo(
              latest, chrome_branch=version_info.chrome_branch,
              incr_type=self.incr_type)

        git.CreatePushBranch(manifest_version.PUSH_BRANCH, self.manifest_dir,
                             sync=False)
        version = self.GetNextVersion(version_info)
        self.PublishManifest(new_manifest, version, build_id=build_id)
        self.current_version = version
        return self.GetLocalManifest(version)
      except cros_build_lib.RunCommandError as e:
        err_msg = 'Failed to generate LKGM Candidate. error: %s' % e
        logging.error(err_msg)
        last_error = err_msg

    raise manifest_version.GenerateBuildSpecException(last_error)

  def CreateFromManifest(self, manifest, retries=manifest_version.NUM_RETRIES,
                         build_id=None):
    """Sets up an lkgm_manager from the given manifest.

    This method sets up an LKGM manager and publishes a new manifest to the
    manifest versions repo based on the passed in manifest but filtering
    internal repositories and changes out of it.

    Args:
      manifest: A manifest that possibly contains private changes/projects. It
        is named with the given version we want to create a new manifest from
        i.e R20-1920.0.1-rc7.xml where R20-1920.0.1-rc7 is the version.
      retries: Number of retries for updating the status.
      build_id: Optional integer cidb build id of the build publishing the
                manifest.

    Raises:
      GenerateBuildSpecException in case of failure to check-in the new
        manifest because of a git error or the manifest is already checked-in.
    """
    last_error = None
    new_manifest = self._FilterCrosInternalProjectsFromManifest(manifest)
    version_info = self.GetCurrentVersionInfo()
    for _attempt in range(0, retries + 1):
      try:
        self.RefreshManifestCheckout()
        self.InitializeManifestVariables(version_info)

        git.CreatePushBranch(manifest_version.PUSH_BRANCH, self.manifest_dir,
                             sync=False)
        version = os.path.splitext(os.path.basename(manifest))[0]
        logging.info('Publishing filtered build spec')
        self.PublishManifest(new_manifest, version, build_id=build_id)
        self.current_version = version
        return self.GetLocalManifest(version)
      except cros_build_lib.RunCommandError as e:
        err_msg = 'Failed to generate LKGM Candidate. error: %s' % e
        logging.error(err_msg)
        last_error = err_msg

    raise manifest_version.GenerateBuildSpecException(last_error)

  def GetLatestCandidate(self, timeout=10 * 60):
    """Gets and syncs to the next candiate manifest.

    Args:
      timeout: The timeout in seconds.

    Returns:
      Local path to manifest to build or None in case of no need to build.

    Raises:
      GenerateBuildSpecException in case of failure to generate a buildspec
    """
    def _AttemptToGetLatestCandidate():
      """Attempts to acquire latest candidate using manifest repo."""
      self.RefreshManifestCheckout()
      self.InitializeManifestVariables(self.GetCurrentVersionInfo())
      if self.latest_unprocessed:
        return self.latest_unprocessed
      elif self.dry_run and self.latest:
        return self.latest

    def _PrintRemainingTime(remaining):
      logging.info('Found nothing new to build, will keep trying for %s',
                   remaining)
      logging.info('If this is a PFQ, then you should have forced the master'
                   ', which runs cbuildbot_master')

    # TODO(sosa):  We only really need the overlay for the version info but we
    # do a full checkout here because we have no way of refining it currently.
    self.CheckoutSourceCode()
    try:
      version_to_build = timeout_util.WaitForSuccess(
          lambda x: x is None,
          _AttemptToGetLatestCandidate,
          timeout,
          period=self.SLEEP_TIMEOUT,
          fallback_timeout=max(10, timeout),
          side_effect_func=_PrintRemainingTime)
    except timeout_util.TimeoutError:
      _PrintRemainingTime(0)
      version_to_build = _AttemptToGetLatestCandidate()

    if version_to_build:
      logging.info('Starting build spec: %s', version_to_build)
      self.current_version = version_to_build

      # Actually perform the sync.
      manifest = self.GetLocalManifest(version_to_build)
      self.cros_source.Sync(manifest)
      self._GenerateBlameListSinceLKGM()
      return manifest
    else:
      return None

  def PromoteCandidate(self, retries=manifest_version.NUM_RETRIES):
    """Promotes the current LKGM candidate to be a real versioned LKGM."""
    assert self.current_version, 'No current manifest exists.'

    last_error = None
    path_to_candidate = self.GetLocalManifest(self.current_version)
    assert os.path.exists(path_to_candidate), 'Candidate not found locally.'

    # This may potentially fail for not being at TOT while pushing.
    for attempt in range(0, retries + 1):
      try:
        if attempt > 0:
          self.RefreshManifestCheckout()
        git.CreatePushBranch(manifest_version.PUSH_BRANCH,
                             self.manifest_dir, sync=False)
        manifest_version.CreateSymlink(path_to_candidate, self.lkgm_path)
        git.RunGit(self.manifest_dir, ['add', self.LKGM_PATH])
        self.PushSpecChanges(
            'Automatic: %s promoting %s to LKGM' % (self.build_names[0],
                                                    self.current_version))
        return
      except cros_build_lib.RunCommandError as e:
        last_error = 'Failed to promote manifest. error: %s' % e
        logging.error(last_error)
        logging.error('Retrying to promote manifest:  Retry %d/%d', attempt + 1,
                      retries)

    raise PromoteCandidateException(last_error)

  def _ShouldGenerateBlameListSinceLKGM(self):
    """Returns True if we should generate the blamelist."""
    # We want to generate the blamelist only for valid pfq types and if we are
    # building on the master branch i.e. revving the build number.
    return (self.incr_type == 'build' and
            cbuildbot_config.IsPFQType(self.build_type) and
            self.build_type != constants.CHROME_PFQ_TYPE)

  def _GenerateBlameListSinceLKGM(self):
    """Prints out links to all CL's that have been committed since LKGM.

    Add buildbot trappings to print <a href='url'>text</a> in the waterfall for
    each CL committed since we last had a passing build.
    """
    if not self._ShouldGenerateBlameListSinceLKGM():
      logging.info('Not generating blamelist for lkgm as it is not appropriate '
                   'for this build type.')
      return
    # Suppress re-printing changes we tried ourselves on paladin
    # builders since they are redundant.
    only_print_chumps = self.build_type == constants.PALADIN_TYPE
    GenerateBlameList(self.cros_source, self.lkgm_path,
                      only_print_chumps=only_print_chumps)

  def GetLatestPassingSpec(self):
    """Get the last spec file that passed in the current branch."""
    raise NotImplementedError()


def GenerateBlameList(source_repo, lkgm_path, only_print_chumps=False):
  """Generate the blamelist since the specified manifest.

  Args:
    source_repo: Repository object for the source code.
    lkgm_path: Path to LKGM manifest.
    only_print_chumps: If True, only print changes that were chumped.
  """
  handler = git.Manifest(lkgm_path)
  reviewed_on_re = re.compile(r'\s*Reviewed-on:\s*(\S+)')
  author_re = re.compile(r'\s*Author:.*<(\S+)@\S+>\s*')
  committer_re = re.compile(r'\s*Commit:.*<(\S+)@\S+>\s*')
  for rel_src_path, checkout in handler.checkouts_by_path.iteritems():
    project = checkout['name']

    # Additional case in case the repo has been removed from the manifest.
    src_path = source_repo.GetRelativePath(rel_src_path)
    if not os.path.exists(src_path):
      cros_build_lib.Info('Detected repo removed from manifest %s' % project)
      continue

    revision = checkout['revision']
    cmd = ['log', '--pretty=full', '%s..HEAD' % revision]
    try:
      result = git.RunGit(src_path, cmd)
    except cros_build_lib.RunCommandError as ex:
      # Git returns 128 when the revision does not exist.
      if ex.result.returncode != 128:
        raise
      cros_build_lib.Warning('Detected branch removed from local checkout.')
      cros_build_lib.PrintBuildbotStepWarnings()
      return
    current_author = None
    current_committer = None
    for line in unicode(result.output, 'ascii', 'ignore').splitlines():
      author_match = author_re.match(line)
      if author_match:
        current_author = author_match.group(1)

      committer_match = committer_re.match(line)
      if committer_match:
        current_committer = committer_match.group(1)

      review_match = reviewed_on_re.match(line)
      if review_match:
        review = review_match.group(1)
        _, _, change_number = review.rpartition('/')
        items = [
            os.path.basename(project),
            current_author,
            change_number,
        ]
        if current_committer not in ('chrome-bot', 'chrome-internal-fetch',
                                     'chromeos-commit-bot'):
          items.insert(0, 'CHUMP')
        elif only_print_chumps:
          continue
        cros_build_lib.PrintBuildbotLink(' | '.join(items), review)
