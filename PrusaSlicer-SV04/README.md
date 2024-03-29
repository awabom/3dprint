## Presets for SV04 in PrusaSlicer

NOTE: I've tested these presets on both johncarlson21's SV04 firmware (I used these on v2.1.3.1b3 initially) and on Bjoern70's firmware.

These presets are a work in progress.

There is no need to select mode with the printer display - the gcode will set the printer into the correct mode automatically, based on the selected 'Printer' in PrusaSlicer.

For normal single-color printing and dual-color printing: Use 'Dual and Single' printer preset. I personally currently use the 'Beta' profile the most.
By using only one extruder on the plate, the other extruder will be inactive during the print (So no Single 1/2 profiles are needed).

For the "Copy Mode" and "Mirror Mode" presets, the two extruders are for setting different filament temperatures in PrusaSlicer. Do not attempt to define extruder for different objects on the plate! (I don't know what happens)

The print settings-presets are available in two versions: "With Scripts" and 'without'. 
The "With Scripts" versions use my extra post-processing scripts to improve things that PrusaSlicer does not currently handle well:

 * Cooling an extruder when it has nothing left to print in the gcode - IDEXEarlyShutoff.py
 * Pre-heating the extruder before it becoming active - IDEXPreheat.py
 * Modifying travel-after to travel-before M600 color change to avoid new color blob on early part - FixM600.py fixes this.
 
The presets (all version) also slow down the tool change retraction to 20 mm/s. This was recommended by several sources (e.g. @tobycwood on Prusa forums)

### Installation

To use these profiles with all the scripts, follow these steps:

1. Install Python 3.11.x - Make sure you install for "All Users", not just for the current account

https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

(found on https://www.python.org/downloads/)

2. Download this whole repository from:

https://github.com/awabom/3dprint/archive/refs/heads/main.zip

3. Unzip the file, placing all the 'PrusaSlicer-'... folder into "C:\github\3dprint", so e.g. the "C:\github\3dprint\PrusaSlicer-IDEXOozeFix"
should now contain a 'IDEXOozeFix.py' file.

4. Copy all PS presets from "C:\github\3dprint\PrusaSlicer-SV04\PrusaSlicer" to "%APPDATA%\PrusaSlicer" (just copy/paste this folder path into file explorer address bar and it will change to the actual folder).

5. Done! Start PrusaSlicer and select the SV04 presets and print... hopefully :)
