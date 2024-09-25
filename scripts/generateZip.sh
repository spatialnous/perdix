# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2020 Space Syntax Ltd.
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

#/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
mkdir -p .generated
cd ../perdix/
git archive --format zip -o $DIR/.generated/perdix.zip --prefix=perdix/ HEAD