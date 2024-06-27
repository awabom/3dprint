## Sovol SV08 - Notes

These are my changes made to the SV08 config, using firmware version 2.3.3 as a starting point.

USE AT YOUR OWN RISK. This is only tested on my personal machine. If your printer breaks, don't blame me.
The 'skew correction' stuff is the newest and most lightly tested addition.

### saved_variables.cfg

Make sure you have no manual z-offset adjustment:

	offsetadjust = 0

Note to self: ...and in the future remember to reset this value again if you adjust the offset manually directly on the printer.

### macro.cfg

 * Raised & colder nozzle cleaning: I think the nozzle cleaning digs the nozzle a bit to much into the cleaning pad. Some parts were ripped off after just 2 cleaning cycles.
 * Calibration of z-offset each print.
 * Using parameters to 'START_PRINT' from slicer (see start g-code below)
 * New start sequence: Heating bed to target temperature before homing and calibration of z-offset.
 * Handling of skew_correction (turn off/on at the correct times, hopefully)
 * A bit more flush volume for filament change
 
 See complete [macro.cfg](macro.cfg)

### printer.cfg

#### Input Shaper

Under the "input_shaper" section, I manually entered the results from the 'Belt tuning' sequence. 
It seems the menu option does not save the correct 'shaper_type' setting after belt tuning. 
I also manually entered the correct frequency values here to be safe (the sovol command will save the values in the separate "saved_variables.cfg" file.

#### PID tuning

After 

	PID_CALIBRATE HEATER=extruder TARGET=240
	SAVE_CONFIG
	
...the updated values will be at the bottom of printer.cfg 

I also did

	PID_CALIBRATE HEATER=heater_bed TARGET=80
	SAVE_CONFIG

#### Skew Correction

After (and maybe before?) belt tuning, it prints askew. See [skew correction](https://www.klipper3d.org/Skew_Correction.html).
Enable with an empty "skew_correction" section in printer.cfg:

	[skew_correction]

To create a skew correction profile run the following using the console (with my example values):

	SET_SKEW XY=141.5,141.0,99.9
	SKEW_PROFILE SAVE=my_skew_profile
	SAVE_CONFIG
	
Then the macro.cfg will automatically load it at the proper times.... I hope.

### Orca Slicer profile (Based on Voron 2.4 350)

 * Printable height: 345
 * Probe point distance, X & Y: 30
 * Machine start G-Code: Use the one from below under "Based on Sovol's"
 * Machine end G-code:

	END_PRINT
	TIMELAPSE_TAKE_FRAME
	
 * Change filament g-code

	M600
	
 * Extruder - Retraction - Length: 0.5
 * Z-hop when retracting: 0.2
 * Z-hop-type: Auto
 * Emit limits to G-code: unchecked
 * Speed Values: X 700, Y 700, Z 20, E 50. 
 * Accel Limits: X 40000, Y 40000
 * Jerk: X 20, Y 20, Z 0.5, E 5

The print settings I use are mostly based on Voron-presets, but with increased accelerations and speeds taken from Sovol's Orca Profiles (see below)


### Orca Slicer profile (Based on Sovol's)

I used Sovol's official Orca Slicer profile (from the Google Drive folder). Then made the following changes:

#### Basic - Advanced - G-code thumbnails

Only one size:

	400x300

#### Start G-Code

 * Warning: To use this start g-code you MUST use my macro.cfg

 * Note 1: At the end of the start g-code, there is a section of if-statements. This adjusts the z-offset to my liking based on material. I guess the values will differ for you.

 * Note 2: Due to changes in the priming sequence, I use 5 skirt lines as extra priming in my print profiles.

Code:

	START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]

	{if filament_type[initial_extruder] == "PETG"}
	SET_GCODE_OFFSET Z_ADJUST=0.1
	{elsif filament_type[initial_extruder] == "ABS"}
	SET_GCODE_OFFSET Z_ADJUST=-0.025
	{elsif filament_type[initial_extruder] == "ASA"}
	SET_GCODE_OFFSET Z_ADJUST=-0.025
	{else}
	SET_GCODE_OFFSET Z_ADJUST=0
	{endif}

	M400


#### Timelapse G-Code

	TIMELAPSE_TAKE_FRAME

(Also, remove this command from the stock 'Layer change G-code' section.)

#### Change Filament G-Code

	M600

#### Multimaterial tab

Checked the 'Manual Filament Change' checkbox.

#### Extruder tab

These are mostly a matter of opinion, but I changed:

Z hop when retracting set to 0.2
Z hop type changed to "Auto"

#### Print Speed

Under print speed (in Process Global Settings for each print profile), I entered the Acceleration values I got from the belt tuning sequence. 
It mentions something about 'Don't go over X m/s2 to avoid too much smoothing'. 
I used the smaller value of those for 'Normal printing'. Travel is still 20k.

Note: It seems to be pretty OK to go above those values, significantly, without getting too much ringing.
