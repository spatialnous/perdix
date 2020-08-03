# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'explorer/ui_Explorer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from __future__ import absolute_import
from builtins import object
from qgis.PyQt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ExplorerDialog(object):
    def setupUi(self, ExplorerDialog):
        ExplorerDialog.setObjectName(_fromUtf8("ExplorerDialog"))
        ExplorerDialog.resize(364, 550)
        ExplorerDialog.setMinimumSize(QtCore.QSize(364, 550))
        self.explorerLayout = QtGui.QWidget()
        self.explorerLayout.setObjectName(_fromUtf8("explorerLayout"))
        self.verticalLayout = QtGui.QVBoxLayout(self.explorerLayout)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.explorerLayout)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.attributesLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.attributesLayout.setObjectName(_fromUtf8("attributesLayout"))
        self.layersLayout = QtGui.QHBoxLayout()
        self.layersLayout.setObjectName(_fromUtf8("layersLayout"))
        self.layerCombo = QtGui.QComboBox(self.layoutWidget)
        self.layerCombo.setObjectName(_fromUtf8("layerCombo"))
        self.layersLayout.addWidget(self.layerCombo)
        self.layerRefreshButton = QtGui.QPushButton(self.layoutWidget)
        self.layerRefreshButton.setObjectName(_fromUtf8("layerRefreshButton"))
        self.layersLayout.addWidget(self.layerRefreshButton)
        self.layersLayout.setStretch(0, 5)
        self.attributesLayout.addLayout(self.layersLayout)
        self.attributesLabel = QtGui.QLabel(self.layoutWidget)
        self.attributesLabel.setObjectName(_fromUtf8("attributesLabel"))
        self.attributesLayout.addWidget(self.attributesLabel)
        self.attributesList = QtGui.QListWidget(self.layoutWidget)
        self.attributesList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.attributesList.setObjectName(_fromUtf8("attributesList"))
        self.attributesLayout.addWidget(self.attributesList)
        self.attributesLayout.setStretch(0, 1)
        self.attributesLayout.setStretch(1, 1)
        self.attributesLayout.setStretch(2, 10)
        self.explorerTabs = QtGui.QTabWidget(self.splitter)
        self.explorerTabs.setObjectName(_fromUtf8("explorerTabs"))
        self.symbologyTab = QtGui.QWidget()
        self.symbologyTab.setObjectName(_fromUtf8("symbologyTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.symbologyTab)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(10)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.coloursLayout = QtGui.QGridLayout()
        self.coloursLayout.setContentsMargins(-1, -1, 0, -1)
        self.coloursLayout.setObjectName(_fromUtf8("coloursLayout"))
        self.colourRangeCombo = QtGui.QComboBox(self.symbologyTab)
        self.colourRangeCombo.setObjectName(_fromUtf8("colourRangeCombo"))
        self.coloursLayout.addWidget(self.colourRangeCombo, 0, 1, 1, 1)
        self.colourRangeLabel = QtGui.QLabel(self.symbologyTab)
        self.colourRangeLabel.setObjectName(_fromUtf8("colourRangeLabel"))
        self.coloursLayout.addWidget(self.colourRangeLabel, 0, 0, 1, 1)
        self.lineWidthLabel = QtGui.QLabel(self.symbologyTab)
        self.lineWidthLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineWidthLabel.setObjectName(_fromUtf8("lineWidthLabel"))
        self.coloursLayout.addWidget(self.lineWidthLabel, 2, 0, 1, 1)
        self.lineWidthSpin = QtGui.QDoubleSpinBox(self.symbologyTab)
        self.lineWidthSpin.setPrefix(_fromUtf8(""))
        self.lineWidthSpin.setMaximum(10.0)
        self.lineWidthSpin.setSingleStep(0.25)
        self.lineWidthSpin.setObjectName(_fromUtf8("lineWidthSpin"))
        self.coloursLayout.addWidget(self.lineWidthSpin, 2, 1, 1, 1)
        self.displayOrderCombo = QtGui.QComboBox(self.symbologyTab)
        self.displayOrderCombo.setEnabled(True)
        self.displayOrderCombo.setFrame(True)
        self.displayOrderCombo.setObjectName(_fromUtf8("displayOrderCombo"))
        self.displayOrderCombo.addItem(_fromUtf8(""))
        self.displayOrderCombo.addItem(_fromUtf8(""))
        self.coloursLayout.addWidget(self.displayOrderCombo, 1, 1, 1, 1)
        self.invertColourCheck = QtGui.QCheckBox(self.symbologyTab)
        self.invertColourCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.invertColourCheck.setObjectName(_fromUtf8("invertColourCheck"))
        self.coloursLayout.addWidget(self.invertColourCheck, 1, 0, 1, 1)
        self.coloursLayout.setColumnStretch(1, 1)
        self.verticalLayout_2.addLayout(self.coloursLayout)
        self.intervalsLayout = QtGui.QGridLayout()
        self.intervalsLayout.setObjectName(_fromUtf8("intervalsLayout"))
        self.intervalLabel = QtGui.QLabel(self.symbologyTab)
        self.intervalLabel.setObjectName(_fromUtf8("intervalLabel"))
        self.intervalsLayout.addWidget(self.intervalLabel, 0, 0, 1, 1)
        self.intervalTypeCombo = QtGui.QComboBox(self.symbologyTab)
        self.intervalTypeCombo.setObjectName(_fromUtf8("intervalTypeCombo"))
        self.intervalsLayout.addWidget(self.intervalTypeCombo, 0, 2, 1, 1)
        self.topLimitLabel = QtGui.QLabel(self.symbologyTab)
        self.topLimitLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.topLimitLabel.setLineWidth(0)
        self.topLimitLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.topLimitLabel.setObjectName(_fromUtf8("topLimitLabel"))
        self.intervalsLayout.addWidget(self.topLimitLabel, 1, 0, 1, 1)
        self.topLimitText = QtGui.QLineEdit(self.symbologyTab)
        self.topLimitText.setObjectName(_fromUtf8("topLimitText"))
        self.intervalsLayout.addWidget(self.topLimitText, 1, 2, 1, 1)
        self.bottomLimitLabel = QtGui.QLabel(self.symbologyTab)
        self.bottomLimitLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bottomLimitLabel.setObjectName(_fromUtf8("bottomLimitLabel"))
        self.intervalsLayout.addWidget(self.bottomLimitLabel, 2, 0, 1, 1)
        self.bottomLimitSpin = QtGui.QSpinBox(self.symbologyTab)
        self.bottomLimitSpin.setSpecialValueText(_fromUtf8(""))
        self.bottomLimitSpin.setPrefix(_fromUtf8(""))
        self.bottomLimitSpin.setMaximum(100)
        self.bottomLimitSpin.setObjectName(_fromUtf8("bottomLimitSpin"))
        self.intervalsLayout.addWidget(self.bottomLimitSpin, 2, 1, 1, 1)
        self.bottomLimitText = QtGui.QLineEdit(self.symbologyTab)
        self.bottomLimitText.setObjectName(_fromUtf8("bottomLimitText"))
        self.intervalsLayout.addWidget(self.bottomLimitText, 2, 2, 1, 1)
        self.topLimitSpin = QtGui.QSpinBox(self.symbologyTab)
        self.topLimitSpin.setMaximum(100)
        self.topLimitSpin.setProperty("value", 100)
        self.topLimitSpin.setObjectName(_fromUtf8("topLimitSpin"))
        self.intervalsLayout.addWidget(self.topLimitSpin, 1, 1, 1, 1)
        self.intervalSpin = QtGui.QSpinBox(self.symbologyTab)
        self.intervalSpin.setMinimum(1)
        self.intervalSpin.setMaximum(1024)
        self.intervalSpin.setObjectName(_fromUtf8("intervalSpin"))
        self.intervalsLayout.addWidget(self.intervalSpin, 0, 1, 1, 1)
        self.intervalsLayout.setColumnStretch(2, 1)
        self.verticalLayout_2.addLayout(self.intervalsLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.symbologyApplyButton = QtGui.QPushButton(self.symbologyTab)
        self.symbologyApplyButton.setObjectName(_fromUtf8("symbologyApplyButton"))
        self.verticalLayout_2.addWidget(self.symbologyApplyButton)
        self.explorerTabs.addTab(self.symbologyTab, _fromUtf8(""))
        self.statsTab = QtGui.QWidget()
        self.statsTab.setObjectName(_fromUtf8("statsTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.statsTab)
        self.verticalLayout_3.setMargin(10)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.statisticsTable = QtGui.QTableWidget(self.statsTab)
        self.statisticsTable.setLineWidth(1)
        self.statisticsTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.statisticsTable.setAutoScroll(True)
        self.statisticsTable.setAlternatingRowColors(True)
        self.statisticsTable.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.statisticsTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.statisticsTable.setGridStyle(QtCore.Qt.NoPen)
        self.statisticsTable.setRowCount(0)
        self.statisticsTable.setColumnCount(3)
        self.statisticsTable.setObjectName(_fromUtf8("statisticsTable"))
        item = QtGui.QTableWidgetItem()
        self.statisticsTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.statisticsTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.statisticsTable.setHorizontalHeaderItem(2, item)
        self.statisticsTable.horizontalHeader().setStretchLastSection(True)
        self.statisticsTable.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.statisticsTable)
        self.statisticsProgressBar = QtGui.QProgressBar(self.statsTab)
        self.statisticsProgressBar.setProperty("value", 24)
        self.statisticsProgressBar.setObjectName(_fromUtf8("statisticsProgressBar"))
        self.verticalLayout_3.addWidget(self.statisticsProgressBar)
        self.verticalLayout_3.setStretch(0, 4)
        self.explorerTabs.addTab(self.statsTab, _fromUtf8(""))
        self.chartsTab = QtGui.QWidget()
        self.chartsTab.setObjectName(_fromUtf8("chartsTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.chartsTab)
        self.verticalLayout_4.setMargin(10)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.chartsLayout = QtGui.QHBoxLayout()
        self.chartsLayout.setObjectName(_fromUtf8("chartsLayout"))
        self.chartToolsLayout = QtGui.QVBoxLayout()
        self.chartToolsLayout.setObjectName(_fromUtf8("chartToolsLayout"))
        self.chartSetupLayout = QtGui.QVBoxLayout()
        self.chartSetupLayout.setObjectName(_fromUtf8("chartSetupLayout"))
        self.histogramCheck = QtGui.QRadioButton(self.chartsTab)
        self.histogramCheck.setObjectName(_fromUtf8("histogramCheck"))
        self.chartSetupLayout.addWidget(self.histogramCheck)
        self.scatterplotCheck = QtGui.QRadioButton(self.chartsTab)
        self.scatterplotCheck.setObjectName(_fromUtf8("scatterplotCheck"))
        self.chartSetupLayout.addWidget(self.scatterplotCheck)
        self.yaxisLabel = QtGui.QLabel(self.chartsTab)
        self.yaxisLabel.setObjectName(_fromUtf8("yaxisLabel"))
        self.chartSetupLayout.addWidget(self.yaxisLabel)
        self.yaxisCombo = QtGui.QComboBox(self.chartsTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yaxisCombo.sizePolicy().hasHeightForWidth())
        self.yaxisCombo.setSizePolicy(sizePolicy)
        self.yaxisCombo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.yaxisCombo.setObjectName(_fromUtf8("yaxisCombo"))
        self.chartSetupLayout.addWidget(self.yaxisCombo)
        self.rLabel = QtGui.QLabel(self.chartsTab)
        self.rLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.rLabel.setObjectName(_fromUtf8("rLabel"))
        self.chartSetupLayout.addWidget(self.rLabel)
        self.pLabel = QtGui.QLabel(self.chartsTab)
        self.pLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.pLabel.setObjectName(_fromUtf8("pLabel"))
        self.chartSetupLayout.addWidget(self.pLabel)
        self.r2Label = QtGui.QLabel(self.chartsTab)
        self.r2Label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.r2Label.setObjectName(_fromUtf8("r2Label"))
        self.chartSetupLayout.addWidget(self.r2Label)
        self.lineLabel = QtGui.QLabel(self.chartsTab)
        self.lineLabel.setWordWrap(True)
        self.lineLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lineLabel.setObjectName(_fromUtf8("lineLabel"))
        self.chartSetupLayout.addWidget(self.lineLabel)
        self.chartToolsLayout.addLayout(self.chartSetupLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.chartToolsLayout.addItem(spacerItem1)
        self.lineCheck = QtGui.QCheckBox(self.chartsTab)
        self.lineCheck.setChecked(True)
        self.lineCheck.setObjectName(_fromUtf8("lineCheck"))
        self.chartToolsLayout.addWidget(self.lineCheck)
        self.chartToolsLayout.setStretch(1, 3)
        self.chartsLayout.addLayout(self.chartToolsLayout)
        self.verticalLayout_4.addLayout(self.chartsLayout)
        self.chartsProgressBar = QtGui.QProgressBar(self.chartsTab)
        self.chartsProgressBar.setProperty("value", 24)
        self.chartsProgressBar.setObjectName(_fromUtf8("chartsProgressBar"))
        self.verticalLayout_4.addWidget(self.chartsProgressBar)
        self.verticalLayout_4.setStretch(0, 4)
        self.explorerTabs.addTab(self.chartsTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.splitter)
        ExplorerDialog.setWidget(self.explorerLayout)

        self.retranslateUi(ExplorerDialog)
        self.explorerTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ExplorerDialog)

    def retranslateUi(self, ExplorerDialog):
        ExplorerDialog.setWindowTitle(_translate("ExplorerDialog", "Attributes Explorer", None))
        self.layerRefreshButton.setText(_translate("ExplorerDialog", "Refresh", None))
        self.attributesLabel.setText(_translate("ExplorerDialog", "Numeric attributes:", None))
        self.colourRangeLabel.setText(_translate("ExplorerDialog", "Colour range:", None))
        self.lineWidthLabel.setText(_translate("ExplorerDialog", "Width / Size:", None))
        self.displayOrderCombo.setItemText(0, _translate("ExplorerDialog", "Display top level first", None))
        self.displayOrderCombo.setItemText(1, _translate("ExplorerDialog", "Display bottom level first", None))
        self.invertColourCheck.setText(_translate("ExplorerDialog", "Invert", None))
        self.intervalLabel.setText(_translate("ExplorerDialog", "Intervals:", None))
        self.topLimitLabel.setText(_translate("ExplorerDialog", "Top:", None))
        self.topLimitText.setText(_translate("ExplorerDialog", "Maximum", None))
        self.bottomLimitLabel.setText(_translate("ExplorerDialog", "Bottom:", None))
        self.bottomLimitText.setText(_translate("ExplorerDialog", "Minimum", None))
        self.symbologyApplyButton.setText(_translate("ExplorerDialog", "Apply Symbology", None))
        self.explorerTabs.setTabText(self.explorerTabs.indexOf(self.symbologyTab), _translate("ExplorerDialog", "Symbology", None))
        item = self.statisticsTable.horizontalHeaderItem(0)
        item.setText(_translate("ExplorerDialog", "Statistic", None))
        item = self.statisticsTable.horizontalHeaderItem(1)
        item.setText(_translate("ExplorerDialog", "Value", None))
        item = self.statisticsTable.horizontalHeaderItem(2)
        item.setText(_translate("ExplorerDialog", "Selection", None))
        self.explorerTabs.setTabText(self.explorerTabs.indexOf(self.statsTab), _translate("ExplorerDialog", "Stats", None))
        self.histogramCheck.setText(_translate("ExplorerDialog", "Histogram", None))
        self.scatterplotCheck.setText(_translate("ExplorerDialog", "Scatter plot", None))
        self.yaxisLabel.setText(_translate("ExplorerDialog", "Y axis:", None))
        self.yaxisCombo.setToolTip(_translate("ExplorerDialog", "Select y axis attribute of scatter plot.", None))
        self.rLabel.setText(_translate("ExplorerDialog", "r: ", None))
        self.pLabel.setText(_translate("ExplorerDialog", "p: ", None))
        self.r2Label.setText(_translate("ExplorerDialog", "r2: ", None))
        self.lineLabel.setText(_translate("ExplorerDialog", "f(x): ", None))
        self.lineCheck.setText(_translate("ExplorerDialog", "Regression line", None))
        self.explorerTabs.setTabText(self.explorerTabs.indexOf(self.chartsTab), _translate("ExplorerDialog", "Charts", None))

from . import resources_rc
