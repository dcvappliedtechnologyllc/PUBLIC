# Doyle Vee Jaws — fixture handoff

How to design something that docks in these jaws. Everything below is inches; the source of truth is
`CAD/dock_keel.scad` (keel) and `CAD/doyle_vee_jaw.scad` (jaw). Parts are modelled in mm, parameters in inches.

## The jaw vee (what you dock into)

Two printed jaws on a Harbor Freight Doyle 4-1/2 in vise (57737), 4.50 in long, each with a **light vee**:
a 150° included vee (faces tilted 15° off vertical), apex 2.00 in above the casting top, faces reaching 1.00 in
above and below the apex. The jaw top is flat, 3.00 in above the casting. Below the vee is a band with a foam slot;
the band never carries a fixture.

Frame used in every file: **X along the jaws, Y across the vise (toward the workpiece = away from that jaw's casting),
Z up.** For a fixture the useful datum is the *apex line* of the two vees; with the keel seated the apex lines are
**2.50 in apart** and the jaw tops are 0.985 in above them (see lift, below).

## The keel: the standard foot

The keel (`dock_keel_4.5in_v9_ONEND_PRINT.stl`, v9) is the negative of the two vees — a hexagon in section — with a
tee flange on top. Anything that needs to sit in the vise should either *be* a keel (same section, your own top) or
*bolt to* the keel's pocket. The numbers, in the section plane (Y across, Z up, Z = 0 at the jaw-bottom datum the
keel's own files use):

| Feature | Value | Why |
|---|---|---|
| Length along X | 4.50 | = the vise plate seat; clamps over the casting, no wing loading |
| Width at the apex line | 2.500 | the jaws close to 2.50 at apex when seated |
| Vee faces | 15° off vertical, ±1.00 from the apex line | must match the jaws |
| Width at the flange underside (0.985 above apex) | 1.972 | = 2.50 − 2 × 0.985 × tan 15° |
| **Tee flange** | 0.50 reach each side × 0.20 thick, underside 0.985 above the apex | rests on both jaw tops; sets roll and pitch before the handle is touched |
| Overall width over the flanges | 2.972 | |
| **Lift** | keel apex sits 0.015 above the jaw apex when the flange is down | upper faces engage first and push the keel *down* onto the flange; lower faces get 0.008 total clearance |
| Bottom trim | keel bottom 0.30 above the lower vee edge line | lower faces are a 0.70 backup; bottom clears the foam lips |
| Section height | 1.885 (bottom trim to flange top) | |

Rules that came from broken prints: no fin or tab into the foam slot (v1–v8 hung on one and clamped cocked); a 15°
vee cannot self-centre against plastic-on-plastic friction, so a fixture must be located *before* the handle moves —
that is what the flange and the lift do. Push down → flange; pull up → the upper wedge tightens.

## The pocket: how tops attach

The keel top has a pocket for a swappable insert, and two screws come **up from below**:

- Pocket: 2.64 × 1.34, 0.15 deep, 0.01 clearance each side, centred on the keel.
- Two 1/4-20 × 1-1/4 button heads on **1.60 c-c** along X, 9/32 clearance holes through the keel, Ø0.52 counterbores
  from the keel bottom (a 5/32 T-handle reaches them between the jaws). 0.50 in of keel web is left under the heads.
- The insert has a 0.40 in thick base that fills the pocket and two hex pockets (7/16 AF, from the top) that trap 1/4-20
  nuts: the nut bears down on the base, the head bears up on the keel web, so base + web are actually clamped.
- All hardware in this project is 1/4-20. Do not introduce M6.

So a new top = a 2.64 × 1.34 × 0.40 base (the pocket is cut 0.01 larger all round) with two nut pockets on 1.60 c-c, plus whatever you want on top of it.
Reference insert: `dock_mag_insert_PMAG_v5_PRINT.stl` (`CAD/mag_insert.py`).

## Variants on the same section

- **Reaction-rod clamshell** (Rev A, draft): the keel section split on a vertical plane with a D-channel for a rod along
  X, so the vise closes the shell on the rod; 0.030 parting gap so the clamp goes through the rod, rubber-band grooves
  for preload, a tongue-and-groove key planned for Rev B. `CAD/rod_clamshell.scad`. If your fixture clamps something
  rather than holding it, start there.
- Anything long along X can overhang the jaws; the section is what matters.

## Printing

Print keels and clamshells **on end** ("pop can", `print_on_end = true`): flange, pocket, bores and channel all become
vertical walls, no support. A roof is only a roof in one orientation and a 45° face is only printable if it grows off
solid — run `CAD/printcheck.py <stl>` before sending anything; it slices at 0.24 and reports unsupported area.
Materials so far: PETG for protos, PET-CF17 for the keel (290 °C, textured PEI 80 °C + glue, fan 0–10 %, door open),
PA612-CF15 for jaws and inserts.

## Files

`CAD/dock_keel.scad` (parameters: `keel_apex_width_in`, `flange_reach_in`, `keel_lift_in`, `bottom_trim_in`, pocket
and bolt sizes), `CAD/mag_insert.py`, `CAD/rod_clamshell.scad`, `CAD/printcheck.py`, and the 3D viewer artifact
(`CAD/viewer/doyle_assembly_viewer.html`) to see how it all sits.
