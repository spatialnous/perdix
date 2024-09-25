# SPDX-FileCopyrightText: 2014 - 2015 Jorge Gil <jorge.gil@ucl.ac.uk>
# SPDX-FileCopyrightText: 2014 - 2015 UCL
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
# 
# SPDX-License-Identifier: GPL-2.0-or-later

import os
from builtins import str

from qgis.PyQt import QtWidgets, uic

from perdix.utilities import utility_functions as uf

Ui_VerificationSettingsDialog, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'verification_settings_dialog.ui'))

class VerificationSettingsDialog(QtWidgets.QDialog, Ui_VerificationSettingsDialog):
    def __init__(self, settings):
        QtWidgets.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)

        # internal GUI signals
        self.axialThresholdEdit.editingFinished.connect(self.checkSettingsValues)
        self.axialMinimumEdit.editingFinished.connect(self.checkSettingsValues)
        self.unlinksThresholdEdit.editingFinished.connect(self.checkSettingsValues)
        self.linksThresholdEdit.editingFinished.connect(self.checkSettingsValues)
        self.closeButtonBox.accepted.connect(self.updateSettings)
        self.closeButtonBox.rejected.connect(self.restoreSettings)

        # hide unused UI buttons
        self.linksThresholdLabel.hide()
        self.linksThresholdEdit.hide()

        #
        self.ok = self.closeButtonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.settings = settings
        self.restoreSettings()

    def checkSettingsValues(self):
        ax_min = self.axialMinimumEdit.text()
        ax_dist = self.axialThresholdEdit.text()
        unlink_dist = self.unlinksThresholdEdit.text()
        link_dist = self.linksThresholdEdit.text()
        if uf.isNumeric(ax_min) and uf.isNumeric(ax_dist) and uf.isNumeric(unlink_dist) and uf.isNumeric(link_dist):
            self.ok.setDisabled(False)
        else:
            self.ok.setToolTip("Check if the settings values are correct.")
            self.ok.setDisabled(True)

    def restoreSettings(self):
        self.axialThresholdEdit.setText(str(self.settings['ax_dist']))
        self.axialMinimumEdit.setText(str(self.settings['ax_min']))
        self.unlinksThresholdEdit.setText(str(self.settings['unlink_dist']))
        self.linksThresholdEdit.setText(str(self.settings['link_dist']))

    def updateSettings(self):
        self.settings['ax_dist'] = float(self.axialThresholdEdit.text())
        self.settings['ax_min'] = float(self.axialMinimumEdit.text())
        self.settings['unlink_dist'] = float(self.unlinksThresholdEdit.text())
        self.settings['link_dist'] = float(self.linksThresholdEdit.text())
