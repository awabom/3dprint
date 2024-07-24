## ColorSpliceList - Multi-color printing via filament splicing

Experimental! Generates a 'cut list' for creating a long spliced filament with color changes prepared at specific lengths.

### Use

The script will output a .txt file next to the .gcode file.

Add a line in "Post-processing scripts" in "Print Settings":

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\ColorSpliceList\ColorSpliceList.py";
```

...and make sure you have "Manual Filament Change" checked in the printer Multimaterial settings tab.

Note: You can also run this script manually from the command-line.