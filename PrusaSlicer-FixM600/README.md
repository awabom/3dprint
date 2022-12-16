## FixM600.py - Improves/fixes PrusaSlicer M600 commands

The default behavior of PrusaSlicer 2.5.0 does the color change at the end of the layer - before traveling to the next print position of the next layer. 
This can leave a blob in the previous layer when the printer resumes after color change.

This post-processing script moves the M600 command to right before the first extrusion of the next layer. 
Additionally, you can prime the nozzle after color change, using an extra g-code command.

Tested using an Ender-3 V2 with "Professional Firmware" (mriscoc).

### Use

Add a line in "Post-processing scripts" in "Print Settings":

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\FixM600.py";
```

In addition to moving the M600 command, you can also prime the nozzle with an extra extrusion:

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\FixM600.py" "G1 E6 F2400";
```