# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2020 Space Syntax Ltd.
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

import csv
import os
import stat
import platform
import re
import subprocess
import tempfile
import threading

from builtins import str
from typing import Optional, Tuple

from qgis.PyQt.QtCore import QObject

from perdix.analysis.engines.AnalysisEngine import AnalysisEngine
from perdix.analysis.engines.Depthmap.DepthmapEngine import DepthmapEngine
from perdix.utilities import layer_field_helpers as lfh
from perdix.utilities.utility_functions import overrides
from perdix.utilities.exceptions import BadInputError
from perdix.analysis.engines.DepthmapCLI.DepthmapCLISettingsWidget import (
    DepthmapCLISettingsWidget,
)


class DepthmapCLIEngine(QObject, DepthmapEngine):
    @overrides(DepthmapEngine)
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface

        # initialise global variables
        self.axial_layer = None
        self.datastore = None
        self.settings = None
        self.axial_id = ""
        self.prep_line_data = None
        self.prep_unlink_data = None
        self.analysis_settings = None
        self.analysis_process = None
        self.analysis_graph_file = None
        self.analysis_results = None

    @staticmethod
    def get_engine_name() -> str:
        return "depthmapXcli"

    def create_settings_widget(self, dock_widget):
        return DepthmapCLISettingsWidget(dock_widget)

    @staticmethod
    def getStartupInfo():
        # startupinfo is used in windows to suppress the
        # display of command-line windows when popen is called
        startupinfo = None
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return startupinfo

    @staticmethod
    def get_depthmap_cli() -> str:
        if platform.system() == "Windows":
            ext = "exe"
        elif platform.system() == "Darwin":
            ext = "darwin"
        elif platform.system() == "Linux":
            ext = "linux"
        else:
            raise ValueError("Unknown platform: " + platform.system())
        basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, "depthmapXcli/depthmapXcli." + ext)

    @staticmethod
    def ready() -> bool:
        cliFile = DepthmapCLIEngine.get_depthmap_cli()
        if not os.path.isfile(cliFile):
            return False
        if platform.system() == "Linux":
            if not os.access(cliFile, os.X_OK):
                print(
                    f"The file {cliFile} is not executable, trying to make it executable..."
                )
                st = os.stat(cliFile)
                os.chmod(cliFile, st.st_mode | stat.S_IEXEC)
                if not os.access(cliFile, os.X_OK):
                    print(f"Failed to make the file {cliFile} executable.")
                    return False
        return True

    @staticmethod
    def parse_result_file(result_file):
        values = []
        with open(result_file, newline="") as f:
            reader = csv.reader(f)
            first_row = True
            for row in reader:
                if first_row:
                    attributes = row
                    first_row = False
                else:
                    values.append(row)
        return attributes, values

    def get_line_data_csv(self, layers, settings):
        # get relevant QGIS layer objects
        axial = layers["map"]
        if axial != "":
            axial_layer = lfh.getLegendLayerByName(self.iface, axial)
        else:
            return None

        if layers["unlinks"] != "":
            unlinks_layer = lfh.getLegendLayerByName(self.iface, layers["unlinks"])
        else:
            unlinks_layer = ""
        # prepare analysis layers
        if settings["weight"]:
            weight_by = settings["weightBy"]
        else:
            weight_by = ""
        # look for user defined ID
        if settings["id"]:
            axial_id = settings["id"]
        else:
            axial_id = lfh.getIdField(axial_layer)
        # prepare map and unlinks layers
        if settings["type"] in (0, 1):
            axial_data = self.prepare_axial_map(
                axial_layer, settings["type"], axial_id, weight_by, ",", True
            )
            if axial_data == "":
                raise AnalysisEngine.AnalysisEngineError(
                    "The axial layer is not ready for analysis: verify it first."
                )
            if unlinks_layer:
                unlinks_data = self.prepare_unlinks(
                    axial_layer, unlinks_layer, axial_id, True, "\t", "\n", True
                )
            else:
                unlinks_data = ""
        else:
            axial_data = self.prepare_segment_map(
                axial_layer, settings["type"], axial_id, weight_by, ",", True
            )
            unlinks_data = ""
        return axial_data, unlinks_data

    @staticmethod
    def get_prep_commands(settings, unlinks_file_name):
        commands = []
        if settings["type"] == 0:
            commands.append(
                ["-m", "MAPCONVERT", "-co", "axial", "-con", "Axial Map", "-cir"]
            )
            if unlinks_file_name:
                commands.append(
                    [
                        "-m",
                        "LINK",
                        "-lm",
                        "unlink",
                        "-lt",
                        "coords",
                        "-lmt",
                        "shapegraphs",
                        "-lf",
                        unlinks_file_name,
                    ]
                )
        elif settings["type"] == 1:
            commands.append(
                ["-m", "MAPCONVERT", "-co", "axial", "-con", "Axial Map", "-coc"]
            )
            if unlinks_file_name:
                commands.append(
                    [
                        "-m",
                        "LINK",
                        "-lm",
                        "unlink",
                        "-lt",
                        "coords",
                        "-lmt",
                        "shapegraphs",
                        "-lf",
                        unlinks_file_name,
                    ]
                )
            commands.append(
                [
                    "-m",
                    "MAPCONVERT",
                    "-co",
                    "segment",
                    "-con",
                    "Segment Map",
                    "-cir",
                    "-coc",
                    "-crsl",
                    str(settings["stubs"]),
                ]
            )
        elif settings["type"] == 2:
            commands.append(
                [
                    "-m",
                    "MAPCONVERT",
                    "-co",
                    "segment",
                    "-con",
                    "Segment Map",
                    "-coc",
                    "-cir",
                ]
            )
        return commands

    def setup_analysis(self, layers, settings):
        self.prep_line_data, self.prep_unlink_data = self.get_line_data_csv(
            layers, settings
        )
        self.analysis_settings = settings
        if self.prep_line_data:
            return True
        return False

    def start_analysis(self):
        depthmap_cli = DepthmapCLIEngine.get_depthmap_cli()

        line_data_file = tempfile.NamedTemporaryFile("w+t", suffix=".csv", delete=False)
        line_data_file.write(self.prep_line_data)
        line_data_file.close()

        self.analysis_graph_file = tempfile.NamedTemporaryFile(
            "w+t", suffix=".graph", delete=False
        )
        process = subprocess.Popen(
            [
                depthmap_cli,
                "-f",
                line_data_file.name,
                "-o",
                self.analysis_graph_file.name,
                "-m",
                "IMPORT",
                "-it",
                "data",
            ],
            startupinfo=DepthmapCLIEngine.getStartupInfo(),
        )
        process.wait()
        os.unlink(line_data_file.name)

        unlink_data_file = tempfile.NamedTemporaryFile(
            "w+t", suffix=".tsv", delete=False
        )
        unlink_data_file.write(self.prep_unlink_data)
        unlink_data_file.close()

        prep_commands = DepthmapCLIEngine.get_prep_commands(
            self.analysis_settings, unlink_data_file.name
        )

        for prep_command in prep_commands:
            cli_command = [
                depthmap_cli,
                "-f",
                self.analysis_graph_file.name,
                "-o",
                self.analysis_graph_file.name,
            ]
            cli_command.extend(prep_command)
            process = subprocess.Popen(
                cli_command, startupinfo=DepthmapCLIEngine.getStartupInfo()
            )
            process.wait()

        os.unlink(unlink_data_file.name)

        command = DepthmapCLIEngine.get_analysis_command(self.analysis_settings)
        cli_command = [
            depthmap_cli,
            "-f",
            self.analysis_graph_file.name,
            "-o",
            self.analysis_graph_file.name,
            "-p",
        ]
        cli_command.extend(command)

        self.analysis_process = DepthmapCLIEngine.AnalysisThread(cli_command)
        self.analysis_process.start()

    def parse_progress(self, msg) -> Tuple[Optional[int], Optional[int], Optional[str]]:
        # calculate percent done
        p = re.compile(
            ".*?step:\\s?([0-9]+)\\s?/\\s?([0-9]+)\\s?record:\\s?([0-9]+)\\s?/\\s?([0-9]+).*?"
        )
        m = p.match(msg)
        # extract number of nodes
        if m:
            # string matches
            self.analysis_nodes = int(m.group(4))
            if self.analysis_nodes > 0:
                prog = int(m.group(3))
                step = int(m.group(1))
                relprog = int((float(prog) / float(self.analysis_nodes)) * 100)
                return step, relprog, ""
        return None, None, None

    class AnalysisThread(threading.Thread):
        def __init__(self, cmd):
            self.cmd = cmd
            self.p = None
            self.current_line = ""
            threading.Thread.__init__(self)

        def run(self):
            self.p = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=DepthmapCLIEngine.getStartupInfo(),
            )
            while True:
                self.current_line = self.p.stdout.readline()
                print("starttt " + self.current_line.decode("utf-8"))
                if not self.current_line:
                    break
            self.p.stdout.close()

    def get_progress(
        self, settings, datastore
    ) -> Tuple[Optional[int], Optional[int], Optional[str]]:
        rc = self.analysis_process.p.poll()
        if rc is None:
            # process still running
            # read the last line from it...
            output = self.analysis_process.current_line
            prg = self.parse_progress(str(output))
            return prg
        elif rc == 0:
            # process exited normally
            export_data_file = tempfile.NamedTemporaryFile(
                "w+t", suffix=".csv", delete=False
            )
            export_command = DepthmapCLIEngine.get_export_command()
            depthmap_cli = DepthmapCLIEngine.get_depthmap_cli()
            cli_command = [
                depthmap_cli,
                "-f",
                self.analysis_graph_file.name,
                "-o",
                export_data_file.name,
            ]
            cli_command.extend(export_command)
            process = subprocess.Popen(
                cli_command, startupinfo=DepthmapCLIEngine.getStartupInfo()
            )
            process.wait()

            attributes, values = self.parse_result_file(export_data_file.name)
            export_data_file.close()
            os.unlink(export_data_file.name)

            self.analysis_results = DepthmapEngine.process_analysis_result(
                settings, datastore, attributes, values
            )
            return 0, 100, "Completed"
        return None, None, None

    def cleanup(self):
        if os.path.isfile(self.analysis_graph_file.name):
            self.analysis_graph_file.close()
            os.unlink(self.analysis_graph_file.name)

    @staticmethod
    def get_analysis_command(settings):
        if settings["weight"]:
            weight_by = settings["weightBy"]
        else:
            weight_by = ""
        # get radius values
        radii = settings["rvalues"]
        #
        # prepare analysis user settings
        command = []
        # axial analysis settings
        if settings["type"] == 0:
            command.extend(["-m", "AXIAL"])
            command.extend(["-xa", str(radii)])
            if settings["betweenness"] == 1:
                command.append("-xac")
            if settings["fullset"] == 1:
                command.extend(["-xal", "-xar"])
            if weight_by != "":
                command.extend(["-xaw", settings["weightBy"].title()])
            # if unlinks_data != '':
            #     command += "acp.unlinkid:-1\n"
            #     command += "acp.unlinks:" + str(unlinks_data) + "\n"

        # 1: segment analysis settings with segmentation and unlinks
        # 2: segment analysis settings, data only
        elif settings["type"] in (1, 2):
            command.extend(["-m", "SEGMENT"])
            # command += "segment.stubs:" + str(settings['stubs']) + "\n"
            if settings["betweenness"] == 1:
                command.append("-sic")
            command.extend(["-st", "tulip"])
            command.extend(["-stb", "1024"])
            if settings["radiustype"] == 0:
                command.extend(["-srt", "steps"])
            elif settings["radiustype"] == 1:
                command.extend(["-srt", "angular"])
            elif settings["radiustype"] == 2:
                command.extend(["-srt", "metric"])
            else:
                raise BadInputError("Unknown radius type " + settings["radiustype"])

            command.extend(["-sr", str(radii)])
            if weight_by != "":
                command.extend(["-swa", settings["weightBy"].title()])
            # if unlinks_data != '':
            #     command += "acp.unlinkid:-1\n"
            #     command += "acp.unlinks:" + str(unlinks_data) + "\n"

        return command

    @staticmethod
    def get_export_command():
        return ["-m", "EXPORT", "-em", "shapegraph-map-csv"]
