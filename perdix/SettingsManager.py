# SPDX-FileCopyrightText: 2014 - 2015 Jorge Gil <jorge.gil@ucl.ac.uk>
# SPDX-FileCopyrightText: 2014 - 2015 UCL
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

import os

# Import the PyQt and QGIS libraries
from qgis.PyQt.QtCore import QObject, QSettings, QFileInfo
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.uic import loadUiType

Ui_SettingsDialog, _ = loadUiType(
    os.path.join(os.path.dirname(__file__), "ui", "settings_dialog.ui")
)


class SettingsManager(QObject):
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface
        self.dlg = SettingsDialog()

    def showDialog(self):
        self.dlg.show()

    def getLastDir(self):
        settings = QSettings()
        return settings.value("/esst/lastUsedDir", "")

    def setLastDir(self, path):
        settings = QSettings()
        save_path = QFileInfo(path).filePath()
        settings.setValue("/esst/lastUsedDir", save_path)


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)
        # set up internal GUI signals
        self.closeButtonBox.rejected.connect(self.close)
