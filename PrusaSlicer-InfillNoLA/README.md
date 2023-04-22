## InfillNoLA.py - Disables Linear Advance when printing infill

This post-processing script disables linear advance when printing 'Internal infill' by setting the K-factor to 0, then restores the previous K-factor when not printing infill.

### Use

Add a line in "Post-processing scripts" in "Print Settings":

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\InfillNoLA.py";
```
