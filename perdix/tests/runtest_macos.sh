# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later

#!/bin/sh
# -*- coding: utf-8 -*-

# This script is provided as a helper to run the tests. While it is placed in the tests directory,
# it should be called from the perdix directory and a test provided as a module argument:
# ./tests/runtest_macos.sh tests.test_utility_functions

QGISPATH="/Applications/QGIS3.10.app"
export PYTHONPATH="${PYTHONPATH}:${QGISPATH}/Contents/Resources/python/"
export QT_QPA_PLATFORM_PLUGIN_PATH="${QGISPATH}/Contents/PlugIns"
${QGISPATH}/Contents/MacOS/bin/python3 -m $1
