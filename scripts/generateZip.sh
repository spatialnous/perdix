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

# Get the number of commits after the last change of the version line
PATT="version=.*"
LINE_NUMBER=$(sed -n "/$PATT/=" metadata.txt)
LAST_VERSION_HASH=$(git log -s -1 --format=format:%H -L $LINE_NUMBER,$LINE_NUMBER:metadata.txt)
COMMITS_SINCE_LAST_VERSION=$(git rev-list $LAST_VERSION_HASH.. --count)

# Create a zip file archive from zip
git archive --format zip -o $DIR/.generated/perdix.zip --prefix=perdix/ HEAD

# Unzip the file to /tmp, modify the metadata.txt (append the number of commits
# to the version) and update the zip
rm -rf /tmp/perdix
mkdir -p /tmp/perdix
unzip $DIR/.generated/perdix.zip perdix/metadata.txt -d /tmp/perdix/

cd /tmp/perdix/perdix
sed -i "s/$PATT/&.$COMMITS_SINCE_LAST_VERSION/g" metadata.txt

cd ..
zip --update "$DIR/.generated/perdix.zip" "perdix/metadata.txt" 
