# SPDX-FileCopyrightText: 2014 - 2015 Jorge Gil <jorge.gil@ucl.ac.uk>
# SPDX-FileCopyrightText: 2014 - 2015 UCL
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
This script initializes the plugin, making it known to QGIS.
"""

from __future__ import absolute_import


def classFactory(iface):
    from .Perdix import Perdix
    return Perdix(iface)
