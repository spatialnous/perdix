# SPDX-FileCopyrightText: 2014 - 2015 Jorge Gil <jorge.gil@ucl.ac.uk>
# SPDX-FileCopyrightText: 2014 - 2015 UCL
# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import print_function

from qgis.PyQt.QtWidgets import QMessageBox


# ------------------------------
# General functions
# ------------------------------
# Display an error message via Qt message box
def pop_up_error(msg=""):
    # newfeature: make this work with the new messageBar
    QMessageBox.warning(None, "error", "%s" % msg)


# ------------------------------
# Canvas functions
# ------------------------------
# Display a message in the QGIS canvas
def showMessage(iface, msg, type="Info", lev=1, dur=2):
    iface.messageBar().pushMessage(type, msg, level=lev, duration=dur)


def getCanvasColour(iface):
    colour = iface.mapCanvas().canvasColor()
    return colour
