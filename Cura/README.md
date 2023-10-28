## Sovol SV04 in Cura

My quite early test versions of things for using my Sovol SV04 in Cura.
(Using modded johncarlson21 firmware with increased temp-limit, and bi-metal heatbrakes).

The script StartGCodeMover.py moves temperature setting g-code added automatically by Cura from before the start g-code to after. This lets Cura add the proper temperatures when using two extruders, since the default placeholders seem to add the incorrect temperature sometimes when only extruder 2 is active.
