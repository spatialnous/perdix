# SPDX-FileCopyrightText: 2019 Ioanna Kolovou <i.kolovou@spacesyntax.com>
# SPDX-FileCopyrightText: 2019 Space Syntax Limited
# 
# SPDX-License-Identifier: GPL-2.0-or-later

# Script for uninstalling Perdix plugin for QGIS on Mac OS/X

# Path variables
rcl_plugin_dir=~/.qgis2/python/plugins/perdix

# Make sure QGIS is installed
if [ ! -d "$rcl_plugin_dir" ]; then
	echo "Perdix QGIS plugin not found."
	exit 1
fi

rm -rf "$rcl_plugin_dir"
if [ $? -ne 0 ]; then
	echo "ERROR: Couldn't remove currently installed Perdix QGIS plugin."
	echo "Please close QGIS if it is running, and then try again."
	exit 1
fi

echo "Perdix QGIS plugin was successfully uninstalled."
