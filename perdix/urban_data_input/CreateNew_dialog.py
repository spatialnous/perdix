# SPDX-FileCopyrightText: 2016 Abhimanyu Acharya <a.acharya@spacesyntax.com>
# SPDX-FileCopyrightText: 2016 Space Syntax Limited
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import print_function

import os

from qgis.PyQt import QtCore, QtWidgets, uic

from perdix.utilities import db_helpers as dbh
from .DbSettings_dialog import DbSettingsDialog

Ui_CreateNewDialog, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ui", "create_new_dialog.ui")
)


class CreatenewDialog(QtWidgets.QDialog, Ui_CreateNewDialog):
    create_new_layer = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(CreatenewDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # setup signals
        self.closePopUpButton.clicked.connect(self.closePopUp)
        self.pushButtonSelectLocation.clicked.connect(self.selectSaveLocation)
        self.pushButtonNewFileDLG.clicked.connect(self.createLayer)

        available_dbs = dbh.getQGISDbs()
        self.dbsettings_dlg = DbSettingsDialog(available_dbs)
        self.dbsettings_dlg.nameLineEdit.setText("frontages")

        self.f_memory_radioButton.setChecked(True)
        self.lineEditFrontages.setPlaceholderText("Specify temporary layer name")
        self.lineEditFrontages.setDisabled(False)
        self.f_shp_radioButton.setChecked(False)
        self.f_postgis_radioButton.setChecked(False)

        self.f_shp_radioButton.clicked.connect(self.setOutput)
        self.f_postgis_radioButton.clicked.connect(self.setOutput)
        self.f_memory_radioButton.clicked.connect(self.setOutput)
        self.pushButtonSelectLocation.setDisabled(True)

        # self.dbsettings_dlg.setDbOutput.connect(self.setOutput)
        self.dbsettings_dlg.dbCombo.currentIndexChanged.connect(self.setDbPath)
        self.dbsettings_dlg.schemaCombo.currentIndexChanged.connect(self.setDbPath)
        self.dbsettings_dlg.nameLineEdit.textChanged.connect(self.setDbPath)
        self.dbsettings_dlg.okButton.clicked.connect(self.setDbPath)

    # Close create new file pop up dialogue when cancel button is pressed
    def closePopUp(self):
        self.close()

    # Open Save file dialogue and set location in text edit
    def selectSaveLocation(self):
        if self.f_shp_radioButton.isChecked():
            self.lineEditFrontages.clear()
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Specify Output Location ", "", "*.shp"
            )
            self.lineEditFrontages.setText(filename)
        elif self.f_postgis_radioButton.isChecked():
            self.lineEditFrontages.clear()
            self.setOutput()
            self.dbsettings_dlg.show()
            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            print("self.dbsettings", self.dbsettings)
            if self.dbsettings:
                db_layer_name = "%s:%s:%s" % (
                    self.dbsettings["dbname"],
                    self.dbsettings["schema"],
                    self.dbsettings["table_name"],
                )
                print("db_layer_name")
                self.lineEditFrontages.setText(db_layer_name)
        elif self.f_memory_radioButton.isChecked():
            self.lineEditFrontages.clear()
            pass

    def createLayer(self):
        self.create_new_layer.emit()

    def setDbPath(self):
        print("setdbpath")
        if self.f_postgis_radioButton.isChecked():
            try:
                self.dbsettings = self.dbsettings_dlg.getDbSettings()
                db_layer_name = "%s:%s:%s" % (
                    self.dbsettings["dbname"],
                    self.dbsettings["schema"],
                    self.dbsettings["table_name"],
                )
                self.lineEditFrontages.setText(db_layer_name)
            except Exception as e:
                print(
                    f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
                )
                self.lineEditFrontages.setText(self.lineEditFrontages.placeholderText())
        return

    def setOutput(self):
        if self.f_shp_radioButton.isChecked():
            self.lineEditFrontages.clear()
            self.lineEditFrontages.setPlaceholderText("Specify output location")
            self.lineEditFrontages.setDisabled(True)
            self.pushButtonSelectLocation.setDisabled(False)
        elif self.f_postgis_radioButton.isChecked():
            self.lineEditFrontages.clear()
            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            self.pushButtonSelectLocation.setDisabled(False)
            print("dbs1", self.dbsettings)
            if self.dbsettings != {}:
                db_layer_name = "%s:%s:%s" % (
                    self.dbsettings["dbname"],
                    self.dbsettings["schema"],
                    self.dbsettings["table_name"],
                )
                self.lineEditFrontages.setText(db_layer_name)
                self.lineEditFrontages.setDisabled(False)
            else:
                self.lineEditFrontages.setPlaceholderText(
                    "Specify as database:schema:table name"
                )
                self.lineEditFrontages.setDisabled(True)
        elif self.f_memory_radioButton.isChecked():
            self.lineEditFrontages.clear()
            self.lineEditFrontages.setDisabled(False)
            self.lineEditFrontages.setPlaceholderText("Specify temporary layer name")
            self.pushButtonSelectLocation.setDisabled(True)
