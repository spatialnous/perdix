# SPDX-FileCopyrightText: 2019 Ioanna Kolovou <i.kolovou@spacesyntax.com>
# SPDX-FileCopyrightText: 2019 Space Syntax Limited
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

# general imports
from builtins import str

from qgis.PyQt.QtCore import QObject, QMetaType
from qgis.core import QgsField, QgsFields

flds = QgsFields()
flds.append(QgsField("id", QMetaType.Type.Int))

flds2 = QgsFields(flds)
flds2.append(QgsField("topology", QMetaType.Type.QString))
flds2.append(QgsField("adj_edges", QMetaType.Type.QString))


class sNode(QObject):
    def __init__(self, id, feature, topology, adj_edges):
        QObject.__init__(self)
        self.id = id
        self.topology = topology
        self.adj_edges = adj_edges
        self.feature = feature
        self.feature.setFields(flds)
        self.feature.setAttributes([self.id])

    def getCoords(self):
        coords = self.feature.geometry().asPoint()
        return coords[0], coords[1]

    def getFeature(self):
        self.feature.setFields(flds2)
        self.feature.setAttributes([self.id, str(self.topology), str(self.adj_edges)])
        return self.feature
