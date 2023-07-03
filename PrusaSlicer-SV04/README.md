## Presets for SV04 in PrusaSlicer

NOTE: These presets probably requires John Carlson's SV04 firmware (I used these on v2.1.3.1b3 initially)
These presets are a work in progress. They work kind of ok, but there's room for improvement, especially with the tool changing. Currently, both nozzles stay heated for faster switching.

There is no need to select mode with the printer display - the gcode will set the printer into the correct mode automatically.

For the "Copy Mode" and "Mirror Mode" presets, the two extruders are for setting different filament temperatures in PrusaSlicer. Do not attempt to define extruder for different objects on the plate! (I don't know what happens)

The "Single Mode" and "Single Mode 2" printers differ only with a T0/T1 command to make the printer use the correct extruder.

The print settings-presets use some of my other scripts from GitHub - If you don't want to use those scripts, just remove them from "Print Settings" - "Output options" - "Post-processing scripts".

### Installation

On Windows, the "PrusaSlicer" folder is at "%APPDATA%\PrusaSlicer".
