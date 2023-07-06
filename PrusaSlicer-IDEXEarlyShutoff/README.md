## IDEXEarlyShutoff.py - Turns off nozzle heat when not used in rest of print

PrusaSlicer does not cool down unused nozzles to zero until the end of a print.

This post-processing script turns off heating for any nozzle that is not used any more for the rest of the print.

### Use

Add a line in "Post-processing scripts" in "Print Settings":

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\PrusaSlicer-IDEXEarlyShutoff\IDEXEarlyShutoff.py";
```
