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

currentCutSum = Decimal(0)
currentCutList = 'unknown'

regex_cutlist = re.compile('^; MANUAL_TOOL_CHANGE T(?P<cut>.*)') # Cut list comment
regex_disable = re.compile('^M600( .*)?') # Commands to comment out
regex_extrusion = re.compile('^G1( .*)? E(?P<length>[^ ]*)') # G1 with extrusion

outputLines = []
cutLines = []

# Go through file and count all extrusions between 'cut_list' comments, and comment out all 'disable' commands
for inputLine in inputLines:
  if bool(regex_disable.match(inputLine)): # Something to disable found - comment it out
    outputLines.append('; ' + inputLine)
  else:
    outputLines.append(inputLine)
    
    extMatch = regex_extrusion.match(inputLine)
    cutMatch = regex_cutlist.match(inputLine)
    if bool(extMatch):
      extLength = Decimal(extMatch.group('length'))
      currentCutSum += extLength
    elif bool(cutMatch):
      if currentCutSum > 0:
        cutLines.append(currentCutList + "\t" + str(currentCutSum) + "\n")
      currentCutList = cutMatch.group('cut')
      currentCutSum = 0

cutLines.append(currentCutList + "\t" + str(currentCutSum) + "\n")


# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)
  
# Output cutlist to file
with open(cutFile, "w") as f:
  f.writelines(cutLines)
