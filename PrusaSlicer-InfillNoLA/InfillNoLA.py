#!/usr/bin/env python3

# ---------------------------------------------------------------------
# PrusaSlicer post-processor script disabling linear advance for infill
# ---------------------------------------------------------------------

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

regex_m900 = re.compile('^M900 K.*') # Matches a linear-advance command (the 'normal' setting to use except for infill)

regex_typeInfill = re.compile('^;TYPE:(Internal infill)') # Matches start of infill section
regex_typeOther = re.compile('^;TYPE:(?!Internal infill)') # Matches start of not-infill section
regex_typeExtrusion = re.compile('^G1.*E.*') # Matches extrusion (any extrusion value)

outputLines = []
matchedM900 = None

kZero = False
kZeroOutput = False

# Go through lines and look for M900, save it and use for all non-infill sections
for inputLine in inputLines:
  if bool(regex_typeInfill.match(inputLine)) and not kZero: # Start of infill 
    kZero = True
    kZeroOutput = False
  elif bool(regex_m900.match(inputLine)): # M900 command already in gcode - use for 'non-infill'
    matchedM900 = inputLine
    kZero = False
  elif bool(regex_typeOther.match(inputLine)) and matchedM900 != None and kZero:
    outputLines.append(matchedM900)
    outputLines.append("\n")
    kZero = False
  
  outputLines.append(inputLine)
  
  # After first extrusion of infill, disable linear advance
  if bool(regex_typeExtrusion.match(inputLine)) and kZero and not kZeroOutput:
    outputLines.append("M900 K0\n")
    kZeroOutput = True

# Output modified g-code to file
with open(gcodeFile, "w") as f:
  f.writelines(outputLines)