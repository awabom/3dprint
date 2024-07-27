#!/usr/bin/env python3

# ------------------------------------------------------------------------------------------------------------------
# OrcaSlicer post-processor script creating filament splicing cut list from MANUAL_TOOL_CHANGE and M600 color change
# ------------------------------------------------------------------------------------------------------------------

import sys
import re
import os
import io
import subprocess
from decimal import Decimal

# Path to g-code file from command-line
gcodeFile = sys.argv[len(sys.argv)-1]

slicerOutName = os.getenv('SLIC3R_PP_OUTPUT_NAME')
if slicerOutName is None:
  cutFile = gcodeFile 
else:
  cutFile = slicerOutName
  
cutFile += "-cutlist.txt"

# Read g-code into memory
with open(gcodeFile, "r") as f:
  inputLines = f.readlines()

currentSum = Decimal(0)
currentPrintSum = Decimal(0)
currentCutList = None
nextCutList = None

regex_change = re.compile('^; MANUAL_TOOL_CHANGE T(?P<cut>.*)') # Tool change
regex_towerend = re.compile('^; CP TOOLCHANGE END') # Wipe tower end
regex_disable = re.compile('^M600( .*)?') # Commands to comment out
regex_extrusion = re.compile('^G1( .*)? E(?P<length>[^ ]*)') # G1 with extrusion

outputLines = []
cutLines = []

# Sum extrusions and produce a cut list
for inputLine in inputLines:
  if bool(regex_disable.match(inputLine)): # Something to disable found - comment it out
    outputLines.append('; ' + inputLine)
  else:
    outputLines.append(inputLine)
    
    extMatch = regex_extrusion.match(inputLine)
    changeMatch = regex_change.match(inputLine)
    towerMatch = regex_towerend.match(inputLine)
    
    if bool(extMatch): # Is this an extrusion move? Just add it to sum
      extLength = Decimal(extMatch.group('length'))
      currentSum += extLength
    elif bool(changeMatch): # Found filament change
      tool = changeMatch.group('cut')
      if currentCutList is None: # First filament change command?
        currentCutList = tool
        if currentSum > 0: # There may be extrusions in the start g-code before manual filament change
          cutLines.append("initial\t" + str(currentSum) + "\n")
          currentSum = Decimal(0)
      else:
        nextCutList = tool
        
      # Store current "print moves sum" - used later when prime tower end is found
      currentPrintSum = currentSum
      currentSum = Decimal(0)
    elif bool(towerMatch) and nextCutList != currentCutList: # found end of prime tower after a tool change, split the tower extrusions in half
      split = currentSum / Decimal(2)
      cutLines.append(currentCutList + "\t" + str(currentPrintSum + split) + "\n")
      currentCutList = nextCutList
      currentSum = split
      currentPrintSum = Decimal(0)

# Any extra extrusions left (no prime tower at end of print to detect)
cutLines.append(currentCutList + "\t" + str(currentPrintSum + currentSum) + "\n")

# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)
  
# Output cutlist to file
with open(cutFile, "w") as f:
  f.writelines(cutLines)
