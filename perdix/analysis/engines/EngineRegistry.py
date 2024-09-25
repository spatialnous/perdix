# SPDX-FileCopyrightText: 2021 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2021 Space Syntax Ltd
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

from typing import Dict
from perdix.analysis.engines.AnalysisEngine import AnalysisEngine
from perdix.analysis.engines.DepthmapNet.DepthmapNetEngine import DepthmapNetEngine
from perdix.analysis.engines.DepthmapCLI.DepthmapCLIEngine import DepthmapCLIEngine


class EngineRegistry:
    """Meant to hold and handle all available analysis engines"""

    available_engines: Dict[str, str] = {}

    def __init__(self):
        self.available_engines[DepthmapNetEngine.get_engine_name()] = (
            "DepthmapNetEngine"
        )
        self.available_engines[DepthmapCLIEngine.get_engine_name()] = (
            "DepthmapCLIEngine"
        )

    def get_available_engines(self) -> [str]:
        return self.available_engines.keys()

    def get_engine(self, type: str, iface: object) -> AnalysisEngine:
        if type not in self.available_engines:
            return
        return globals()[self.available_engines[type]](iface)
