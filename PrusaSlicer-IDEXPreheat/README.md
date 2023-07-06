## IDEXPreheat.py - Pre-heats nozzle a bit before it will start printing

Experimental code!

PrusaSlicer does not heat up the nozzle until just before it should start printing, when using the ooze-prevention feature (unlike Cura...)

This post-processing script starts heating the nozzle to final printing temperature 1-2 minutes before that tool will start printing.
Requires the 'Ooze prevention' feature to be enabled under 'Multiple Extruders' in print settings.

### Use

Add a line in "Post-processing scripts" in "Print Settings":

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\PrusaSlicer-IDEXPreheat\IDEXPreheat.py";
```
