# SPDX-FileCopyrightText: 2016 Abhimanyu Acharya <a.acharya@spacesyntax.com>
# SPDX-FileCopyrightText: 2016 Space Syntax Limited
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import

from qgis.PyQt.QtCore import QObject, QSettings, Qt
from qgis.core import QgsProject

from .entrances import EntranceTool
from .frontages import FrontageTool
from .landuse import LanduseTool
from .urban_data_input_dockwidget import UrbanDataInputDockWidget
from perdix.utilities import utility_functions as uf


class UrbanDataInputTool(QObject):
    # initialise class with self and iface
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # create the dialog objects
        self.dockwidget = UrbanDataInputDockWidget(self.iface)
        self.frontage_tool = FrontageTool(self.iface, self.dockwidget)
        self.entrance_tool = EntranceTool(self.iface, self.dockwidget)
        self.lu_tool = LanduseTool(self.iface, self.dockwidget)

        # connect to provide cleanup on closing of dockwidget
        self.dockwidget.closingPlugin.connect(self.unload_gui)

        # get current user settings
        self.user_settings = {}
        self.user_settings["crs"] = QSettings().value("/qgis/crs/use_project_crs")
        self.user_settings["attrib_dialog"] = QSettings().value(
            "/qgis/digitizing/disable_enter_attribute_values_dialog"
        )

    def load_gui(self):
        # Overide existing QGIS settings
        if not self.user_settings["attrib_dialog"]:
            QSettings().setValue(
                "/qgis/digitizing/disable_enter_attribute_values_dialog", True
            )
        if not self.user_settings["crs"]:
            QSettings().setValue("/qgis/crs/use_project_crs", True)

        # show the dockwidget
        # TODO: fix to allow choice of dock location
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        self.dockwidget.show()

        # set up GUI operation signals
        # legend change connections
        self.iface.projectRead.connect(self.updateLayers)
        self.iface.newProjectCreated.connect(self.updateLayers)
        QgsProject.instance().layersRemoved.connect(self.updateLayers)
        QgsProject.instance().layersAdded.connect(self.updateLayers)
        # Frontages
        self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addDataFields)
        # Entrances
        self.iface.mapCanvas().selectionChanged.connect(
            self.dockwidget.addEntranceDataFields
        )
        # Landuse
        self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addLUDataFields)
        # Initialisation
        self.updateLayers()

    def unload_gui(self):
        # self.dockwidget.close()
        # disconnect interface signals
        try:
            # restore user settings
            QSettings().setValue(
                "/qgis/digitizing/disable_enter_attribute_values_dialog",
                self.user_settings["attrib_dialog"],
            )
            QSettings().setValue("/qgis/crs/use_project_crs", self.user_settings["crs"])

            # legend change connections
            uf.disconnectSignal(self.iface.projectRead, self.updateLayers)
            uf.disconnectSignal(self.iface.newProjectCreated, self.updateLayers)
            uf.disconnectSignal(QgsProject.instance().layersRemoved, self.updateLayers)
            uf.disconnectSignal(QgsProject.instance().layersAdded, self.updateLayers)

            # Frontages
            uf.disconnectSignal(
                self.iface.mapCanvas().selectionChanged, self.dockwidget.addDataFields
            )
            self.frontage_tool.disconnectFrontageLayer()
            # Entrances
            uf.disconnectSignal(
                self.iface.mapCanvas().selectionChanged,
                self.dockwidget.addEntranceDataFields,
            )
            self.entrance_tool.disconnectEntranceLayer()
            # Landuse
            uf.disconnectSignal(
                self.iface.mapCanvas().selectionChanged, self.dockwidget.addLUDataFields
            )
            self.lu_tool.disconnectLULayer()
        except Exception as e:
            print(
                f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
            pass

    def updateLayers(self):
        # frontages
        self.frontage_tool.updateLayers()
        self.frontage_tool.updateFrontageLayer()
        # this is not being used at the moment
        # self.frontage_tool.updateLayersPushID
        # entrances
        self.entrance_tool.updateEntranceLayer()
        # land use
        self.lu_tool.loadLULayer()
        self.lu_tool.updatebuildingLayers()
        self.lu_tool.updateLULayer()
