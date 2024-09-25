# SPDX-FileCopyrightText: 2024 Petros Koutsolampros
# 
# SPDX-License-Identifier: GPL-2.0-or-later

#!/bin/python3

import sys, subprocess, re
from datetime import datetime

reusedata = subprocess.check_output(["reuse", "spdx"])
reusedata = reusedata.decode("utf-8").splitlines();

if len(sys.argv) < 2:
    sys.exit('Error: No files provided')

filesNeeded = [sys.argv[1]]


cprPrefix = "SPDX-FileCopyrightText:"

fileData = {}

currentFile = ""
cprs = []

for line in reusedata:
    if line.startswith("FileName:"):
        fileName = line[len("FileName:"):].strip()
        if fileName in filesNeeded:
            fileData[fileName] = {"maxyear": 1900}
            currentFile = fileName
        else:
            currentFile = ""
    elif (currentFile != "" and line != ""):
        if line.startswith("FileCopyrightText:"):
            cprs = [line[len("FileCopyrightText:"):].strip()]
            if not cprs[0].startswith("<text>"):
                cprs = []
                continue
            cprs[0] = cprs[0][len("<text>"):].strip()
            if not cprs[0].startswith(cprPrefix):
                cprs = []
                continue
            if cprs[0].endswith("</text>"):
                cprs[0] = cprs[0][len(cprPrefix):
                    len(cprs[0]) - len("</text>")].strip()
                fileData[currentFile]["copyright"] = cprs
                cprs = []
                continue;
        elif cprs != []:
            if line.endswith("</text>"):
                line = line[:len(line) - len("</text>")].strip()
                cprs.append(line)
                for i in range(len(cprs)):
                    cprs[i] = cprs[i][len(cprPrefix):].strip()
                fileData[currentFile]["copyright"] = cprs
                cprs = []
            else:
                cprs.append(line)
nocpr = []

for fd in fileData:
    if "copyright" not in fileData[fd]:
        nocpr.append(fd)
        continue
    for cpr in fileData[fd]["copyright"]:
        m = re.match("[12][0-9]{3}\s?-\s?([12][0-9]{3}).*?", cpr)
        if m:
            year = int(m.group(1))
            if year > 1900 and year > fileData[fd]["maxyear"]:
                fileData[fd]["maxyear"] = year
        else:
            m = re.match("([12][0-9]{3}).*?", cpr)
            if m:
                year = int(m.group(1))
                if year > 1900 and year > fileData[fd]["maxyear"]:
                    fileData[fd]["maxyear"] = year

for item in nocpr:
    fileData.pop(item, None)
    print("Skipping file: " + item)

if len(fileData) == 0:
    print("No files left to process...")
    exit()

for fd in fileData:
    if fileData[fd]["maxyear"] < datetime.now().year:
        sys.exit('File ' + fd + " has not had its Copyright " +
            "statement updated to this year (" + str(datetime.now().year) +
            "), only goes up to " + str(fileData[fd]["maxyear"]))
print("Test passed")