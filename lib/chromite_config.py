# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Manage various ~/.config/chromite/ configuration files."""

from pathlib import Path
import sys


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


DIR = Path('~/.config/chromite').expanduser()

# List of configs that we might use.  Normally this would be declared in the
# respective modules that actually use the config file, but having the list be
# here helps act as a clearing house and get a sense of project-wide naming
# conventions, and to try and prevent conflicts.

CHROME_SDK_BASHRC = DIR / 'chrome_sdk.bashrc'


def initialize():
  """Initialize the config dir for use.

  Code does not need to invoke this all the time, but can be helpful when
  creating new config files with default content.
  """
  DIR.mkdir(mode=0o755, parents=True, exist_ok=True)
