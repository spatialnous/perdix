# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later

#/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
cd ../perdix/
git archive --format zip -o $DIR/perdix.zip --prefix=perdix/ HEAD