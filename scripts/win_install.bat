REM SPDX-FileCopyrightText: 2019 Ioanna Kolovou <i.kolovou@spacesyntax.com>
REM SPDX-FileCopyrightText: 2019 Space Syntax Limited

REM SPDX-License-Identifier: GPL-2.0-or-later

@ECHO OFF

REM Path variables
set qgis_user_dir=%UserProfile%\.qgis2
set rcl_plugin_dir=%qgis_user_dir%\python\plugins\perdix

REM Make sure QGIS is installed
IF NOT EXIST %qgis_user_dir% (
	ECHO ERROR: QGIS not found.
	GOTO FAILURE
)

REM Remove potential previously installed plugin
IF EXIST "%rcl_plugin_dir%" (
	ECHO Removing currently installed Perdix QGIS plugin...
	rmdir "%rcl_plugin_dir%" /s /q
	IF EXIST "%rcl_plugin_dir%" (
		ECHO ERROR: Couldn't remove currently installed Perdix QGIS plugin.
		ECHO Please close QGIS if it is running, and then try installing again.
		GOTO FAILURE
	)
)

ECHO Copying Perdix QGIS plugin to QGIS plugin directory...
xcopy "%~dp0*.*" "%rcl_plugin_dir%\" /syq
REM NOTE: The test below tests errorlevel >= 1, not errorlevel == 1
IF ERRORLEVEL 1 (
	ECHO ERROR: Couldn't copy files "%~dp0*.*" to "%rcl_plugin_dir%\"
	GOTO FAILURE
)

ECHO.
ECHO Perdix QGIS plugin was successfully installed!
ECHO Please see readme.txt for instructions on how to enable it.
ECHO.
PAUSE
EXIT

:FAILURE
ECHO Perdix QGIS plugin was NOT installed.
ECHO.
PAUSE