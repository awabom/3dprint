## Pressure Advance calibration for PrusaSlicer

 1. Set up a print using your normal profile, and add PressureAdvanceCorners.stl to the plate.
 2. In Printers - Custom G-code - After layer change G-code, add:
```
SET_PRESSURE_ADVANCE ADVANCE={0.02 + (0.04-0.02) * layer_num / (total_layer_count-1)}
```
 3. Change both the 0.02 values to your start value, and the single 0.04 value to the end value.
 4. Slice and print!
 5. Measure where the best results are, and check the Preview tab and look in the G-code what the current SET_PRESSURE_ADVANCE command was for that layer.
 6. In Filaments - Custom G-code - Start G-code, for the tested filament, add the new value:
```
SET_PRESSURE_ADVANCE ADVANCE=0.0123
```
 