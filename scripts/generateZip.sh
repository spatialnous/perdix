# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2020 Space Syntax Ltd.
# SPDX-FileCopyrightText: 2024 - 2026 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

#/bin/sh

IS_LTR="$1"
PRJ_NAME="perdix"
PRJ_LABEL="Perdix"
OUT_NAME="${PRJ_NAME}"
if [ -n "$IS_LTR" ]; then
    OUT_NAME="${PRJ_NAME}-ltr"
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
mkdir -p .generated
cd ../${PRJ_NAME}/

NAME_PATT="name=.*"
NAME=$(sed -n 's/^name= *//p' ../${PRJ_NAME}/metadata.txt)
NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]')

# Get the number of commits after the last change of the version line
VERSION_PATT="version=.*"
LINE_NUMBER=$(sed -n "/$VERSION_PATT/=" metadata.txt)
LAST_VERSION_HASH=$(git log -s -1 --format=format:%H -L $LINE_NUMBER,$LINE_NUMBER:metadata.txt)
COMMITS_SINCE_LAST_VERSION=$(git rev-list $LAST_VERSION_HASH.. --count)

# Create a zip file archive from zip
git archive --format zip -o $DIR/.generated/$OUT_NAME.zip --prefix="${OUT_NAME}"/ HEAD

# Unzip the file to /tmp, modify the metadata.txt (append the number of commits
# to the version) and update the zip
rm -rf /tmp/${PRJ_NAME}
mkdir -p /tmp/${PRJ_NAME}
unzip $DIR/.generated/$OUT_NAME.zip ${OUT_NAME}/metadata.txt -d /tmp/${PRJ_NAME}/

cd /tmp/${PRJ_NAME}/${OUT_NAME}
sed -i "s/$VERSION_PATT/&.$COMMITS_SINCE_LAST_VERSION/g" metadata.txt
if [ -n "$IS_LTR" ]; then
    sed -i "s/^name=$PRJ_LABEL$/&-ltr/" metadata.txt
    grep -q 'Version compatible with QGIS Long-term support version.' metadata.txt || \
        sed -i 's/^description=.*/& Version compatible with QGIS Long-term support version./' metadata.txt
fi

cd ..
zip --update "$DIR/.generated/$OUT_NAME.zip" "${OUT_NAME}/metadata.txt"
