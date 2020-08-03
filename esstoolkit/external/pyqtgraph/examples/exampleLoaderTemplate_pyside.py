# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exampleLoaderTemplate.ui'
#
# Created: Sat Feb 28 10:31:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(846, 552)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.exampleTree = QtGui.QTreeWidget(self.widget)
        self.exampleTree.setObjectName("exampleTree")
        self.exampleTree.headerItem().setText(0, "1")
        self.exampleTree.header().setVisible(False)
        self.gridLayout.addWidget(self.exampleTree, 0, 0, 1, 2)
        self.graphicsSystemCombo = QtGui.QComboBox(self.widget)
        self.graphicsSystemCombo.setObjectName("graphicsSystemCombo")
        self.graphicsSystemCombo.addItem("")
        self.graphicsSystemCombo.addItem("")
        self.graphicsSystemCombo.addItem("")
        self.graphicsSystemCombo.addItem("")
        self.gridLayout.addWidget(self.graphicsSystemCombo, 2, 1, 1, 1)
        self.qtLibCombo = QtGui.QComboBox(self.widget)
        self.qtLibCombo.setObjectName("qtLibCombo")
        self.qtLibCombo.addItem("")
        self.qtLibCombo.addItem("")
        self.qtLibCombo.addItem("")
        self.qtLibCombo.addItem("")
        self.gridLayout.addWidget(self.qtLibCombo, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.loadBtn = QtGui.QPushButton(self.widget)
        self.loadBtn.setObjectName("loadBtn")
        self.gridLayout.addWidget(self.loadBtn, 3, 1, 1, 1)
        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.loadedFileLabel = QtGui.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.loadedFileLabel.setFont(font)
        self.loadedFileLabel.setText("")
        self.loadedFileLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadedFileLabel.setObjectName("loadedFileLabel")
        self.verticalLayout.addWidget(self.loadedFileLabel)
        self.codeView = QtGui.QPlainTextEdit(self.widget1)
        font = QtGui.QFont()
        font.setFamily("FreeMono")
        self.codeView.setFont(font)
        self.codeView.setObjectName("codeView")
        self.verticalLayout.addWidget(self.codeView)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsSystemCombo.setItemText(0, QtGui.QApplication.translate("Form", "default", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsSystemCombo.setItemText(1, QtGui.QApplication.translate("Form", "native", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsSystemCombo.setItemText(2, QtGui.QApplication.translate("Form", "raster", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsSystemCombo.setItemText(3, QtGui.QApplication.translate("Form", "opengl", None, QtGui.QApplication.UnicodeUTF8))
        self.qtLibCombo.setItemText(0, QtGui.QApplication.translate("Form", "default", None, QtGui.QApplication.UnicodeUTF8))
        self.qtLibCombo.setItemText(1, QtGui.QApplication.translate("Form", "PyQt4", None, QtGui.QApplication.UnicodeUTF8))
        self.qtLibCombo.setItemText(2, QtGui.QApplication.translate("Form", "PySide", None, QtGui.QApplication.UnicodeUTF8))
        self.qtLibCombo.setItemText(3, QtGui.QApplication.translate("Form", "PyQt5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Graphics System:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Qt Library:", None, QtGui.QApplication.UnicodeUTF8))
        self.loadBtn.setText(QtGui.QApplication.translate("Form", "Run Example", None, QtGui.QApplication.UnicodeUTF8))

