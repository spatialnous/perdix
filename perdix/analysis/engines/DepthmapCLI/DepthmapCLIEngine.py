# SPDX-FileCopyrightText: 2020 Petros Koutsolampros <p.koutsolampros@spacesyntax.com>
# SPDX-FileCopyrightText: 2020 Space Syntax Ltd.
# SPDX-FileCopyrightText: 2024 - 2026 Petros Koutsolampros
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

from enum import Enum, auto
from queue import Queue

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
        self.currstep = -1

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

    def inDebugMode(self):
        return self.analysis_settings["debugMode"] == 1

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
        if settings["type"] == 0:  # axial
            commands.append({
                "name": "Converting to axial map",
                "nsteps": 1,
                "args": [
                    "-m", "MAPCONVERT",
                    "-co", "axial",
                    "-con", "Axial Map",
                    "-cir"
                ]
            })  # fmt: skip
            if unlinks_file_name:
                commands.append({
                    "name": "Linking",
                    "nsteps": 1,
                    "args": [
                        "-m", "LINK",
                        "-lm", "unlink",
                        "-lt", "coords",
                        "-lmt", "shapegraphs",
                        "-lf", unlinks_file_name,
                    ]
                })  # fmt: skip
        elif settings["type"] == 1:  # axial then segment
            commands.append({
                "name": "Converting to axial map",
                "nsteps": 1,
                "args": [
                    "-m", "MAPCONVERT",
                    "-co", "axial",
                    "-con", "Axial Map",
                    "-coc"
                ]
            })  # fmt: skip
            if unlinks_file_name:
                commands.append({
                    "name": "Linking",
                    "nsteps": 1,
                    "args": [
                        "-m", "LINK",
                        "-lm", "unlink",
                        "-lt", "coords",
                        "-lmt", "shapegraphs",
                        "-lf", unlinks_file_name,
                    ]
                })  # fmt: skip
            commands.append({
                "name": "Converting to segment map",
                "nsteps": 1,
                "args": [
                    "-m", "MAPCONVERT",
                    "-co", "segment",
                    "-con", "Segment Map",
                    "-cir",
                    "-coc",
                    "-crsl", str(settings["stubs"]),
                ]
            })  # fmt: skip
        elif settings["type"] == 2:  # segment
            commands.append({
                "name": "Converting to segment map",
                "nsteps": 1,
                "args": [
                    "-m", "MAPCONVERT",
                    "-co", "segment",
                    "-con", "Segment Map",
                    "-coc",
                    "-cir",
                ]
            })  # fmt: skip
        return commands

    def setup_analysis(self, layers, settings):
        self.prep_line_data, self.prep_unlink_data = self.get_line_data_csv(
            layers, settings
        )
        self.analysis_settings = settings
        if self.prep_line_data:
            return True
        return False

    def _setup_line_file(self, context):
        line_data_file = tempfile.NamedTemporaryFile("w+t", suffix=".csv", delete=False)
        line_data_file.write(self.prep_line_data)
        line_data_file.close()

        self.analysis_graph_file = tempfile.NamedTemporaryFile(
            "w+t", suffix=".graph", delete=False
        )
        return {
            "line_data_filename": line_data_file.name,
            "analysis_graph_filename": self.analysis_graph_file.name,
        }

    def _cleanup_line_file(self, context):
        if "line_data_filename" in context and os.path.exists(
            context["line_data_filename"]
        ):
            os.unlink(context["line_data_filename"])
        return {}

    def _setup_unlinks(self, context):
        unlink_data_filename = ""
        if self.prep_unlink_data:
            unlink_data_file = tempfile.NamedTemporaryFile(
                "w+t", suffix=".tsv", delete=False
            )
            unlink_data_file.write(self.prep_unlink_data)
            unlink_data_file.close()
            unlink_data_filename = unlink_data_file.name
        return {"unlink_data_filename": unlink_data_filename}

    def _cleanup_unlinks(self, context):
        if "unlink_data_filename" in context and os.path.exists(
            context["unlink_data_filename"]
        ):
            os.unlink(context["unlink_data_filename"])
        return {}

    def _setup_export(self, context):
        export_data_file = tempfile.NamedTemporaryFile(
            "w+t", suffix=".csv", delete=False
        )
        export_data_file.close()
        return {"export_data_filename": export_data_file.name}

    def _cleanup_export(self, context):
        if "export_data_filename" in context and os.path.exists(
            context["export_data_filename"]
        ):
            attributes, values = self.parse_result_file(context["export_data_filename"])
            os.unlink(context["export_data_filename"])
            return {"attributes": attributes, "values": values}
        return {}

    def start_analysis(self):
        depthmap_cli = DepthmapCLIEngine.get_depthmap_cli()

        cmdSets = []

        cmdSets.append({
            "setup": self._setup_line_file,
            "cmds": [{
                "name": "Importing lines to graph file",
                "nsteps": 1,
                "args": [
                    depthmap_cli,
                    "-f", "{line_data_filename}",
                    "-o", "{analysis_graph_filename}",
                    "-m", "IMPORT",
                    "-it", "data",
            ]}],
            "cleanup": self._cleanup_line_file
        })  # fmt: skip

        prep_commands = DepthmapCLIEngine.get_prep_commands(
            self.analysis_settings, "{unlink_data_filename}"
        )
        cli_commands = []
        for prep_command in prep_commands:
            cli_command = [
                depthmap_cli,
                "-f", "{analysis_graph_filename}",
                "-o", "{analysis_graph_filename}",
            ]  # fmt: skip
            cli_command.extend(prep_command["args"])

            cli_commands.append(
                {"name": prep_command["name"], "nsteps": 1, "args": cli_command}
            )

        cmdSets.append({
            "setup": self._setup_unlinks,
            "cmds": cli_commands,
            "cleanup": self._cleanup_line_file
        })  # fmt: skip

        cmdSets.append({
            "setup": lambda ctx: {
                'analysis_graph_filename':
                    ctx['analysis_graph_filename']
            },
            "cmds": [{
                "name": "Starting analysis",
                "nsteps": 1,
                "args": [
                    depthmap_cli,
                    "-f", "{analysis_graph_filename}",
                    "-o", "{analysis_graph_filename}",
                    "-p",
                ] + DepthmapCLIEngine.get_analysis_command(self.analysis_settings)
            }],
            "cleanup": lambda ctx: {}
        })  # fmt: skip

        cmdSets.append({
            "setup": self._setup_export,
            "cmds": [{
                "name": "Exporting to QGIS",
                "nsteps": 1,
                "args": [
                    depthmap_cli,
                    "-f", "{analysis_graph_filename}",
                    "-o", "{export_data_filename}",
                ] + DepthmapCLIEngine.get_export_command()
            }],
            "cleanup": self._cleanup_export,
        })  # fmt: skip

        self.analysis_process = DepthmapCLIEngine.AnalysisThread(
            cmdSets, self.inDebugMode()
        )
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

    # [{
    #     setup: function(),
    #     cmds: [],
    #     cleanup: function()
    # }]
    class AnalysisThread(threading.Thread):
        class State(Enum):
            NOT_STARTED = auto()
            RUNNING = auto()
            COMPLETED = auto()
            CANCELLED = auto()

        def __init__(self, cmdsets, inDebugMode):
            self.cmdsets = cmdsets
            self.cmdset = None  # current
            self.cmd = None  # current
            self.p = None
            self.maxlog = 5
            self.lastlog = []
            self.current_line = ""
            self.inDebugMode = inDebugMode
            self.context = {}
            self.state = self.State.NOT_STARTED
            self.step_queue = Queue()
            self.nsteps = 0
            self.nstepscmds = 0
            threading.Thread.__init__(self)

        def run(self):
            self.context = {}
            self.state = self.State.RUNNING
            self.step_queue = Queue()
            self.nsteps = 0
            self.nstepscmds = 0
            stepcount = 1
            for self.cmdset in self.cmdsets:
                self.nsteps += len(self.cmdset["cmds"])
                for self.cmd in self.cmdset["cmds"]:
                    self.nstepscmds += self.cmd["nsteps"] - 1
            for self.cmdset in self.cmdsets:
                if self.state == self.State.CANCELLED:
                    break
                if "setup" in self.cmdset:
                    self.context.update(self.cmdset["setup"](self.context))
                    del self.cmdset["setup"]
                for self.cmd in self.cmdset["cmds"]:
                    self.step_queue.put({"step": stepcount, "name": self.cmd["name"]})
                    if self.state == self.State.CANCELLED:
                        break
                    final_cmd = [c.format(**self.context) for c in self.cmd["args"]]
                    self.p = subprocess.Popen(
                        final_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=DepthmapCLIEngine.getStartupInfo(),
                    )
                    while True:
                        self.current_line = self.p.stdout.readline()
                        self.lastlog.append(self.current_line.decode("utf-8"))
                        if len(self.lastlog) > self.maxlog:
                            self.lastlog.pop(0)
                        if self.inDebugMode:
                            print("out:  " + self.current_line.decode("utf-8"))
                        if not self.current_line:
                            break
                    self.p.stdout.close()
                    stepcount = stepcount + 1
                if "cleanup" in self.cmdset:
                    self.context.update(self.cmdset["cleanup"](self.context))
                    del self.cmdset["cleanup"]
            self.cmdset = None
            self.state = self.State.COMPLETED

        def terminate(self):
            if self.state != self.State.COMPLETED and "cleanup" in self.cmdset:
                self.context.update(self.cmdset["cleanup"](self.context))
                del self.cmdset["cleanup"]
            self.context = {}
            self.p.terminate()
            self.state = self.State.CANCELLED

    def get_progress(
        self, settings, datastore
    ) -> Tuple[Optional[int], Optional[str], Optional[int], Optional[str]]:
        if self.analysis_process is None or self.analysis_process.p is None:
            return None, None, None, None
        # rc = self.analysis_process.p.poll()
        # if rc is None:
        if self.analysis_process.state == self.AnalysisThread.State.RUNNING:
            # process still running
            # read the last line from it...
            output = self.analysis_process.current_line
            prg = self.parse_progress(str(output))
            cmdstep = prg[0]
            if cmdstep is None:
                cmdstep = 0
            laststep = self.currstep
            allstepnames = []
            while not self.analysis_process.step_queue.empty():
                stepdata = self.analysis_process.step_queue.get()
                laststep = stepdata["step"]
                allstepnames.append(
                    "["
                    + str(stepdata["step"])
                    + "/"
                    + str(self.analysis_process.nsteps)
                    + "] "
                    + stepdata["name"]
                )
                if laststep != self.currstep:
                    self.currstep = laststep
            progress = prg[1]
            if progress is None and self.currstep >= 0:
                progress = 0
            return self.currstep + cmdstep, "\n".join(allstepnames), progress, prg[2]
        # elif rc == 0:
        elif self.analysis_process.state == self.AnalysisThread.State.CANCELLED:
            raise AnalysisEngine.AnalysisEngineError("User cancelled")
        elif self.analysis_process.state == self.AnalysisThread.State.COMPLETED:
            # process exited normally
            if "attributes" in self.analysis_process.context:
                attributes = self.analysis_process.context["attributes"]
            else:
                raise AnalysisEngine.AnalysisEngineError(
                    "attributes not found in context"
                    + "\n".join(self.analysis_process.lastlog)
                )

            if "values" in self.analysis_process.context:
                values = self.analysis_process.context["values"]
            else:
                raise AnalysisEngine.AnalysisEngineError(
                    "values not found in context"
                    + "\n".join(self.analysis_process.lastlog)
                )

            self.analysis_results = DepthmapEngine.process_analysis_result(
                settings, datastore, attributes, values
            )
            return 0, None, 100, "Completed"
        else:
            # process errored
            raise AnalysisEngine.AnalysisEngineError(
                "\n".join(self.analysis_process.lastlog)
            )
        return None, None, None, None

    def terminate(self):
        if self.analysis_process is not None:
            self.analysis_process.terminate()

    def cleanup(self):
        if self.analysis_process is not None:
            self.analysis_process = None
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
