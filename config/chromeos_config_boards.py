# -*- coding: utf-8 -*-
# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Configuration options for cbuildbot boards."""

from __future__ import print_function

#
# Define assorted constants describing various sets of boards.
#

# Base per-board configuration.
# Every board must appear in exactly 1 of the following sets.

#
# Define assorted constants describing various sets of boards.
#

# Base per-board configuration.
# Every board must appear in exactly 1 of the following sets.

arm_internal_release_boards = frozenset([
    'arkham',
    'beaglebone',
    'beaglebone_servo',
    'capri-zfpga',
    'gale',
    'kevin-arc64',
    'littlejoe',
    'nyan_big',
    'nyan_blaze',
    'oak',
    'tael',
    'veyron_jaq',
    'veyron_jerry',
    'veyron_mighty',
    'veyron_minnie',
    'veyron_rialto',
    'veyron_speedy',
    'viking',
    'viking-poc2',
    'whirlwind',
])

arm_external_boards = frozenset([
    'arm-generic',
    'arm64-generic',
    'arm64-llvmpipe',
])

x86_internal_release_boards = frozenset([
    'deltaur',
    'falco_li',
    'glados',
    'guado_labstation',
    'guybrush',
    'jecht',
    'lakitu',
    'majolica',
    'mancomb',
    'monroe',
    'poppy',
    'samus-kernelnext',
    'sludge',
    'tatl',
    'wristpin',
])

x86_external_boards = frozenset([
    'amd64-generic',
    'moblab-generic-vm',
    'x32-generic',
])

# Board can appear in 1 or more of the following sets.
brillo_boards = frozenset([
    'arkham',
    'gale',
    'mistral',
    'whirlwind',
])

accelerator_boards = frozenset([
    'fizz-accelerator',
])

beaglebone_boards = frozenset([
    'beaglebone',
    'beaglebone_servo',
])

dustbuster_boards = frozenset([
    'wristpin',
])

lakitu_boards = frozenset([
    'lakitu',
])

lassen_boards = frozenset([
    'lassen',
])

loonix_boards = frozenset([
    'capri',
    'capri-zfpga',
    'cobblepot',
    'gonzo',
    'lasilla-ground',
    'octavius',
    'romer',
    'wooten',
])

reven_boards = frozenset([
    'reven',
])

wshwos_boards = frozenset([
    'littlejoe',
    'viking',
    'viking-poc2',
])

moblab_boards = frozenset([
    'puff-moblab',
    'fizz-moblab',
    'moblab-generic-vm',
])

scribe_boards = frozenset([
    'guado-macrophage',
    'puff-macrophage',
])

termina_boards = frozenset([
    'sludge',
    'tatl',
    'tael',
])

nofactory_boards = (
    lakitu_boards | termina_boards | lassen_boards | reven_boards | frozenset([
        'x30evb',
    ])
)

toolchains_from_source = frozenset([
    'x32-generic',
])

noimagetest_boards = (lakitu_boards | loonix_boards | termina_boards
                      | scribe_boards | wshwos_boards | dustbuster_boards)

nohwqual_boards = (lakitu_boards | lassen_boards | loonix_boards
                   | termina_boards | beaglebone_boards | wshwos_boards
                   | dustbuster_boards | reven_boards)

base_layout_boards = lakitu_boards | termina_boards

builder_incompatible_binaries_boards = frozenset([
    'grunt',
    'grunt-arc-r',
    'zork',
    'zork-borealis',
])
