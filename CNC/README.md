## CNC conversion for Ender 3 V2 using a Dremel

Very early version... proceed with CAUTION.

NOTE: The g-code currently gets one G1 Z-move at the very start of the print. This makes the tool plunge straight down into the midpoint. This line must be removed manually before running the g-code!

### Hardware steps

We'll keep the thermistors plugged in, to avoid having firmware issues. So keep both the hot-end thermistor and the bed thermistor.

Remove the whole hot-end assembly from the X-gantry carriage. Make sure not to damage the thermistor!
Pull the thermistor cable out of the wire loom. Bundle it up and put inside the motherboard enclosure.
Remove heater power cables for bed and hot-end.

I connected the part cooling output to the motherboard fan (This is pretty much how it is stock on the Ender 3 V2). The heat-brake fan was disconnected.

Print and mount the Dremel-clamp (check the Parts folder here)

### Software steps

Copy the PrusaSlicer profiles into your %APPDATA%\PrusaSlicer directory. 
You should now have new printers, a cnc 'filament', and some different Print Settings.

### How to

Mount material on print bed.
Lower the tool down so it touches the material at the zero position x=y=0.
Start the print.
Wait until the gantry is raised and the printer pauses.
Turn on Dremel.
Press button on printer so it continues.

Take cover... ;D

NOTE: If you need to stop the print - do NOT use the printer's stop feature - instead CUT THE POWER. Otherwise, the printer may auto-home and take a path straight through the material being cut.
