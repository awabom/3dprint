## Presets for SV04 in PrusaSlicer

NOTE: I've tested these presets on both johncarlson21's SV04 firmware (I used these on v2.1.3.1b3 initially) and on Bjoern70's firmware.

These presets are a work in progress.

There is no need to select mode with the printer display - the gcode will set the printer into the correct mode automatically, based on the selected 'Printer' in PrusaSlicer.

For the "Copy Mode" and "Mirror Mode" presets, the two extruders are for setting different filament temperatures in PrusaSlicer. Do not attempt to define extruder for different objects on the plate! (I don't know what happens)

The "Single Mode" and "Single Mode 2" printers differ only with a T0/T1 command to make the printer use the correct extruder.

The print settings-presets are available in two versions: "With Scripts" and 'without'. 
The "With Scripts" versions use my extra post-processing scripts to improve things that PrusaSlicer does not currently handle well:

 * Cooling an extruder when it has nothing left to print in the gcode - IDEXEarlyShutoff.py
 * Pre-heating the extruder before it becoming active - IDEXPreheat.py
 * Modifying travel-after to travel-before M600 color change to avoid new color blob on early part - FixM600.py fixes this.
 
The presets (all version) also slow down the tool change retraction to 20 mm/s. This was recommended by several sources (e.g. @tobycwood on Prusa forums)

### Installation

On Windows, the "PrusaSlicer" folder is at "%APPDATA%\PrusaSlicer".
