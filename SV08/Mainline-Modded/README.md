# Sovol SV08 - Notes

Work in progress. This is new documentation, a bit different from the 'Stock' one I have here on github as well.

USE AT YOUR OWN RISK. This is only tested on my personal machine. If your printer breaks, don't blame me.

These are my changes made to the SV08 I currently run:

 * Mainline klipper using the guide at: https://github.com/Rappetor/Sovol-SV08-Mainline
 * Biqu Microprobe, using the mount from: https://www.printables.com/model/952307-sovol-sv08-biqu-microprobe-mount-v20
 * New shroud, not yet released. But the stock shroud is fine - I just like to see the nozzle.
 * DIY Enclosure from acrylic panels and tape - This is important. Get an enclosure (The factory one seems nice too).
 * My config files:
   * Modded the startup scripts for the Microprobe
   * ...and chamber heating (using the bed and nozzle as temp sensor)
   * Enabled skew_correction.
 * Slicer profiles based on Voron 350 with 0.4 nozzle
   * PrusaSlicer: Voron_v2_350_afterburner 0.4 nozzle 
   * OrcaSlicer: Voron 2.4 350 0.4 nozzle
   
You NEED to use a mechanical probe and mainline klipper for this to work.

## Config files for klipper

These files can be edited via Mainsail and just edited directly into the printer by editing existing, and creating new files:

 * Files here: [klipper_config/](klipper_config/)
 
NOTE: You need to enter the correct serial numbers for your MCU and TOOLHEAD MCU!!

### Input Shaper

Under the "input_shaper" section, I manually entered the results from the 'Belt tuning' sequence.

### PID tuning

After 

	PID_CALIBRATE HEATER=extruder TARGET=250
	SAVE_CONFIG
	
...the updated values will be at the bottom of printer.cfg 

I also did

	PID_CALIBRATE HEATER=heater_bed TARGET=80
	SAVE_CONFIG

### Skew Correction

After (and maybe before?) belt tuning, it prints askew. See [skew correction](https://www.klipper3d.org/Skew_Correction.html).
Enable with an empty "skew_correction" section in printer.cfg:

	[skew_correction]

To create a skew correction profile run the following using the console (with my example values):

	SET_SKEW XY=141.5,141.0,99.9
	SKEW_PROFILE SAVE=my_skew_profile
	SAVE_CONFIG
	

## Slicer setup

### PrusaSlicer profile 

 * Create a Voron 2.4 350 printer, and modify the following:

 * General
   * Max print height: 345
   * Extruders: 2
   * Single Extruder Multi Material: true
   * Supports remaining times: true
 * Machine limits, see below.
 * Extruder 1
   * Layer height limits
     * Max: 0.32
     * Min: 0.08
   * Travel lift
     * Use ramping lift: true
     * Maximum ramping lift: 0.4
     * Steeper ramp before obstacles: true
     * Only lift Above Z: 0
   * Retraction
     * Retraction length: 0.5
     * Retraction speed: 30
     * Minimum travel after retraction: 2
     * Retract on layer change: true
     * Wipe while retracting: true
     * Retract amount before wipe: 70%
   * Retraction when tool is disabled...
     * Length: 0
   * After entering all these values, click 'Apply below setting to other extruders'
 * Single extruder MM setup
   * Cooling tube length: 0
   * Cooling tube position: 0
   * Extra loading distance: 0
   * Filament parking position: 0
   * Purging volume: 50 (this is just a guess, currently)

Not important/tune them yourself:

 * Machine limits
   * Max feedrates
     * E: 50
     * X: 700
     * Y: 700
     * Z: 20
   * Maximum accelerations
     * Max accel E: 5000
     * ...extruding Normal: 20000
     * ...retracting Normal: 5000
     * X Normal: 40000
     * Y Normal: 40000
   * Jerk:
     * E: 5
     * X: 20
     * Y: 20
     * Z: 0.5

 * Custom G-code:
   * Emit temperature commands automatically: false

#### Start G-code

	START_PRINT EXTRUDER_TEMP=[first_layer_temperature[initial_tool]] BED_TEMP=[first_layer_bed_temperature] CHAMBER_TEMP=[chamber_minimal_temperature]
	
	G1 E10 F100
	G1 Z5 E-1 F1200
	G1 Z5 F600
	
	G1 X{first_layer_print_min[0]} Y{max(0, first_layer_print_min[1]-5)} F6000
	G1 Z0.2 F600
	G1 X{first_layer_print_min[0]+30} E5 F600

	M400

#### End G-code

	END_PRINT
	
#### Before layer change G-code

	;BEFORE_LAYER_CHANGE
	;[layer_z]
	G92 E0

#### After layer change G-code

	;AFTER_LAYER_CHANGE
	;[layer_z]
	TIMELAPSE_TAKE_FRAME

#### Tool change G-code

	; Fake tool change to T{next_extruder}
	{ if previous_extruder >= 0 }
	M117 Change to {next_extruder}
	M600
	{ else }
	; Not doing filament change for first extrusion
	{ endif }
	
#### Between objects G-code (for sequential printing)

Leave empty

#### Color Change G-code

	M600
	
#### Pause Print G-code

	PAUSE
	

