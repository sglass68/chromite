# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Utilities for requesting information for a gerrit server via https.

https://gerrit-review.googlesource.com/Documentation/rest-api.html
"""

import base64
import httplib
import json
import logging
import netrc
import os
import time
import urllib
from cStringIO import StringIO

try:
  NETRC = netrc.netrc()
except (IOError, netrc.NetrcParseError):
  NETRC = netrc.netrc(os.devnull)
LOGGER = logging.getLogger()
TRY_LIMIT = 5

# Controls the transport protocol used to communicate with gerrit.
# This is parameterized primarily to enable cros_test_lib.GerritTestCase.
GERRIT_PROTOCOL = 'https'


class GOBError(Exception):
  """Exception class for errors commuicating with the gerrit-on-borg service."""
  def __init__(self, http_status, *args, **kwargs):
    super(GOBError, self).__init__(*args, **kwargs)
    self.http_status = http_status
    self.message = '(%d) %s' % (self.http_status, self.message)


def _QueryString(param_dict, first_param=None):
  """Encodes query parameters in the key:val[+key:val...] format specified here:

  https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes
  """
  q = [urllib.quote(first_param)] if first_param else []
  q.extend(['%s:%s' % (key, val) for key, val in param_dict.iteritems()])
  return '+'.join(q)


def CreateHttpConn(host, path, reqtype='GET', headers=None, body=None):
  """Opens an https connection to a gerrit service, and sends a request."""
  headers = headers or {}
  bare_host = host.partition(':')[0]
  auth = NETRC.authenticators(bare_host)
  if auth:
    headers.setdefault('Authorization', 'Basic %s' % (
        base64.b64encode('%s:%s' % (auth[0], auth[2]))))
  else:
    LOGGER.debug('No authorization found')
  if body:
    body = json.JSONEncoder().encode(body)
    headers.setdefault('Content-Type', 'application/json')
  if LOGGER.isEnabledFor(logging.DEBUG):
    LOGGER.debug('%s %s://%s/a/%s' % (reqtype, GERRIT_PROTOCOL, host, path))
    for key, val in headers.iteritems():
      if key == 'Authorization':
        val = 'HIDDEN'
      LOGGER.debug('%s: %s' % (key, val))
    if body:
      LOGGER.debug(body)
  conn = httplib.HTTPSConnection(host)
  conn.req_host = host
  conn.req_params = {
      'url': '/a/%s' % path,
      'method': reqtype,
      'headers': headers,
      'body': body,
  }
  conn.request(**conn.req_params)
  return conn


def ReadHttpResponse(conn, ignore_404=True):
  """Reads an http response from a connection into a string buffer.

  Args:
    conn: An HTTPSConnection created by CreateHttpConn, above.
    ignore_404: For many requests, gerrit-on-borg will return 404 if the request
                doesn't match the database contents.  In most such cases, we
                want the API to return None rather than raise an Exception.

  Returns:
    A string buffer containing the connection's reply.
  """

  sleep_time = 0.5
  for idx in range(TRY_LIMIT):
    response = conn.getresponse()
    # If response.status < 500 then the result is final; break retry loop.
    if response.status < 500:
      break
    # A status >=500 is assumed to be a possible transient error; retry.
    http_version = 'HTTP/%s' % ('1.1' if response.version == 11 else '1.0')
    msg = (
        'A transient error occured while querying %s:\n'
        '%s %s %s\n'
        '%s %d %s' % (
            conn.host, conn.req_params['method'], conn.req_params['url'],
            http_version, http_version, response.status, response.reason))
    if TRY_LIMIT - idx > 1:
      msg += '\n... will retry %d more times.' % (TRY_LIMIT - idx - 1)
      time.sleep(sleep_time)
      sleep_time = sleep_time * 2
      req_host = conn.req_host
      req_params = conn.req_params
      conn = httplib.HTTPSConnection(req_host)
      conn.req_host = req_host
      conn.req_params = req_params
      conn.request(**req_params)
    LOGGER.warn(msg)
  if ignore_404 and response.status == 404:
    return StringIO()
  if response.status != 200:
    raise GOBError(response.status, response.reason)
  return StringIO(response.read())


def ReadHttpJsonResponse(conn, ignore_404=True):
  """Parses an https response as json."""
  fh = ReadHttpResponse(conn, ignore_404=ignore_404)
  # The first line of the response should always be: )]}'
  s = fh.readline()
  if s and s.rstrip() != ")]}'":
    raise GOBError(200, 'Unexpected json output: %s' % s)
  s = fh.read()
  if not s:
    return None
  return json.loads(s)


def QueryChanges(host, param_dict, first_param=None, limit=None, o_params=None,
                 sortkey=None):
  """Queries a gerrit-on-borg server for changes matching query terms.

  Args:
    param_dict: A dictionary of search parameters, as documented here:
        http://gerrit-documentation.googlecode.com/svn/Documentation/2.6/user-search.html
    first_param: A change identifier
    limit: Maximum number of results to return.
    o_params: A list of additional output specifiers, as documented here:
        https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes

  Returns:
    A list of json-decoded query results.
  """
  # Note that no attempt is made to escape special characters; YMMV.
  if not param_dict and not first_param:
    raise RuntimeError('QueryChanges requires search parameters')
  path = 'changes/?q=%s' % _QueryString(param_dict, first_param)
  if sortkey:
    path = '%s&N=%s' % (path, sortkey)
  if limit:
    path = '%s&n=%d' % (path, limit)
  if o_params:
    path = '%s&%s' % (path, '&'.join(['o=%s' % p for p in o_params]))
  # Don't ignore 404; a query should always return a list, even if it's empty.
  return ReadHttpJsonResponse(CreateHttpConn(host, path), ignore_404=False)


def MultiQueryChanges(host, param_dict, change_list, limit=None, o_params=None,
                      sortkey=None):
  """Initiate a query composed of multiple sets of query parameters."""
  if not change_list:
    raise RuntimeError(
        "MultiQueryChanges requires a list of change numbers/id's")
  q = ['q=%s' % '+OR+'.join([urllib.quote(str(x)) for x in change_list])]
  if param_dict:
    q.append(_QueryString(param_dict))
  if limit:
    q.append('n=%d' % limit)
  if sortkey:
    q.append('N=%s' % sortkey)
  if o_params:
    q.extend(['o=%s' % p for p in o_params])
  path = 'changes/?%s' % '&'.join(q)
  try:
    result = ReadHttpJsonResponse(CreateHttpConn(host, path), ignore_404=False)
  except GOBError as e:
    msg = '%s:\n%s' % (e.message, path)
    raise GOBError(e.http_status, msg)
  return result


def GetGerritFetchUrl(host):
  """Given a gerrit host name returns URL of a gerrit instance to fetch from."""
  return '%s://%s/' % (GERRIT_PROTOCOL, host)


def GetChangePageUrl(host, change_number):
  """Given a gerrit host name and change number, return change page url."""
  return '%s://%s/#/c/%d/' % (GERRIT_PROTOCOL, host, change_number)


def GetChangeUrl(host, change):
  """Given a gerrit host name and change id, return an url for the change."""
  return '%s://%s/a/changes/%s' % (GERRIT_PROTOCOL, host, change)


def GetChange(host, change):
  """Query a gerrit server for information about a single change."""
  path = 'changes/%s' % change
  return ReadHttpJsonResponse(CreateHttpConn(host, path))


def GetChangeReview(host, change, revision='current'):
  """Get the current review information for a change."""
  path = 'changes/%s/revisions/%s/review' % (change, revision)
  return ReadHttpJsonResponse(CreateHttpConn(host, path))


def GetChangeCommit(host, change, revision='current'):
  """Get the current review information for a change."""
  path = 'changes/%s/revisions/%s/commit' % (change, revision)
  return ReadHttpJsonResponse(CreateHttpConn(host, path))


def GetChangeCurrentRevision(host, change):
  """Get information about the latest revision for a given change."""
  jmsg = GetChangeReview(host, change)
  if jmsg:
    return jmsg.get('current_revision')


def GetChangeDetail(host, change, o_params=None):
  """Query a gerrit server for extended information about a single change."""
  path = 'changes/%s/detail' % change
  if o_params:
    path = '%s?%s' % (path, '&'.join(['o=%s' % p for p in o_params]))
  return ReadHttpJsonResponse(CreateHttpConn(host, path))


def GetChangeReviewers(host, change):
  """Get information about all reviewers attached to a change."""
  path = 'changes/%s/reviewers' % change
  return ReadHttpJsonResponse(CreateHttpConn(host, path))


def AbandonChange(host, change, msg=''):
  """Abandon a gerrit change."""
  path = 'changes/%s/abandon' % change
  body = {'message': msg} if msg else None
  conn = CreateHttpConn(host, path, reqtype='POST', body=body)
  return ReadHttpJsonResponse(conn, ignore_404=False)


def RestoreChange(host, change, msg=''):
  """Restore a previously abandoned change."""
  path = 'changes/%s/restore' % change
  body = {'message': msg} if msg else None
  conn = CreateHttpConn(host, path, reqtype='POST', body=body)
  return ReadHttpJsonResponse(conn, ignore_404=False)


def SubmitChange(host, change, wait_for_merge=True):
  """Submits a gerrit change via Gerrit."""
  path = 'changes/%s/submit' % change
  body = {'wait_for_merge': wait_for_merge}
  conn = CreateHttpConn(host, path, reqtype='POST', body=body)
  return ReadHttpJsonResponse(conn, ignore_404=False)


def GetReviewers(host, change):
  """Get information about all reviewers attached to a change."""
  path = 'changes/%s/reviewers' % change
  return ReadHttpJsonResponse(CreateHttpConn(host, path))


def AddReviewers(host, change, add=None):
  """Add reviewers to a change."""
  if not add:
    return
  if isinstance(add, basestring):
    add = (add,)
  path = 'changes/%s/reviewers' % change
  for r in add:
    body = {'reviewer': r}
    conn = CreateHttpConn(host, path, reqtype='POST', body=body)
    jmsg = ReadHttpJsonResponse(conn, ignore_404=False)
  return jmsg


def RemoveReviewers(host, change, remove=None):
  """Remove reveiewers from a change."""
  if not remove:
    return
  if isinstance(remove, basestring):
    remove = (remove,)
  for r in remove:
    path = 'changes/%s/reviewers/%s' % (change, r)
    conn = CreateHttpConn(host, path, reqtype='DELETE')
    try:
      ReadHttpResponse(conn, ignore_404=False)
    except GOBError as e:
      # On success, gerrit returns status 204; anything else is an error.
      if e.http_status != 204:
        raise
    else:
      raise GOBError(
          'Unexpectedly received a 200 http status while deleting reviewer "%s"'
          ' from change %s' % (r, change))


def SetReview(host, change, revision='current', msg=None, labels=None,
              notify=None):
  """Set labels and/or add a message to a code review."""
  if not msg and not labels:
    return
  path = 'changes/%s/revisions/%s/review' % (change, revision)
  body = {}
  if msg:
    body['message'] = msg
  if labels:
    body['labels'] = labels
  if notify:
    body['notify'] = notify
  conn = CreateHttpConn(host, path, reqtype='POST', body=body)
  response = ReadHttpJsonResponse(conn)
  if labels:
    for key, val in labels.iteritems():
      if ('labels' not in response or key not in response['labels'] or
          int(response['labels'][key] != int(val))):
        raise GOBError(200, 'Unable to set "%s" label on change %s.' % (
            key, change))


def ResetReviewLabels(host, change, label, value='0', revision='current',
                      message=None, notify=None):
  """Reset the value of a given label for all reviewers on a change."""
  # This is tricky when working on the "current" revision, because there's
  # always the risk that the "current" revision will change in between API
  # calls.  So, the code dereferences the "current" revision down to a literal
  # sha1 at the beginning and uses it for all subsequent calls.  As a sanity
  # check, the "current" revision is dereferenced again at the end, and if it
  # differs from the previous "current" revision, an exception is raised.
  current = (revision == 'current')
  jmsg = GetChangeDetail(
      host, change, o_params=['CURRENT_REVISION', 'CURRENT_COMMIT'])
  if current:
    revision = jmsg['current_revision']
  value = str(value)
  path = 'changes/%s/revisions/%s/review' % (change, revision)
  message = message or (
      '%s label set to %s programmatically by chromite.' % (label, value))
  for review in jmsg.get('labels', {}).get(label, {}).get('all', []):
    if str(review.get('value', value)) != value:
      body = {
          'message': message,
          'labels': {label: value},
          'on_behalf_of': review['_account_id'],
      }
      if notify:
        body['notify'] = notify
      conn = CreateHttpConn(host, path, reqtype='POST', body=body)
      response = ReadHttpJsonResponse(conn)
      if str(response['labels'][label]) != value:
        username = review.get('email', jmsg.get('name', ''))
        raise GOBError(200, 'Unable to set %s label for user "%s"'
                       ' on change %s.' % (label, username, change))
  if current:
    new_revision = GetChangeCurrentRevision(host, change)
    if not new_revision:
      raise GOBError(
          200, 'Could not get review information for change "%s"' % change)
    elif new_revision != revision:
      raise GOBError(200, 'While resetting labels on change "%s", '
                     'a new patchset was uploaded.' % change)
