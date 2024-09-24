# SPDX-FileCopyrightText: 2021 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2021 Space Syntax Ltd
# 
# SPDX-License-Identifier: GPL-2.0-or-later

from qgis.PyQt.QtWidgets import (QWidget, QDockWidget)
from perdix.utilities import layer_field_helpers as lfh


class AnalysisEngine:
    """ Generic Engine Interface Class"""

    @staticmethod
    def get_engine_name() -> str:
        pass

    def create_settings_widget(self, dock_widget: QDockWidget) -> QWidget:
        pass

    @staticmethod
    def is_valid_unlinks_layer(self, unlinks_layer):
        return lfh.fieldExists(unlinks_layer, 'line1') and \
               lfh.fieldExists(unlinks_layer, 'line2') and \
               not lfh.fieldHasNullValues(unlinks_layer, 'line1') and \
               not lfh.fieldHasNullValues(unlinks_layer, 'line2')

    class AnalysisEngineError(Exception):
        """ Generic Exception raised when the engine errors"""
        pass

    class AnalysisResults:
        """ Stores results from the analysis for passing around"""

        def __init__(self, attributes, types, values, coords):
            self.attributes = attributes
            self.types = types
            self.values = values
            self.coords = coords
