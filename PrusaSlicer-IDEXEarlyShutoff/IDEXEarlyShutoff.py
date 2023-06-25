#!/usr/bin/env python3

# --------------------------------------------------------------------------------------------
# PrusaSlicer post-processor script: Turn off nozzle when nozzle is not used for rest of print
# --------------------------------------------------------------------------------------------

import sys
import re
import os
import io
import subprocess

# Path to g-code file from command-line
gcodeFile = sys.argv[len(sys.argv)-1]

# Read g-code into memory
with open(gcodeFile, "r") as f:
  inputLines = f.readlines()

regex_toolchange = re.compile('^(?P<tool>T[\d]+).*') # Matches a tool-change command

toolUseLastLine = {}

# 1st pass: Go through lines and look for tool changes
for lineNum, inputLine in enumerate(inputLines):
  toolMatch = regex_toolchange.match(inputLine)
  if bool(toolMatch):
    toolKey = toolMatch.group('tool')
    toolUseLastLine[toolKey] = lineNum

outputLines = []

# 2nd pass: Go though lines, add to output. If last use of tool ends - cool it down
currentTool = None
for lineNum, inputLine in enumerate(inputLines):
  outputLines.append(inputLine)

  toolMatch = regex_toolchange.match(inputLine)
  if bool(toolMatch):
    nextTool = toolMatch.group('tool')

    if currentTool != None and nextTool != currentTool:
      if toolUseLastLine[currentTool] < lineNum:
        outputLines.append('M104 S0 ' + currentTool + ' ; Early Shutoff of nozzle\n')
        
    currentTool = nextTool

# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)
  