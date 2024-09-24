# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later

#/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
cd ../

echo "- Utility Function tests"
./perdix/tests/runtest_macos.sh perdix.tests.test_utility_functions
echo "- Gate Transformer tests"
./perdix/tests/runtest_macos.sh perdix.tests.test_gate_transformer
echo "- Network Segmenter tests"
./perdix/tests/runtest_macos.sh perdix.tests.test_segmenter
echo "- Road Centerline Cleaner tests"
./perdix/tests/runtest_macos.sh perdix.tests.test_rcl_cleaner