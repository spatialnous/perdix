# SPDX-FileCopyrightText: 2014 - 2015 Jorge Gil <jorge.gil@ucl.ac.uk>
# SPDX-FileCopyrightText: 2014 - 2015 UCL
# 
# SPDX-License-Identifier: GPL-2.0-or-later

# Import the PyQt and QGIS libraries
from qgis.PyQt.QtCore import (QThread, pyqtSignal)


class AttributeStats(QThread):
    calculationFinished = pyqtSignal(dict, list)
    calculationProgress = pyqtSignal(int)
    calculationError = pyqtSignal(str)

    def __init__(self, parentThread, parentObject, layer, attribute):
        QThread.__init__(self, parentThread)
        self.parent = parentObject
        self.running = False
        self.layer = layer
        self.attribute = attribute

    def run(self):
        pass
