#!/usr/bin/python

# Copyright (c) 2010 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Helper script for printing differences between tags."""

import cgi
from datetime import datetime
import operator
import optparse
import os
import re
import sys

from chromite.lib.cros_build_lib import RunCommand


# TODO(dianders):
# We use GData to access the tracker on code.google.com.  Eventually, we
# want to create an ebuild and add the ebuild to hard-host-depends
# For now, we'll just include instructions for installing it.
INSTRS_FOR_GDATA = """
To access the tracker you need the GData library.  To install in your home dir:

  GDATA_INSTALL_DIR=~/gdatalib
  mkdir -p "$GDATA_INSTALL_DIR"

  TMP_DIR=`mktemp -d`
  pushd $TMP_DIR
  wget http://gdata-python-client.googlecode.com/files/gdata-2.0.12.zip
  unzip gdata-2.0.12.zip
  cd gdata-2.0.12/
  python setup.py install --home="$GDATA_INSTALL_DIR"
  popd

  export PYTHONPATH="$GDATA_INSTALL_DIR/lib/python:$PYTHONPATH"

You should add the PYTHONPATH line to your .bashrc file (or equivalent)."""


DEFAULT_TRACKER = 'chromium-os'


def _GrabOutput(cmd):
  """Returns output from specified command."""
  return RunCommand(cmd, shell=True, print_cmd=False,
                    redirect_stdout=True).output


def _GrabTags():
  """Returns list of tags from current git repository."""
  # TODO(dianders): replace this with the python equivalent.
  cmd = ("git for-each-ref refs/tags | awk '{print $3}' | "
         "sed 's,refs/tags/,,g' | sort -t. -k3,3rn -k4,4rn")
  return _GrabOutput(cmd).split()


def _GrabDirs():
  """Returns list of directories managed by repo."""
  return _GrabOutput('repo forall -c "pwd"').split()


class Issue(object):
  """Class for holding info about issues (aka bugs)."""

  def __init__(self, project_name, issue_id, tracker_acc):
    """Constructor for Issue object.

    Args:
      project_name: The tracker project to query.
      issue_id: The ID of the issue to query
      tracker_acc: A TrackerAccess object, or None.
    """
    self.project_name = project_name
    self.issue_id = issue_id
    self.milestone = ''
    self.priority = ''

    if tracker_acc is not None:
      keyed_labels = tracker_acc.GetKeyedLabels(project_name, issue_id)
      if 'Mstone' in keyed_labels:
        self.milestone = keyed_labels['Mstone']
      if 'Pri' in keyed_labels:
        self.priority = keyed_labels['Pri']

  def GetUrl(self):
    """Returns the URL to access the issue."""
    bug_url_fmt = 'http://code.google.com/p/%s/issues/detail?id=%s'

    # Get bug URL. We use short URLs to make the URLs a bit more readable.
    if self.project_name == 'chromium-os':
      bug_url = 'http://crosbug.com/%s' % self.issue_id
    elif self.project_name == 'chrome-os-partner':
      bug_url = 'http://crosbug.com/p/%s' % self.issue_id
    else:
      bug_url = bug_url_fmt % (self.project_name, self.issue_id)

    return bug_url

  def __str__(self):
    """Provides a string representation of the issue.

    Returns:
      A string that looks something like:

      project:id (milestone, priority)
    """
    if self.milestone and self.priority:
      info_str = ' (%s, P%s)' % (self.milestone, self.priority)
    elif self.milestone:
      info_str = ' (%s)' % self.milestone
    elif self.priority:
      info_str = ' (P%s)' % self.priority
    else:
      info_str = ''

    return '%s:%s%s' % (self.project_name, self.issue_id, info_str)

  def __cmp__(self, other):
    """Compare two Issue objects."""
    return cmp((self.project_name.lower(), self.issue_id),
               (other.project_name.lower(), other.issue_id))


class Commit(object):
  """Class for tracking git commits."""

  def __init__(self, commit, projectname, commit_email, commit_date, subject,
               body, tracker_acc):
    """Create commit logs.

    Args:
      commit: The commit hash (sha) from git.
      projectname: The project name, from:
                   git config --get remote.cros.projectname
      commit_email: The email address associated with the commit (%ce in git
                    log)
      commit_date: The date of the commit, like "Mon Nov 1 17:34:14 2010 -0500"
                   (%cd in git log))
      subject: The subject of the commit (%s in git log)
      body: The body of the commit (%b in git log)
      tracker_acc: A tracker_access.TrackerAccess object.
    """
    self.commit = commit
    self.projectname = projectname
    self.commit_email = commit_email
    fmt = '%a %b %d %H:%M:%S %Y'
    self.commit_date = datetime.strptime(commit_date, fmt)
    self.subject = subject
    self.body = body
    self._tracker_acc = tracker_acc
    self._issues = self._GetIssues()

  def _GetIssues(self):
    """Get bug info from commit logs and issue tracker.

    This should be called as the last step of __init__, since it
    assumes that our member variables are already setup.

    Returns:
      A list of Issue objects, each of which holds info about a bug.
    """
    # NOTE: most of this code is copied from bugdroid:
    #   <http://src.chromium.org/viewvc/chrome/trunk/tools/bugdroid/bugdroid.py?revision=59229&view=markup>

    # Get a list of bugs.  Handle lots of possibilities:
    # - Multiple "BUG=" lines, with varying amounts of whitespace.
    # - For each BUG= line, bugs can be split by commas _or_ by whitespace (!)
    entries = []
    for line in self.body.split('\n'):
      match = re.match(r'^ *BUG *=(.*)', line)
      if match:
        for i in match.group(1).split(','):
          entries.extend(filter(None, [x.strip() for x in i.split()]))

    # Try to parse the bugs.  Handle lots of different formats:
    # - The whole URL, from which we parse the project and bug.
    # - A simple string that looks like "project:bug"
    # - A string that looks like "bug", which will always refer to the previous
    #   tracker referenced (defaulting to the default tracker).
    #
    # We will create an "Issue" object for each bug.
    issues = []
    last_tracker = DEFAULT_TRACKER
    regex = (r'http://code.google.com/p/(\S+)/issues/detail\?id=([0-9]+)'
             r'|(\S+):([0-9]+)|(\b[0-9]+\b)')

    for new_item in entries:
      bug_numbers = re.findall(regex, new_item)
      for bug_tuple in bug_numbers:
        if bug_tuple[0] and bug_tuple[1]:
          issues.append(Issue(bug_tuple[0], bug_tuple[1], self._tracker_acc))
          last_tracker = bug_tuple[0]
        elif bug_tuple[2] and bug_tuple[3]:
          issues.append(Issue(bug_tuple[2], bug_tuple[3], self._tracker_acc))
          last_tracker = bug_tuple[2]
        elif bug_tuple[4]:
          issues.append(Issue(last_tracker, bug_tuple[4], self._tracker_acc))

    # Sort the issues and return...
    issues.sort()
    return issues

  def AsHTMLTableRow(self):
    """Returns HTML for this change, for printing as part of a table.

    Columns: Project, Date, Commit, Committer, Bugs, Subject.

    Returns:
      A string usable as an HTML table row, like:

      <tr><td>Blah</td><td>Blah blah</td></tr>
    """

    bugs = []
    link_fmt = '<a href="%s">%s</a>'
    for issue in self._issues:
      bugs.append(link_fmt % (issue.GetUrl(), str(issue)))

    url_fmt = 'http://chromiumos-git/git/?p=%s.git;a=commitdiff;h=%s'
    url = url_fmt % (self.projectname, self.commit)
    commit_desc = link_fmt % (url, self.commit[:8])
    bug_str = '<br>'.join(bugs)
    if not bug_str:
      if (self.projectname == 'kernel-next' or
          self.commit_email == 'chrome-bot@chromium.org'):
        bug_str = 'not needed'
      else:
        bug_str = '<font color="red">none</font>'

    cols = [
        cgi.escape(self.projectname),
        str(self.commit_date),
        commit_desc,
        cgi.escape(self.commit_email),
        bug_str,
        cgi.escape(self.subject[:100]),
    ]
    return '<tr><td>%s</td></tr>' % ('</td><td>'.join(cols))

  def __cmp__(self, other):
    """Compare two Commit objects first by project name, then by date."""
    return (cmp(self.projectname, other.projectname) or
            cmp(self.commit_date, other.commit_date))


def _GrabChanges(path, tag1, tag2, tracker_acc):
  """Return list of commits to path between tag1 and tag2.

  Args:
    path: One of the directories managed by repo.
    tag1: The first of the two tags to pass to git log.
    tag2: The second of the two tags to pass to git log.
    tracker_acc: A tracker_access.TrackerAccess object.

  Returns:
    A list of "Commit" objects.
  """

  cmd = 'cd %s && git config --get remote.cros.projectname' % path
  projectname = _GrabOutput(cmd).strip()
  log_fmt = '%x00%H\t%ce\t%cd\t%s\t%b'
  cmd_fmt = 'cd %s && git log --format="%s" --date=local "%s..%s"'
  cmd = cmd_fmt % (path, log_fmt, tag1, tag2)
  output = _GrabOutput(cmd)
  commits = []
  for log_data in output.split('\0')[1:]:
    commit, commit_email, commit_date, subject, body = log_data.split('\t', 4)
    change = Commit(commit, projectname, commit_email, commit_date, subject,
                    body, tracker_acc)
    commits.append(change)
  return commits


def _ParseArgs(argv):
  """Parse command-line arguments.

  Returns:
    An optparse.OptionParser object.
  """
  parser = optparse.OptionParser()
  parser.add_option(
      '--sort-by-date', dest='sort_by_date', default=False,
      action='store_true', help='Sort commits by date.')
  parser.add_option(
      '--tracker-user', dest='tracker_user', default=None,
      help='Specify a username to login to code.google.com.')
  parser.add_option(
      '--tracker-pass', dest='tracker_pass', default=None,
      help='Specify a password to go w/ user.')
  parser.add_option(
      '--tracker-passfile', dest='tracker_passfile', default=None,
      help='Specify a file containing a password to go w/ user.')
  return parser.parse_args(argv)


def main(argv):
  tags = _GrabTags()
  tag1 = None
  options, args = _ParseArgs(argv)
  if len(args) == 2:
    tag1, tag2 = args
  elif len(args) == 1:
    tag2, = args
    if tag2 in tags:
      tag2_index = tags.index(tag2)
      if tag2_index == len(tags) - 1:
        print >>sys.stderr, 'No previous tag for %s' % tag2
        sys.exit(1)
      tag1 = tags[tag2_index + 1]
    else:
      print >>sys.stderr, 'Unrecognized tag: %s' % tag2
      sys.exit(1)
  else:
    print >>sys.stderr, 'Usage: %s [tag1] tag2' % sys.argv[0]
    print >>sys.stderr, 'If only one tag is specified, we view the differences'
    print >>sys.stderr, 'between that tag and the previous tag. You can also'
    print >>sys.stderr, 'specify cros/master to show differences with'
    print >>sys.stderr, 'tip-of-tree.'
    print >>sys.stderr, 'E.g. %s %s cros/master' % (sys.argv[0], tags[0])
    sys.exit(1)

  if options.tracker_user is not None:
    # TODO(dianders): Once we install GData automatically, move the import
    # to the top of the file where it belongs.  It's only here to allow
    # people to run the script without GData.
    try:
      import tracker_access
    except ImportError:
      print >>sys.stderr, INSTRS_FOR_GDATA
      sys.exit(1)
    if options.tracker_passfile is not None:
      options.tracker_pass = open(options.tracker_passfile, 'r').read().strip()
    tracker_acc = tracker_access.TrackerAccess(options.tracker_user,
                                               options.tracker_pass)
  else:
    tracker_acc = None

  print >>sys.stderr, 'Finding differences between %s and %s' % (tag1, tag2)
  paths = _GrabDirs()
  changes = []
  for path in paths:
    changes.extend(_GrabChanges(path, tag1, tag2, tracker_acc))

  title = 'Changelog for %s to %s' % (tag1, tag2)
  print '<html>'
  print '<head><title>%s</title></head>' % title
  print '<h1>%s</h1>' % title
  cols = ['Project', 'Date', 'Commit', 'Committer', 'Bugs', 'Subject']
  print '<table border="1" cellpadding="4">'
  print '<tr><th>%s</th>' % ('</th><th>'.join(cols))
  if options.sort_by_date:
    changes.sort(key=operator.attrgetter('commit_date'))
  else:
    changes.sort()
  for change in changes:
    print change.AsHTMLTableRow()
  print '</table>'
  print '</html>'
