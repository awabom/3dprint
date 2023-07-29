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
regex_toolchange = re.compile('^(?P<tool>T[\d]+).*') # Matches a tool change command
regex_toolzhop = re.compile('^;TOOL_Z_HOP: (?P<hop>.*)') # Matches a tool change z-hop
regex_toolunhop = re.compile('^;TOOL_Z_UNHOP.*') # Matches a 'enable unhop' trigger
regex_movez = re.compile('^(?P<zmove>G1 Z.*)') # Matches a move that changes z (PrusaSlicer only does these separately, currently...)

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
  else: # Check for tool change command
    toolMatch = regex_toolchange.match(inputLine)
    if bool(toolMatch):
      heatTool = toolMatch.group('tool')
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

# 3rd pass - z-hop on tool change (currently does not z-hop that much if on layer change)
inputLines = outputLines
outputLines = []
currentZmove = None
duringZhop = False
doUnhop = False

for lineNum in range(len(inputLines)):
  inputLine = inputLines[lineNum]
  
  # Check for tool change z-hop so we can ignore it (it should not affect our 'z unhop'
  matchToolZhop = regex_toolzhop.match(inputLine)
  if bool(matchToolZhop):
    inputLine = matchToolZhop.group('hop') + '\n'
    duringZhop = True
    doUnhop = False
  else:
    # Search for z moves so we know the z coordinate
    matchMoveZ = regex_movez.match(inputLine)
    if bool(matchMoveZ):
      currentZmove = matchMoveZ.group('zmove')
      # Disable the z-move if we're going to unhop later
      if doUnhop:
        inputLine = '; disabled in z-hop: ' + inputLine
    elif duringZhop:
      if not doUnhop: # unhop is not yet enabled (still in tool change)
        doUnhopMatch = regex_toolunhop.match(inputLine)
        doUnhop = bool(doUnhopMatch)
      else: # unhop enabled - check for first extrude command
        extrudeMatch = regex_extrude.match(inputLine)
        if bool(extrudeMatch):
          outputLines.append(currentZmove + ' ; un-z-hop\n')
          duringZhop = False
          doUnhop = False
        
  outputLines.append(inputLine)



# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)
  