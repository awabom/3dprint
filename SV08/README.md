## Sovol SV08 - Notes

These are my changes made to the SV08 config, using firmware version 2.3.3 as a starting point.

USE AT YOUR OWN RISK. This is only tested on my personal machine. If your printer breaks, don't blame me.

### macro.cfg

 * Raised nozzle cleaning: I think the nozzle cleaning digs the nozzle a bit to much into the cleaning pad. Some parts were ripped off after just 2 cleaning cycles.
 * Calibration of z-offset each print.
 * Using parameters to 'START_PRINT' from slicer (see start g-code below)
 * New start sequence: Heating bed to target temperature before homing and calibration of z-offset.
 
 See complete [macro.cfg](macro.cfg)

### printer.cfg

#### Input Shaper

Under the "input_shaper" section, I manually entered the results from the 'Belt tuning' sequence. 
It seems the menu option does not save the correct 'shaper_type' setting after belt tuning. 
I also manually entered the correct frequency values here to be safe (the sovol command will save the values in the separate "saved_variables.cfg" file.

#### PID tuning

I could not see that the built-in PID tuning saved any values, so I manually entered the values in the "extruder" section (pid_kp, pid_ki, pid_kd).

#### Exclude Object

I enabled the 'exclude object' module by adding

	[exclude_object]
	
At the end of printer.cfg before the 'save_variables' section

### Orca Slicer profile

I used Sovols official Orca Slicer profile (from the Google Drive folder). Then made the following changes:

#### Start G-Code

 * Warning: To use this start g-code you MUST do all changes to macro.cfg above.

 * Note 1: At the end of the start g-code, there is a section of if-statements. This adjusts the z-offset to my liking based on material.
I guess the values will differ for you.

 * Note 2: This removes the priming blob and priming lines. Instead, I use 5 skirt lines as priming in my print profiles.

Code:

	START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]

	{if filament_type[initial_extruder] == "PETG"}
	SET_GCODE_OFFSET Z_ADJUST=0.15
	{elsif filament_type[initial_extruder] == "ASA"}
	SET_GCODE_OFFSET Z_ADJUST=0.10
	{elsif filament_type[initial_extruder] == "ABS"}
	SET_GCODE_OFFSET Z_ADJUST=0.10
	{elsif filament_type[initial_extruder] == "PLA"}
	SET_GCODE_OFFSET Z_ADJUST=0.05
	{else}
	SET_GCODE_OFFSET Z_ADJUST=0.15
	{endif}

	M400


#### Timelapse G-Code

	TIMELAPSE_TAKE_FRAME

(This line was removed from the 'Layer change G-Code' as in the stock profile.

#### Change Filament G-Code

	M600

#### Multimaterial tab

Checked the 'Manual Filament Change' checkbox.

#### Print Speed

Under print speed (in Process Global Settings for each print profile), I entered the Acceleration values I got from the belt tuning sequence. 
It mentions something about 'Don't go over X m/s2 to avoid too much smoothing'. 
I used the smaller value of those for 'Normal printing'. Travel is still 20k.
