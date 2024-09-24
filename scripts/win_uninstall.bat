REM SPDX-FileCopyrightText: 2019 Ioanna Kolovou <i.kolovou@spacesyntax.com>
REM SPDX-FileCopyrightText: 2019 Space Syntax Limited

REM SPDX-License-Identifier: GPL-2.0-or-later

@ECHO OFF

set rcl_plugin_dir=%UserProfile%\.qgis2\python\plugins\perdix

IF NOT EXIST "% rcl_plugin_dir%" (
	ECHO Perdix QGIS plugin not found.
	PAUSE
	EXIT
)

rmdir "%rcl_plugin_dir%" /s /q
IF EXIST "% rcl_plugin_dir%" (
	ECHO ERROR: Couldn't remove currently installed Perdix QGIS plugin.
	ECHO Please close QGIS if it is running, and then try again.
	PAUSE
	EXIT
)

ECHO Perdix QGIS plugin was successfully uninstalled.
ECHO.
PAUSE