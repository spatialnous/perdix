# SPDX-FileCopyrightText: 2017 Ioanna Kolovou <i.kolovou@spacesyntax.com>
# SPDX-FileCopyrightText: 2017 Space Syntax Limited
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
# 
# SPDX-License-Identifier: GPL-2.0-or-later

""" Network based catchment analysis
"""

from __future__ import absolute_import
from __future__ import print_function

import os

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from perdix.utilities import db_helpers as dbh

Ui_DbSettingsDialog, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'db_settings_dialog.ui'))


class DbSettingsDialog(QtWidgets.QDialog, Ui_DbSettingsDialog):
    closingPlugin = pyqtSignal()
    setDbOutput = pyqtSignal()

    def __init__(self, available_dbs, parent=None):
        """Constructor."""
        super(DbSettingsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.available_dbs = available_dbs
        self.connstring = None
        self.popDbs()
        self.okButton.clicked.connect(self.close)
        self.dbCombo.currentIndexChanged.connect(self.popSchemas)

    def popDbs(self):
        self.dbCombo.clear()
        self.dbCombo.addItems(['select db'] + sorted(self.available_dbs.keys()))
        return

    def getSelectedDb(self):
        return self.dbCombo.currentText()

    def getDbSettings(self):
        connection = self.dbCombo.currentText()
        if connection in list(self.available_dbs.keys()):
            return {'dbname': connection,
                    'schema': self.schemaCombo.currentText(),
                    'table_name': self.nameLineEdit.text()}
        else:
            return {}

    def popSchemas(self):
        idx = self.dbCombo.findText('select db')
        if idx != -1:
            self.dbCombo.removeItem(idx)
        self.schemaCombo.clear()
        schemas = []
        selected_db = self.getSelectedDb()
        if len(self.getSelectedDb()) > 1:
            self.get_connstring(selected_db)
            print('connstring', self.connstring)
            schemas = dbh.getPostgisSchemas(self.connstring)
        self.schemaCombo.addItems(schemas)

    def get_connstring(self, selected_db):
        db_info = self.available_dbs[selected_db]
        print('tries', db_info, selected_db)
        self.connstring = ''
        try:
            db_info['user'] = db_info['username']
            del db_info['username']
        except KeyError:
            pass
        try:
            db_info['dbname'] = db_info['database']
            del db_info['database']
        except KeyError:
            pass
        for k, v in list(db_info.items()):
            self.connstring += k + '=' + v + ' '
        return

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
