#!/usr/bin/env python3

# -------------------------------------------------------------------------------------------------------------------
# PrusaSlicer post-processor script: Unretract the first custom ooze-preventing retract and/or add EXTRAPRIME priming
# -------------------------------------------------------------------------------------------------------------------

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
  
# Example in start g-code from custom printer profile: G1 E-5 F1200 ; CUSTOM RETRACT - UNDO T1: G1 E5 F2400

# Example of first tool change: 
# M109 S245 T1 ; set temperature and wait for it to be reached
# ; printing object shape id:0 copy 0
# G1 E-1.5
# G1 X158.109 Y134.448 F7200
# G1 E1.5 F2400
# ;TYPE:External perimeter

# Goal:
# M109 S245 T1 ; set temperature and wait for it to be reached
# ; printing object shape id:0 copy 0
# G1 E-1.5
# G1 X158.109 Y134.448 F7200
# G1 E5 F2400 ; OozeFix
# G1 E1.5 F2400
# ;TYPE:External perimeter


regex_undo = re.compile('.*CUSTOM RETRACT - UNDO (?P<tool>T[\d]+): (?P<undo>.*)') # Matches a retract that should be unretracted for a specific tool
regex_extraprime = re.compile('.*EXTRAPRIME: (?P<prime>.*)') # Matches an 'extraprime' command to apply before first extrude
regex_extrude = re.compile('^G1.*E[^\-].*') # Matches a G1 command that extrudes
regex_m109 = re.compile('^M109 .*(?P<tool>T[\d]+).*') # Matches a heat-and-wait command

# 1st pass - Handle the first 'oozefix' retraction

outputLines = []

undoDone = False
undoTool = None
undoCommand = None

undoOnExtrude = False

for lineNum in range(len(inputLines)):
  inputLine = inputLines[lineNum]
  outputLines.append(inputLine)
  
  if undoDone:
    continue
  
  if undoTool is None:
    undoMatch = regex_undo.match(inputLine)
    if bool(undoMatch):
      undoTool = undoMatch.group('tool')
      undoCommand = undoMatch.group('undo')
  elif undoOnExtrude:
    extrudeMatch = regex_extrude.match(inputLine)
    if bool(extrudeMatch):
      outputLines.insert(len(outputLines)-1, undoCommand + '\n')
      undoDone = True
  else: # Check for heat-and-wait command
    m109Match = regex_m109.match(inputLine)
    if bool(m109Match):
      heatTool = m109Match.group('tool')
      if heatTool == undoTool:
        undoOnExtrude = True


# 2nd pass - Handle any 'EXTRAPRIME' entries
inputLines = outputLines
outputLines = []
extraPrime = None
        
for lineNum in range(len(inputLines)):
  inputLine = inputLines[lineNum]
  
  extraMatch = regex_extraprime.match(inputLine)
  if bool(extraMatch):
    extraPrime = extraMatch.group('prime')
  elif not (extraPrime is None):
    extrudeMatch = regex_extrude.match(inputLine)
    if bool(extrudeMatch):
      outputLines.append(extraPrime + '\n')
      extraPrime = None
      
  outputLines.append(inputLine)

# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)
  