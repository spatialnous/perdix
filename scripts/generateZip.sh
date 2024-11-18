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

NAME_PATT="name=.*"
NAME=$(sed -n 's/^name= *//p' ../perdix/metadata.txt)
NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]')

# Get the number of commits after the last change of the version line
VERSION_PATT="version=.*"
LINE_NUMBER=$(sed -n "/$VERSION_PATT/=" metadata.txt)
LAST_VERSION_HASH=$(git log -s -1 --format=format:%H -L $LINE_NUMBER,$LINE_NUMBER:metadata.txt)
COMMITS_SINCE_LAST_VERSION=$(git rev-list $LAST_VERSION_HASH.. --count)

# Create a zip file archive from zip
git archive --format zip -o $DIR/.generated/$NAME.zip --prefix=perdix/ HEAD

# Unzip the file to /tmp, modify the metadata.txt (append the number of commits
# to the version) and update the zip
rm -rf /tmp/perdix
mkdir -p /tmp/perdix
unzip $DIR/.generated/$NAME.zip perdix/metadata.txt -d /tmp/perdix/

cd /tmp/perdix/perdix
sed -i "s/$VERSION_PATT/&.$COMMITS_SINCE_LAST_VERSION/g" metadata.txt

cd ..
zip --update "$DIR/.generated/perdix.zip" "perdix/metadata.txt" 
