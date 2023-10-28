# Start GCodeMover
# Åke Wallebom

import re
from ..Script import Script


class StartGCodeMover(Script):
    """Moves Cura-generated temperature codes from before the start g-code, to after. Mark start section with '; BEGINSTARTGCODE' and '; ENDSTARTGCODE'
    """

    def getSettingDataString(self):
        return """{
            "name": "Start G-Code Mover",
            "key": "StartGCodeMover",
            "metadata": {},
            "version": 2,
            "settings":
            {
            }
        }"""

    def execute(self, data):
        regexStart = re.compile("; BEGINSTARTGCODE")
        regexEnd = re.compile("; ENDSTARTGCODE")
        regexMove = re.compile("(M10[49] .*|M105$)")
        
        movelines = []
        
        foundStart = False
        foundEnd = False
        
        for layer_index, layer in enumerate(data):
            lines = data[layer_index].split("\n")
            outputLines = []
            for line_index, line in enumerate(lines):
            
                outputLine = line

                # Not already done?
                if not foundEnd:
                    # Reached beginning of start g-code?
                    startMatch = regexStart.match(line)
                    if bool(startMatch):
                        foundStart = True

                    # Not found start g-code yet, check for commands to move
                    if not foundStart:
                        moveMatch = regexMove.match(line)
                        if bool(moveMatch):
                           movelines.append(line)
                           outputLine = "; Moved by Start G-Code Mover: " + line
                    else:
                        endMatch = regexEnd.match(line)
                        if bool(endMatch):
                           foundEnd = True
                           
                    if foundEnd:
                        outputLines.append("; Moved here by Start G-Code Mover:")
                        outputLines.extend(movelines)
                    
                outputLines.append(outputLine)
                    
            
            data[layer_index] = "\n".join(outputLines)
            
            if foundEnd:
                break
        
        return data
