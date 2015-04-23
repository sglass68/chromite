# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Routines and a delegate for dealing with locally worked on packages."""

from __future__ import print_function

import glob
import os
import re

from chromite.cbuildbot import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import git
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import sysroot_lib


def GetWorkonPath(source_root=constants.CHROOT_SOURCE_ROOT, sub_path=None):
  """Get the path to files related to packages we're working locally on.

  Args:
    source_root: path to source root inside chroot.
    sub_path: optional path to file relative to the workon root directory.

  Returns:
    path to the workon root directory or file within the root directory.
  """
  ret = os.path.join(source_root, '.config/cros_workon')
  if sub_path:
    ret = os.path.join(ret, sub_path)

  return ret


class WorkonError(Exception):
  """Raised when invariants of the WorkonHelper are violated."""


def _FilterWorkonOnlyEbuilds(ebuilds):
  """Filter a list of ebuild paths to only with those no stable version.

  Args:
    ebuilds: list of string paths to ebuild files
        (e.g. ['/prefix/sys-app/app/app-9999.ebuild'])

  Returns:
    list of ebuild paths meeting this criterion.
  """
  result = []
  for ebuild_path in ebuilds:
    ebuild_pattern = os.path.join(os.path.dirname(ebuild_path), '*.ebuild')
    stable_ebuilds = [path for path in glob.glob(ebuild_pattern)
                      if not path.endswith('-9999.ebuild')]
    if not stable_ebuilds:
      result.append(ebuild_path)

  return result


def ListAllWorkedOnAtoms(src_root=constants.CHROOT_SOURCE_ROOT):
  """Get a list of all atoms we're currently working on.

  Args:
    src_root: path to source root inside chroot.

  Returns:
    Dictionary of atoms marked as worked on (e.g. ['chromeos-base/shill']) for
    each system.
  """
  workon_dir = GetWorkonPath(source_root=src_root)
  if not os.path.isdir(workon_dir):
    return dict()

  system_to_atoms = dict()
  for file_name in os.listdir(workon_dir):
    if file_name.endswith('.mask'):
      continue
    file_contents = osutils.ReadFile(os.path.join(workon_dir, file_name))

    atoms = []
    for line in file_contents.splitlines():
      match = re.match('=(.*)-9999', line)
      if match:
        atoms.append(match.group(1))
    if atoms:
      system_to_atoms[os.path.basename(file_name)] = atoms

  return system_to_atoms


class WorkonHelper(object):
  """Delegate that knows how to mark packages as being worked on locally.

  This class assumes that we're executing in the build root.
  """

  def __init__(self, sysroot, friendly_name=None, verbose=False,
               src_root=constants.CHROOT_SOURCE_ROOT):
    """Construct an instance.

    Args:
      sysroot: path to sysroot to work on packages within.
      friendly_name: friendly name of the system
          (e.g. 'host', <board name>, or a brick friendly name).
          Defaults to 'host' if sysroot is '/' or the last component of the
          sysroot path.
      verbose: boolean True iff we should print a lot more command output.
          This is intended for debugging, and you should never cause a script
          to depend on behavior enabled by this flag.
      src_root: path to source root inside chroot.
    """
    self._sysroot = sysroot
    if friendly_name:
      self._system = friendly_name
    else:
      self._system = ('host' if sysroot == '/'
                      else os.path.basename(sysroot.rstrip('/')))
    self._verbose = verbose
    self._src_root = src_root
    self._cached_overlays = None
    self._cached_arch = None
    if not os.path.exists(self._sysroot):
      raise WorkonError('Sysroot %s is not setup.' % self._sysroot)

  @property
  def workon_file_path(self):
    """Returns path to the file holding our currently worked on atoms."""
    return GetWorkonPath(source_root=self._src_root, sub_path=self._system)

  @property
  def masked_file_path(self):
    """Returns path to file masking non-9999 ebuilds for worked on atoms."""
    return self.workon_file_path + '.mask'

  @property
  def workon_file(self):
    """Return the content to the workon file or '' if it does not exist."""
    if os.path.exists(self.workon_file_path):
      return osutils.ReadFile(self.workon_file_path)
    return ''

  @property
  def masked_file(self):
    """Return the content to the masked file or '' if it does not exist."""
    if os.path.exists(self.masked_file_path):
      return osutils.ReadFile(self.masked_file_path)
    return ''

  @property
  def _arch(self):
    if self._cached_arch is None:
      self._cached_arch = sysroot_lib.Sysroot(
          self._sysroot).GetStandardField('ARCH')

    return self._cached_arch

  @property
  def _overlays(self):
    """Returns overlays installed for the selected system."""
    if self._cached_overlays is None:
      sysroot = sysroot_lib.Sysroot(self._sysroot)
      portdir_overlay = sysroot.GetStandardField('PORTDIR_OVERLAY')
      if portdir_overlay:
        self._cached_overlays = portdir_overlay.strip().splitlines()
      else:
        # This command is exceptionally slow, and we don't expect the list of
        # overlays to change during the lifetime of WorkonHelper.
        self._cached_overlays = portage_util.FindSysrootOverlays(self._sysroot)

    return self._cached_overlays

  def _AtomsToEbuilds(self, atoms):
    """Maps from a list of CP atoms to a list of corresponding -9999 ebuilds.

    Args:
      atoms: list of portage atoms (e.g. ['sys-apps/dbus']).

    Returns:
      list of ebuilds corresponding to those atoms.
    """
    atoms_to_ebuilds = dict([(atom, None) for atom in atoms])

    for overlay in self._overlays:
      ebuild_paths = glob.glob(
          os.path.join(overlay, '*-*', '*', '*-9999.ebuild'))
      for ebuild_path in ebuild_paths:
        atom = portage_util.EbuildToCP(ebuild_path)
        if atom in atoms_to_ebuilds:
          atoms_to_ebuilds[atom] = ebuild_path

    ebuilds = []
    for atom, ebuild in atoms_to_ebuilds.iteritems():
      if ebuild is None:
        raise WorkonError('Could not find ebuild for atom %s' % atom)
      ebuilds.append(ebuild)

    return ebuilds

  def _GetCanonicalAtom(self, package):
    """Transform a package name or name fragment to the canonical atom.

    If there a multiple atoms that a package name fragment could map to,
    picks an arbitrary one and prints a warning.

    Args:
      package: string package name or fragment of a name.

    Returns:
      string canonical atom name (e.g. 'sys-apps/dbus')
    """
    # Attempt to not hit portage if at all possible for speed.
    worked_on_atoms = self.workon_file.splitlines()
    if '=%s-9999' % package in worked_on_atoms:
      return package

    # Ask portage directly what it thinks about that package.
    ebuild_path = self._FindEbuildForPackage(package)

    # If portage didn't know about that package, try and autocomplete it.
    if ebuild_path is None:
      possible_ebuilds = []
      for ebuild in self._GetWorkonEbuilds(filter_on_arch=False):
        if package in ebuild:
          possible_ebuilds.append(ebuild)

      if not possible_ebuilds:
        logging.warning('Could not find canonical package for %s', package)
        return None

      if len(possible_ebuilds) > 1:
        logging.warning('Multiple autocompletes found: %s',
                        ' '.join(possible_ebuilds))
      autocompleted_package = portage_util.EbuildToCP(possible_ebuilds[0])
      logging.info('Autocompleted "%s" to: %s', package, autocompleted_package)

      return self._GetCanonicalAtom(autocompleted_package)

    # TODO(rcui): remove special casing of chromeos-chrome here when we make it
    # inherit from cros-workon / chromium-source class (chromium-os:19259).
    atom = portage_util.EbuildToCP(ebuild_path)
    if atom == 'chromeos-base/chromeos-chrome':
      return atom

    ebuild_contents = osutils.ReadFile(ebuild_path)
    if not re.search('^inherit .*(cros-workon|chromium-source)',
                     ebuild_contents, re.M):
      logging.warn('%s is not a cros-workon package', atom)
      return None

    return atom

  def _GetCanonicalAtoms(self, packages):
    """Transforms a list of package name fragments into a list of CP atoms.

    Args:
      packages: list of package name fragments.

    Returns:
      list of canonical portage atoms corresponding to the given fragments.
    """
    if not packages:
      raise WorkonError('No packages specified')
    if len(packages) == 1 and packages[0] == '.':
      raise WorkonError('Working on the current package is no longer '
                        'supported.')

    atoms = []
    for package_fragment in packages:
      atom = self._GetCanonicalAtom(package_fragment)
      if atom is None:
        raise WorkonError('Error parsing package list')
      atoms.append(atom)

    return atoms

  def _FindEbuildForPackage(self, package):
    """Find an ebuild for a given atom (accepting even masked ebuilds).

    Args:
      package: package string.

    Returns:
      path to ebuild for given package.
    """
    return portage_util.FindEbuildForPackage(
        package, self._sysroot, include_masked=True,
        extra_env={'ACCEPT_KEYWORDS': '~%s' % self._arch})

  def _GetWorkonEbuilds(self, filter_workon=False, filter_on_arch=True):
    """Get a list of of all cros-workon ebuilds in the current system.

    Args:
      filter_workon: True iff we should filter the list of ebuilds to those
          packages which define only a workon ebuild (i.e. no stable version).
      filter_on_arch: True iff we should only return ebuilds which are marked
          as unstable for the architecture of the system we're interested in.

    Returns:
      list of paths to ebuilds meeting the above criteria.
    """
    result = []
    workon_pat = re.compile('^inherit .*(cros-workon|chromium-source)', re.M)
    if filter_on_arch:
      keyword_pat = re.compile(r'^KEYWORDS=".*~(\*|%s).*"$' % self._arch, re.M)

    for overlay in self._overlays:
      ebuild_paths = glob.glob(
          os.path.join(overlay, '*-*', '*', '*-9999.ebuild'))
      for ebuild_path in ebuild_paths:
        ebuild_contents = osutils.ReadFile(ebuild_path)
        if not workon_pat.search(ebuild_contents):
          continue
        if filter_on_arch and not keyword_pat.search(ebuild_contents):
          continue
        result.append(ebuild_path)

    if filter_workon:
      result = _FilterWorkonOnlyEbuilds(result)

    return result

  def _GetLiveAtoms(self, filter_workon=False):
    """Get a list of atoms currently marked as being locally compiled.

    Args:
      filter_workon: True iff the list should be filtered to only those
          atoms without a stable version (i.e. the -9999 ebuild is the
          only ebuild).

    Returns:
      list of canonical portage atoms.
    """
    atoms = []
    for line in self.workon_file.splitlines():
      match = re.match('^=(.*)-9999$', line)
      if match:
        atoms.append(match.group(1))

    if filter_workon:
      ebuilds = _FilterWorkonOnlyEbuilds(self._AtomsToEbuilds(atoms))
      return [portage_util.EbuildToCP(ebuild) for ebuild in ebuilds]

    return atoms

  def _AddProjectsToPartialManifests(self, atoms):
    """Add projects corresponding to a list of atoms to the local manifest.

    If we mark projects as workon that we don't have in our local checkout,
    it is convenient to have them added to the manifest.  Note that users
    will need to `repo sync` to pull down repositories added in this way.

    Args:
      atoms: iterable of atoms to ensure are in the manifest.
    """
    if git.ManifestCheckout.IsFullManifest(self._src_root):
      # If we're a full manifest, there is nothing to do.
      return

    should_repo_sync = False
    for ebuild_path in self._AtomsToEbuild(atoms):
      infos = portage_util.GetRepositoryForEbuild(ebuild_path, self._sysroot)
      for info in infos:
        if not info.project:
          continue
        cmd = ['loman', 'add', '--workon', info.project]
        cros_build_lib.RunCommand(cmd, print_cmd=False)
        should_repo_sync = True

    if should_repo_sync:
      print('Please run "repo sync" now.')

  def ListAtoms(self, use_all=False, use_workon_only=False):
    """Returns a list of interesting atoms.

    By default, return a list of the atoms marked as being locally worked on
    for the system in question.

    Args:
      use_all: If true, return a list of all atoms we could possibly work on
          for the system in question.
      use_workon_only: If true, return a list of all atoms we could possibly
          work on that have no stable ebuild.

    Returns:
      a list of atoms (e.g. ['chromeos-base/shill', 'sys-apps/dbus']).
    """
    if use_workon_only or use_all:
      ebuilds = self._GetWorkonEbuilds(filter_workon=use_workon_only)
      packages = [portage_util.EbuildToCP(ebuild) for ebuild in ebuilds]
    else:
      packages = self._GetLiveAtoms()

    return sorted(packages)

  def StartWorkingOnPackages(self, packages, use_all=False,
                             use_workon_only=False):
    """Mark a list of packages as being worked on locally.

    Args:
      packages: list of package name fragments.  While each fragment could be a
          a complete portage atom, this helper will attempt to infer intent by
          looking for fragments in a list of all possible atoms for the system
          in question.
      use_all: True iff we should ignore the package list, and instead consider
          all possible atoms that we could mark as worked on locally.
      use_workon_only: True iff we should ignore the package list, and instead
          consider all possible atoms for the system in question that define
          only the -9999 ebuild.
      """
    if use_all or use_workon_only:
      ebuilds = self._GetWorkonEbuilds(filter_workon=use_workon_only)
      atoms = [portage_util.EbuildToCP(ebuild) for ebuild in ebuilds]
    else:
      atoms = self._GetCanonicalAtoms(packages)
    atoms = set(atoms)

    # Read out what atoms we're already working on.
    existing_atoms = set()
    for line in self.workon_file.splitlines():
      if not line.startswith('=') or not line.endswith('-9999'):
        logging.warning('Filtering out malformed atom workon line: %s', line)
        continue
      existing_atoms.add(line[1:-5])

    # Warn the user if they're requested to work on an atom that's already
    # marked as being worked on.
    for atom in atoms & existing_atoms:
      logging.warning('Already working on %s', atom)

    # If we have no new atoms to work on, we can quit now.
    new_atoms = atoms - existing_atoms
    if not new_atoms:
      return

    # Write out all these atoms to the appropriate files.
    current_atoms = new_atoms | existing_atoms
    for pattern, file_path in (('=%s-9999\n', self.workon_file_path),
                               ('<%s-9999\n', self.masked_file_path)):
      contents = ''.join([pattern % atom for atom in current_atoms])
      osutils.WriteFile(file_path, contents, makedirs=True)

    self._AddProjectsToPartialManifests(new_atoms)

    # Legacy scripts used single quotes in their output, and we carry on this
    # honorable tradition.
    logging.info("Started working on '%s' for '%s'",
                 ' '.join(new_atoms), self._system)

  def StopWorkingOnPackages(self, packages, use_all=False,
                            use_workon_only=False):
    """Stop working on a list of packages currently marked as locally worked on.

    Args:
      packages: list of package name fragments.  These will be mapped to
          canonical portage atoms via the same process as
          StartWorkingOnPackages().
      use_all: True iff instead of the provided package list, we should just
          stop working on all currently worked on atoms for the system in
          question.
      use_workon_only: True iff instead of the provided package list, we should
          stop working on all currently worked on atoms that define only a
          -9999 ebuild.
    """
    if use_all or use_workon_only:
      atoms = self._GetLiveAtoms(filter_workon=use_workon_only)
    else:
      atoms = self._GetCanonicalAtoms(packages)

    workon_lines = self.workon_file.splitlines()
    mask_lines = self.masked_file.splitlines()
    stopped_atoms = []
    for atom in atoms:
      workon_line = '=%s-9999' % atom
      mask_line = '<%s-9999' % atom
      if not workon_line in workon_lines:
        logging.warn('Not working on %s', atom)
        continue
      workon_lines = [x for x in workon_lines if x != workon_line]
      mask_lines = [x for x in mask_lines if x != mask_line]
      stopped_atoms.append(atom)

    osutils.WriteFile(self.workon_file_path, '\n'.join(workon_lines),
                      makedirs=True)
    osutils.WriteFile(self.masked_file_path, '\n'.join(mask_lines),
                      makedirs=True)

    if stopped_atoms:
      # Legacy scripts used single quotes in their output, and we carry on this
      # honorable tradition.
      logging.info("Stopped working on '%s' for '%s'",
                   ' '.join(stopped_atoms), self._system)

  def RunCommandInAtomSourceDirectory(self, atom, command):
    """Run a command in the source directory of an atom.

    Args:
      atom: string atom to run the command in (e.g. 'chromeos-base/shill').
      command: string shell command to run in the source directory of |atom|.
    """
    logging.info('Running "%s" on %s', command, atom)
    ebuild_path = self._FindEbuildForPackage(atom)
    if ebuild_path is None:
      raise WorkonError('Error looking for atom %s' % atom)

    for info in portage_util.GetRepositoryForEbuild(ebuild_path, self._sysroot):
      cros_build_lib.RunCommand(command, shell=True, cwd=info.srcdir,
                                print_cmd=False)

  def RunCommandInPackages(self, packages, command, use_all=False,
                           use_workon_only=False):
    """Run a command in the source directory of a list of packages.

    Args:
      packages: list of package name fragments.
      command: string shell command to run in the source directory of |atom|.
      use_all: True iff we should ignore the package list, and instead consider
          all possible workon-able atoms.
      use_workon_only: True iff we should ignore the package list, and instead
          consider all possible atoms for the system in question that define
          only the -9999 ebuild.
    """
    if use_all or use_workon_only:
      atoms = self._GetLiveAtoms(filter_workon=use_workon_only)
    else:
      atoms = self._GetCanonicalAtoms(packages)
    for atom in atoms:
      self.RunCommandInAtomSourceDirectory(atom, command)
