# SPDX-FileCopyrightText: 2016 Abhimanyu Acharya <a.acharya@spacesyntax.com>
# SPDX-FileCopyrightText: 2016 Space Syntax Limited
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import print_function

import os

from qgis.PyQt import QtCore, QtWidgets, uic

from .DbSettings_dialog import DbSettingsDialog
from perdix.utilities import db_helpers as dbh

Ui_CreateNewLUDialog, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'create_new_lu_dialog.ui'))


class CreateNew_LUDialog(QtWidgets.QDialog, Ui_CreateNewLUDialog):
    create_new_layer = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(CreateNew_LUDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # setup signals
        self.pushButtonSelectLocationLU.clicked.connect(self.selectSaveLocationLU)
        self.pushButtonLUNewFileDLG.clicked.connect(self.newLULayer)
        self.closePopUpLUButton.clicked.connect(self.closePopUpLU)

        available_dbs = dbh.getQGISDbs(portlast=True)
        self.dbsettings_dlg = DbSettingsDialog(available_dbs)
        self.dbsettings_dlg.nameLineEdit.setText('landuse')

        self.lu_memory_radioButton.setChecked(True)
        self.lineEditLU.setPlaceholderText('Specify temporary layer name')
        self.lineEditLU.setDisabled(False)
        self.lu_shp_radioButton.setChecked(False)
        self.lu_postgis_radioButton.setChecked(False)

        self.lu_shp_radioButton.clicked.connect(self.setOutput)
        self.lu_postgis_radioButton.clicked.connect(self.setOutput)
        self.lu_memory_radioButton.clicked.connect(self.setOutput)
        self.pushButtonSelectLocationLU.setDisabled(True)

        # self.dbsettings_dlg.setDbOutput.connect(self.setOutput)
        self.dbsettings_dlg.dbCombo.currentIndexChanged.connect(self.setDbPath)
        self.dbsettings_dlg.schemaCombo.currentIndexChanged.connect(self.setDbPath)
        self.dbsettings_dlg.nameLineEdit.textChanged.connect(self.setDbPath)

    def closePopUpLU(self):
        self.close()

    # Open Save file dialogue and set location in text edit
    def selectSaveLocationLU(self):
        if self.lu_shp_radioButton.isChecked():
            self.lineEditLU.clear()
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Specify Output Location ", "", '*.shp')
            self.lineEditLU.setText(filename)
        elif self.lu_postgis_radioButton.isChecked():
            self.lineEditLU.clear()
            self.setOutput()
            self.dbsettings_dlg.show()
            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            if self.dbsettings:
                db_layer_name = "%s:%s:%s" % (
                    self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
                print('db_layer_name')
                self.lineEditLU.setText(db_layer_name)
        elif self.lu_memory_radioButton.isChecked():
            self.lineEditLU.clear()
            pass

    def setDbPath(self):
        if self.lu_postgis_radioButton.isChecked():
            try:
                self.dbsettings = self.dbsettings_dlg.getDbSettings()
                db_layer_name = "%s:%s:%s" % (
                    self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
                self.lineEditLU.setText(db_layer_name)
            except:
                self.lineEditLU.clear()
        return

    def setOutput(self):
        if self.lu_shp_radioButton.isChecked():
            self.lineEditLU.clear()
            self.lineEditLU.setPlaceholderText('Specify output location')
            self.lineEditLU.setDisabled(True)
            self.pushButtonSelectLocationLU.setDisabled(False)
        elif self.lu_postgis_radioButton.isChecked():
            self.lineEditLU.clear()
            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            self.pushButtonSelectLocationLU.setDisabled(False)
            print('dbs1', self.dbsettings)
            if self.dbsettings != {}:
                db_layer_name = "%s:%s:%s" % (
                    self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
                self.lineEditLU.setText(db_layer_name)
                self.lineEditLU.setDisabled(False)
            else:
                self.lineEditLU.setPlaceholderText('Specify as database:schema:table name')
                self.lineEditLU.setDisabled(True)
        elif self.lu_memory_radioButton.isChecked():
            self.lineEditLU.clear()
            self.lineEditLU.setDisabled(False)
            self.lineEditLU.setPlaceholderText('Specify temporary layer name')
            self.pushButtonSelectLocationLU.setDisabled(True)

    def newLULayer(self):
        self.create_new_layer.emit()

    def getSelectedLULayerID(self):
        return self.selectIDbuildingCombo.currentText()
