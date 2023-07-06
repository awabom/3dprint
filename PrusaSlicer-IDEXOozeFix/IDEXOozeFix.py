#!/usr/bin/env python3

# -------------------------------------------------------------------------------------
# PrusaSlicer post-processor script: Unretract the first custom ooze-preventing retract
# -------------------------------------------------------------------------------------

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
  
# Example: G1 E-5 F1200 ; CUSTOM RETRACT - UNDO T1: G1 E5 F2400

regex_undo = re.compile('.*CUSTOM RETRACT - UNDO (?P<tool>T[\d]+): (?P<undo>.*)') # Matches a retract that should be unretracted
regex_m109 = re.compile('^M109 .*(?P<tool>T[\d]+).*') # Matches a heat-and-wait command

outputLines = []

undoDone = False
undoTool = None
undoCommand = None

for lineNum in range(len(inputLines)):
  inputLine = inputLines[lineNum]
  outputLines.append(inputLine)
  
  if not undoDone:
    undoMatch = regex_undo.match(inputLine)
    if bool(undoMatch):
      undoTool = undoMatch.group('tool')
      undoCommand = undoMatch.group('undo')
      continue
  
    m109Match = regex_m109.match(inputLine)
    if bool(m109Match):
      heatTool = m109Match.group('tool')
      if heatTool == undoTool:
        outputLines.append(undoCommand + '\n')
        undoDone = True

# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)
  