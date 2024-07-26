## ColorSpliceList - Multi-color printing via filament splicing

Experimental! Generates a 'cut list' for creating a long spliced filament with color changes prepared at specific lengths.

 * Note: The lengths in the generated 'cut list' does not match OrcaSlicer's... But OrcaSlicer seems to be incorrect. I need more testing.

Only supports OrcaSlicer and its filament change features.

Ensure the following settings under printer 'Multimaterial' settings:
 * Manual Filament Change: checked
 * Purge in prime tower: unchecked
 * Enable filament ramming: unchecked
 * Cooling tube position: 0
 * Cooling tube length: 0
 * Filament parking position: 0
 * Extra loading distance: 0
 * High extruder current... : unchecked

Also, under 'Extruder' settings:
 * Retraction when switching material - Length: 0 mm.

### Use

The script will output a -cutlist.txt file next to the .gcode file.

Add a line in "Post-processing scripts" in "Print Settings":

```
"C:\Program Files\Python311\python.exe" "C:\github\3dprint\ColorSpliceList\ColorSpliceList.py";
```

Note: You can also run this script manually from the command-line.

### Example cut list file

```
0	2156.89429
1	772.34441
2	267.81631
```
This means you should have 2157 mm of filament 0, 772 mm of filament 1, and 268 mm of filament 2. Maybe we need to put some other color before the first filament, so we know when the first color is 'at the nozzle' when starting the print. 

If running Klipper, any filament output by your start macro needs to be taken into account (added to the first length of filament).
