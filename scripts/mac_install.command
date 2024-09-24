# SPDX-FileCopyrightText: 2019 Ioanna Kolovou <i.kolovou@spacesyntax.com>
# SPDX-FileCopyrightText: 2019 Space Syntax Limited
# 
# SPDX-License-Identifier: GPL-2.0-or-later

# Script for installing Perdix plugin for QGIS on Mac OS/X

# Path variables
qgis_user_dir=~/.qgis2
rcl_plugin_dir=$qgis_user_dir/python/plugins/perdix

# Make sure QGIS is installed
if [ ! -d "$qgis_user_dir" ]; then
	echo "ERROR: QGIS not found."
	exit 1
fi

# Remove previously installed plugin
if [ -d "$rcl_plugin_dir" ]; then
	echo "Removing currently installed Perdix QGIS plugin..."
	rm -rf "$rcl_plugin_dir"
	if [ $? -ne 0 ]; then
		echo "ERROR: Couldn't remove currently installed Perdix QGIS plugin."
		echo "Please close QGIS if it is running, and then try installing again."
		exit 1
	fi
fi

if [ ! -d "$rcl_plugin_dir" ]; then
	mkdir -p "$rcl_plugin_dir"
	if [ $? -ne 0 ]; then
		echo "ERROR: Couldn't create directory '$rcl_plugin_dir'"
		exit 1
	fi
fi

echo "Copying Perdix QGIS plugin to QGIS plugin directory..."
dir=${0%/*}
echo $dir 
cp -r $dir/* "$rcl_plugin_dir/"
if [ $? -ne 0 ]; then
	echo "ERROR: Couldn't copy 'perdix' to '$rcl_plugin_dir/'"
	exit 1
fi

echo "Perdix QGIS plugin was successfully installed!"
echo "Please see readme.txt for instructions on how to enable it."
exit 0
