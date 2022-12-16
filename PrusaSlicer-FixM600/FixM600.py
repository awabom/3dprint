#!/usr/bin/env python3

# -----------------------------------------------------------------------------------------------------
# PrusaSlicer post-processor script improving M600 color change for the Professional Firmware (mriscoc)
# -----------------------------------------------------------------------------------------------------

import sys
import re
import os
import io
import subprocess

# Path to g-code file from command-line
gcodeFile = sys.argv[len(sys.argv)-1]

if len(sys.argv) == 3:
  afterM600 = sys.argv[1]
else:
  afterM600 = None

# Read g-code into memory
with open(gcodeFile, "r") as f:
  inputLines = f.readlines()
  
regex_m600 = re.compile('^M600($| .*)') # Just an M600 command
regex_extrusion = re.compile('^G1( .*)? E[^-].*') # G1 with non-negative E-value

outputLines = []
matchedM600 = None

# Go through lines and look for M600 and move it to a later point - before the next extrusion
for inputLine in inputLines:
  if not matchedM600:
    if bool(regex_m600.match(inputLine)): # M600 in input - keep the line for later
      matchedM600 = inputLine
    else: # Not an M600 - just output
      outputLines.append(inputLine)
  else: # Have seen M600 - check for first positive extrusion - output M600 before it
    if bool(regex_extrusion.match(inputLine)): 
      outputLines.append(matchedM600)
      matchedM600 = None
      if afterM600:
        outputLines.append(afterM600)
        outputLines.append("\n")
    outputLines.append(inputLine)

# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)