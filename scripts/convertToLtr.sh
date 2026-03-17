# SPDX-FileCopyrightText: 2026 Petros Koutsolampros
#
# SPDX-License-Identifier: GPL-2.0-or-later

#!/bin/bash
sed -i 's/^name=.*/&-ltr/' metadata.txt
sed -i 's/^description=.*/& Version compatible with QGIS Long-term support version/' metadata.txt
