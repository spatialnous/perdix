# SPDX-FileCopyrightText: 2014 - 2015 Jorge Gil <jorge.gil@ucl.ac.uk>
# SPDX-FileCopyrightText: 2014 - 2015 UCL
#
# SPDX-License-Identifier: GPL-2.0-or-later

from builtins import str

from qgis.PyQt import QtWidgets

from perdix.analysis.engines.DepthmapNet.ui_DepthmapAdvanced import Ui_DepthmapAdvancedDialog

class DepthmapAdvancedDialog(QtWidgets.QDialog, Ui_DepthmapAdvancedDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)

        # internal GUI signals
        self.axialDistanceCombo.currentIndexChanged.connect(self.setDistanceType)
        self.axialRadiusCombo.currentIndexChanged.connect(self.setRadiusType)
        self.axialStubsEdit.editingFinished.connect(self.checkRemoveStubs)

        # hide unused UI buttons
        self.axialDistanceLabel.hide()
        self.axialDistanceCombo.hide()

    def setDistanceType(self, idx):
        self.axialDistanceCombo.setCurrentIndex(idx)

    def disableDistanceType(self, onoff):
        self.axialDistanceLabel.setDisabled(onoff)
        self.axialDistanceCombo.setDisabled(onoff)

    def setRadiusType(self, idx):
        self.axialRadiusCombo.setCurrentIndex(idx)

    def disableRadiusType(self, onoff):
        self.axialRadiusLabel.setDisabled(onoff)
        self.axialRadiusCombo.setDisabled(onoff)

    def setCalculateNorm(self, onoff):
        self.axialCalculateNormCheck.setChecked(onoff)

    def disableCalculateNorm(self, onoff):
        self.axialCalculateNormCheck.setDisabled(onoff)

    def setCalculateFull(self, onoff):
        self.axialCalculateFullCheck.setChecked(onoff)

    def disableCalculateFull(self, onoff):
        self.axialCalculateFullCheck.setDisabled(onoff)

    def setCalculateChoice(self, onoff):
        self.axialCalculateChoiceCheck.setChecked(onoff)

    def setRemoveStubs(self, value):
        self.axialStubsEdit.clear()
        self.axialStubsEdit.setText(str(value))

    def disableRemoveStubs(self, onoff):
        self.axialStubsLabel.setDisabled(onoff)
        self.axialStubsEdit.setDisabled(onoff)

    def checkRemoveStubs(self):
        try:
            int(self.axialStubsEdit.text())
            self.closeButtonBox.button(QtWidgets.QDialogButtonBox.Ok).setDisabled(False)
            self.closeButtonBox.button(QtWidgets.QDialogButtonBox.Ok).setToolTip('')
        except ValueError:
            self.closeButtonBox.button(QtWidgets.QDialogButtonBox.Ok).setDisabled(True)
            self.closeButtonBox.button(QtWidgets.QDialogButtonBox.Ok).setToolTip(
                'Please enter a valid stubs removal % (integer).')
