# DCV Doyle Vee Jaws — Printed Light-Vee Jaws + Keel Dock for the 4-1/2 in Bench Vise

**DCV Applied Technology, LLC** · [DCV-AT.COM](https://dcv-at.com)

Soft vee jaws for the Harbor Freight **Doyle 4-1/2 in swivel vise (item 57737)**, printed in
one piece each, that bolt on in the vise's own 1/4-20 jaw-screw holes. A 150° vee raised 2 in above the
casting holds rifle fore-ends and AR handguards on a few points of contact, a parallel band below
it clamps flat stock like the steel plates did, and a slot behind the band takes a strip of craft
foam. The dock is a double-vee block with a tee flange that hangs from the jaw tops and drops between them
and carries a swappable top — currently a PMAG stub, so an AR lower can be clamped by its magwell
without a separate vise block.

Parametric OpenSCAD plus a Python pipeline for the debossed branding. Everything regenerates from
source; change one number for a different vise.

<!-- photo: both jaws on the vise, handguard clamped -->
<!-- photo: keel dock + PMAG insert with a lower on it -->

---

## ⚠️ Read this first

- This vise makes **7,700 lb of clamping force**. These jaws are designed for a **200 lbf working
  clamp** — enough to hold a fore-end still for work, not enough to crush it. Snug the handle by
  hand. If you lean on it, the jaws will crack at the counterbores before anything else does.
- Provided **as-is, with no warranty of fitness for any purpose**. See LICENSE.
- Printed parts vary enormously with filament, moisture, printer and slicer. Nothing here
  guarantees the strength of a part you print.
- These are **soft jaws**. Never hammer on work held in them, never use them with the vise's
  anvil or pipe jaws in play, and never clamp anything that could go off.
- Inspect before use. Discard at the first crack at a counterbore, the flange root, or the lip.

---

## Why these exist

The steel plates that come on the vise are 4-1/2 in wide, flat, and 1-1/2 in tall. A rifle
fore-end held in them contacts on two lines, right where the finish is, and anything round rolls.
The usual fixes are magnetic rubber pads (which slide) or a dedicated gun vise (which costs more
than the vise did and takes up a bench).

A **light vee** — 150° included, only 0.27 in deep — touches a round or oval fore-end on two
short lines well below its centreline and holds it without crushing. Raising the apex 2 in above
the casting gets the work clear of the vise body so a handguard or a mag well has room around it.
Below the vee, a **parallel band** stands proud like the original plates so flat stock still
clamps parallel with no jaw change. Between the band and the vee is a **foam slot**: a strip of
2 mm craft foam stands in it and leans against the lower vee face, so finished stock never touches
plastic. The lip in front of that slot is deliberately set back from the band's clamp plane so it
never carries load and can't be crushed — it only holds foam.

The **keel dock** is the second half of the idea. A double-vee keel, the negative of the jaw vee,
drops between the jaws, self-centres as they close, and presents a pocket on top. The PMAG insert
that goes in the pocket is the magwell stub from a standard AR vise block on a base with two
captured nuts. Two 1/4-20 screws up through the keel hold it. Swap the insert, swap the fixture.

---

## What's in the box

| File | What it is | Print orientation | Support |
|---|---|---|---|
| `jaw_4.5in_R2_plain_ONEND_PRINT.stl` | Plain jaw. Print two, or one of these + one branded. | Standing on an end face (as delivered) | None |
| `jaw_4.5in_R2_plain_UPRIGHT_PRINT.stl` | Same jaw upright, if you want both jaws the same way | Upright | Under the saddle only |
| `jaw_4.5in_R2_DCV_public_UPRIGHT_PRINT.stl` | Movable jaw with the DCV wordmark and DCV-AT.COM debossed in the back wedge (cleanest artwork) | Upright | Under the saddle only |
| `jaw_4.5in_R2_DCV_public_ONEND_PRINT.stl` | Same, with 45° ceilings cut into the artwork so it prints on end with no support (strongest) | On end | None |
| `dock_keel_4.5in_v9_ONEND_PRINT.stl` | Keel dock (v9 tee-top; v7/v8 hung on a set-tab and clamped cocked — don't print them) | On an end face ("pop can") | None |
| `dock_mag_insert_PMAG_v5_PRINT.stl` | PMAG magwell insert for the keel (cloned PMAG geometry with its sloped magwell seat, on a nut-trap base). v4 was 1/2 in short and the catch never engaged | Base down | None |
| `rod_clamshell_geissele_A_ONEND_PRINT.stl` | **Draft.** Reaction-rod clamshell: two keel-profile halves that close on a Geissele Reaction Rod (Ø0.995 / 0.745 flats), flats facing the jaws, 0.030 in parting gap, two V-grooves for rubber-band preload, two loose 1/8 in register pins. 3.50 in long; sits at the front end of the jaws so the rod still reaches the barrel extension. Rev B waits on a rod-protrusion measurement | On end, both halves + pins | None |
| `jaw_S_chunk_4.5in_PA612_ONEND_PRINT.stl` | **Rev S test print.** One-piece 4.50 in jaw with the Rev S profile: full tab to the OEM pad (pad goes outboard, proud of the band), 9/32 mounting holes, three 3/8 holes on the through-bolt column. Fit-checks the pad-as-washer idea before the steel plates are ordered. Tab assumes a 0.30 in pad | On end | None |
| `jaw_plate_S_DRAFT.dxf` | **Concept.** Laser-cut 1/4 in steel plate for the Rev S segmented jaw (four per jaw between three printed segments). Outline generated by `CAD/jaw_plate.py`; draft until the OEM pad is measured | — | — |
| `jaw_hole_pattern_R2_test_plate_PRINT.stl` | 0.2 in coupon of the Rev R2 slot pattern (2.40 centres, 9/32 holes) — print first to check your screw spacing | Flat | None |
| `vise_handwheel_E_PRINT.stl` | 6-1/2 in handwheel that clips over the vise's sliding T-bar, full DCV logo and a LEFTY LOOSE / RIGHTY TIGHT arrow arc debossed in the face (bonus part, see below) | Face down | None |
| `vise_handwheel_D_plain_PRINT.stl` | Same wheel, plain face | Face down | None |
| `Doyle Jaws 4.5in J - claude PETG+ proto.3mf` | OrcaSlicer project: PETG proto plate, plain jaw on end + branded jaw upright, P1S 0.6 mm | — | — |
| `Doyle Jaws 4.5in Q + PMAG insert - claude PA612-CF15.3mf` | OrcaSlicer project: the nylon jaw plate — both jaws on end, PA612-CF15 presets baked in (as printed 2026-09-09: 5 walls, 40 % 3D honeycomb) | — | — |
| `PMAG insert - claude PA612-CF15.3mf` | OrcaSlicer project: the insert alone, same presets | — | — |
| `Doyle keel v9 + PMAG insert v5 - claude PET-CF17.3mf` | OrcaSlicer project, sliced: keel v9 on end + insert v5, Polymaker PET-CF17 presets baked in (0.24, 4 walls, 30 % 3D honeycomb, 15 mm³/s, 8 mm brim). 4 h 55 m, 259 g | — | — |
| `Polymaker PET-CF17 @BBL P1S 0.6mm Claude.json` | The PET-CF17 filament preset on its own, importable in Orca | — | — |

The jaws are handed only by the artwork. A plain jaw fits either side. The branded jaw reads
correctly on the **movable** jaw (wedge toward the operator); put it on the fixed side and it
reads from the back of the bench, which is fine if that's where you stand.

<!-- previews/jaw_revJ_public_views.png -->

---

## Hardware

All 1/4-20. The vise's own jaw screws are 1/4-20 button heads (5/32 hex) — they are just too short.

| Qty | Part | Where |
|---|---|---|
| 4 | 1/4-20 × **3/4 in** button-head socket cap screw (5/32 hex) | jaws. The casting's holes are blind and only ~0.2 in deep: 3/4 in through the 0.475 in wall + fender is right; a 0.35 in wall (Rev Q) let 3/4 in bottom out; 1 in and 1-1/4 bottom out. |
| 4 | **1/4 in fender washer, 1 in OD** (5/16 hole), ~1/16 thick | under the button heads — the big washer is what carries the prying load. Its bottom edge hangs 0.15 in below the jaw, over air past the casting's ~3/8 in ledge. A 3/4 in OD SAE flat washer also fits the pocket. |
| 4 | 1/4 in SAE flat washer (the ones that came on the vise are fine) | between the button head and the fender washer — a 1/4-20 button head is only 0.44 in across and a fender washer's hole is 5/16, so this bridges it |
| 2 | 1/4-20 × 1-1/4 in button-head socket cap screw | keel → insert, from below, no washer (the head bears in a Ø0.52 bore) |
| 2 | 1/4-20 hex nut (7/16 AF) | dropped down the insert's hex pockets |
| — | 2 mm craft foam, cut 4-1/2 × ~1-1/4 in | foam slot |
| 2 | 3/16 in (4.8 mm) cable tie, 8 in | handwheel |

---

## Key dimensions

Jaw 4.50 L × 3.75 H × 1.54 D (in). Jaw length equals the casting's plate seat, so the ends line
up with the casting sides.

| Feature | Value |
|---|---|
| Vee | 150° included (faces 15° off vertical), 0.27 deep, apex fillet 1/16 |
| Vee span | ±1.00 about the apex |
| Apex height | 2.75 above jaw bottom = 2.00 above the vise top |
| Mounting face to apex | 0.60 |
| Back wedge | 0.35 deep at the saddle, tapering to nothing at the top (82° face) — carries the artwork |
| Saddle | 0.35 over the casting top × 0.40 thick (the casting only has ~1/4 in of flat behind the face before it rounds off); 0.06 relief at the inside corner for the casting's edge radius |
| Parallel band | 0.325 proud of the vee-edge plane, jaw bottom to 1.45 up |
| Foam slot | 0.10 wide × 0.30 deep, against the vee |
| Lip | 0.145 thick, top flush with the lower vee edge, face 0.08 **behind** the band clamp plane |
| Screw pattern | 2 × slots on **2.40** centres (measured: 1.05 from each end of the seat), 0.35 above the jaw bottom; Ø9/32 through, ±1/8 horizontal, **±0.04 vertical** so the machined ledge sets the height and the saddle just lands on the casting |
| Washer pocket | Ø1.06 for a 1 in fender washer, open through the jaw bottom, **0.475** of plastic behind the washer (in compression; sized so a 3/4 in screw fills the casting's blind hole). On end, the pocket ceiling is a single 45° plane ("shed roof") from the vee-side tangent point up through the open jaw bottom, so every layer grows off the solid vee side; upright, it is a teardrop toward the vee. `pocket_roof = "auto"` picks. Rev Q pointed a teardrop at the vee in both orientations and the on-end pockets drooped; the far pocket's plane runs out the jaw end 0.21 in up, which is cosmetic |
| Edges | Lengthwise edges eased: 1/16 chamfers on bed-side edges, 1/16 fillets on top/vee/band edges; slot floor sharp; end edges 1/16 chamfer |

| Keel | Value |
|---|---|
| Length | 4.50 |
| Width | 2.50 across the apex line, 1.96 at the flange, 2.97 over the flanges; 1.89 tall (bottom trimmed 0.30 below the apex line, flange 0.20 above) |
| Pocket | 2.64 × 1.34 × 0.15 |
| Screws | 2 × Ø9/32 on 1.60 centres, Ø0.52 head bores 1.24 deep from the bottom, 0.50 web under the head |
| Tee flange | 0.50 reach × 0.20 thick both sides, full length; rests on the jaw tops |
| Lift | Keel apex 0.015 above the jaw apex when the flange is down → upper vee faces engage first; lower faces get 0.008 total clearance |
| Lower faces | 0.70 long (bottom trimmed 0.30); keel bottom sits 0.30 above the jaw lips. No tab, no reliefs |

| Insert | Value |
|---|---|
| Base | 2.64 × 1.34 × 0.40 |
| Seat | The source block's 11° sloped shoulder, 0.52 tall at the mag's front tapering to nothing at the rear — the rake of the magwell mouth, so the lower sits flat with the stub fully home. Catch notch 2.1–2.3 above the pocket floor |
| Height | 3.43 over the pocket floor |
| Nut pockets | 2 × 7/16 AF hex (+0.01 clearance), from the base top out the top of the stub — nuts drop in from above |

### Handwheel

Not part of the jaw system, but it lives on the same vise. A 6-1/2 in scalloped disc, 0.47 in thick, with a
Ø1.51 in bore that slides over the vise screw's Ø38 mm hub from the front and a rib across the back carrying
an open channel that drops over the Ø15 mm sliding T-bar on both sides of the hub. The hub locates it, the
bar drives it, and two cable ties (through the plate, across the channel mouth, back through — one each
side of the hub) hold it on. The bar is captured centred, so the ball ends stick out past the rim as spinner
knobs and the scallops are the palm grip. The hub pokes out through the front by however far the bar sits
back in it; nothing has to be measured. Six crush ribs in the bore stand 0.016 in proud each side — tap the
wheel on with a mallet and it stays put. The rib walls stop 0.02 in below the bar top so the ties cinch onto
the bar rather than hovering over it. Prints face down, no support, ~4 oz.

Rev E carries the face art: the full DCV logo in the lower half and "◄ LEFTY LOOSE ▪ RIGHTY TIGHT ►" arced
over the top, debossed 0.027 in (first layer plus two 0.24 mm layers, so the floors land on a layer line).
The words are on the *top* arc on purpose — up there the reader's left is counter-clockwise and right is
clockwise, so the arrows point the way the wheel turns. The art is cut mirrored by `handwheel_face.py`
(manifold3d) from the plain Rev D STL, so it reads correctly off the build plate. Rev C was printed and
fitted; D fixed the bore fit and rib height, E added the face.

**Opening.** The vise opens 4-1/2 in between its steel plates. With the printed jaws the apex
line opens roughly 1.2 in less than the bare seat-to-seat distance and the band faces 2.4 in
less. Round stock seats in the vee before the bands meet down to about 1.15 in diameter; below
that use the band flats.

---

## Design basis

Working load **200 lbf** at the apex line, taken as a cantilever from the casting top.

| Member | At 200 lbf | Comment |
|---|---|---|
| Bending in the block at the casting top | ~1,600 psi | 4.5 × 1.19 section, wedge trimmed to 0.35 |
| Saddle bearing on the casting top | ~450 psi | on the casting's ~1/4 in flat |
| Screw tension (prying, both screws) | ~250 lbf each | a grade-5 1/4-20 proofs at ~2,700 lbf |
| Washer bearing on the plastic | ~350 psi | 1 in fender washer on 0.475 of plastic (3/4 in: ~600). With only the small washers the vise ships with it is ~3,000 — use the big ones. |

Loads at the top of the vee instead of the apex are 1.5× these. Against PETG that's a margin of
about 15 on the washer bearing with the 1 in washers and only ~2 with small ones — which is why the working load is 200 and not 500, and why the big washers are not optional. CF nylon roughly
doubles it.

**Load path is designed in-plane.** Every feature is part of one extruded profile, so the plain
jaw prints **standing on an end face** with the layer lines running the length of the jaw, and
the bending stress from clamping never crosses a layer boundary. The branded jaw prints upright
for the sake of the artwork; the clamp load then pulls across layers, and the on-end branded
variant exists for anyone who wants the strong orientation with the mark.

**The lip carries nothing.** Its face sits 0.08 behind the band's clamp plane, and round stock
rides the vee faces above it. A flat piece against the band never reaches it. Earlier revisions
put the lip flush with the band and it was the one thin feature in the load path; setting it back
was cheaper than making it strong.

**The keel hangs from the jaw tops and is clamped by the upper vee faces only.** The tee flange
sets its height on both jaws, flat on flat, so roll and pitch are fixed before the handle moves.
The apex is set 0.015 above the jaw apex: raising a hexagon closes its upper faces and opens its
lower faces by lift × tan 15°, so the upper faces always touch first and their reaction pushes
the keel down onto the flange. Push down → flange → jaw top → saddle → casting; pull up → the
upper wedge tightens. The lower faces are a 0.008 backup. v1–v8 hung on a one-sided set-tab
in the foam slot instead: the keel tipped about 4° on the tab with the vise open and sat 0.04 low,
and a 15° vee (centring component tan 15° = 0.27) cannot out-pull PETG-on-PETG friction
(0.3–0.5) to fix that, so it clamped cocked. A light vee holds a seated keel; it will not seat one.

---

## Printing

Developed on a Bambu P1S, 0.6 mm hardened nozzle, OrcaSlicer. Presets and the sliced plate are in
the 3MF.

| Setting | Jaws, PETG proto | Jaws + insert, PA612-CF (as printed) | Keel |
|---|---|---|---|
| Layer | 0.24 mm (0.30 first) | 0.24 mm (0.30 first) | 0.24 mm |
| Walls | 3 | **5** (0.62 mm lines) | 4 |
| Infill | 20 % cross hatch, infill combination on | **40 % 3D honeycomb**, infill combination on | 30 % 3D honeycomb |
| Top / bottom | 4 / 4 | 4 / 4 | 4 / 4 |
| Support | Tree, on build plate only, branded upright jaw only | none (both jaws on end) | none |
| Brim | 6 mm outer | 8 mm outer | 8 mm |
| Seam | Back (mounting face) | Back | — |
| Speeds | — | outer wall 100, inner 150, infill 150, bridge 30 mm/s; max 9 mm³/s | as nylon, max 15 mm³/s |
| Other | — | precise outer wall on, elephant-foot 0.15, classic walls | |

PETG plate time for a pair of jaws is about 5.5 h and 282 g. The plate is flow-limited: a
0.30 mm layer height on the plain jaw saved nothing measurable, so everything runs at 0.24.

| Material | Where | Notes |
|---|---|---|
| **PETG / PETG+** | prototypes, fit checks | 250 °C, textured PEI 75 °C, fan 30–60 %. Slot, lip and screw slots are dimensioned for it. |
| **PA612-CF15** (Polymaker Fiberon) | final jaws + insert | As printed: 295 °C (290 first layer), high-temp plate 60 °C with glue, fan 0–15 % (off for 3 layers, 30 % on overhangs), no chamber control, **door open, top off**, dry 8–12 h at 80 °C and feed from a dryer. 9 mm³/s. Low moisture uptake keeps the slot and vee stable in a shop. Both jaws on end at 5 walls / 40 % 3D honeycomb plus the insert on its own plate fit one 500 g spool. |
| **PET-CF17** (Polymaker Fiberon) | keel | Compression only; no reason for nylon. 290 °C, textured PEI 80 °C first layer / 75 after with glue stick, fan 0–10 %, 15 mm³/s (PA612 ran 9), **door open** per Polymaker (enclosure not needed), dry 70 °C 8 h. Anneal 120 °C 10 h if you want the extra stiffness; not required. |
| PLA | no | Creeps under sustained clamp load at shop temperatures. |

---

## Fitting

1. Print the **hole-pattern coupon** first. Hold it against the casting with the vise's own
   screws; it should go on without forcing. The slots give ±1/8 in, which covers the scatter in
   these castings.
2. Remove the steel plates. The original screws are the right thread (1/4-20) but too short; keep them for the coupon.
3. Set a jaw on the casting: bottom down on the plate-seat ledge, saddle over the casting top, mounting
   face flat on the seat face. The ledge sets the height; the vertical slop in the slots lets the saddle
   land wherever the rough casting top is. Run in the 1/4-20 × 3/4s with the fender washers (small washer under the head, fender under that), snug, not torqued.
4. Close the vise gently until the bands meet and check the bands are parallel and the vee edges
   line up. If they don't, back off a screw and let the slot find it.
5. Cut a strip of 2 mm craft foam 4-1/2 in long, stand it in the slot, lean it back on the lower
   vee face. Trim it flush with the top.

### Keel dock

1. Drop a 1/4-20 nut down each hex pocket in the insert; it lands on the base.
2. Set the insert in the keel's pocket, run the two 1/4-20 × 1-1/4s up from under the keel.
   The head bears up on the keel web, the nut bears down on the base: base and web are clamped.
3. Pull the foam if it stands above the vee edge. Hang the keel on the fixed jaw by its flange
   (it leans on the upper vee face and stays put), close the movable jaw until the flange is down
   on both jaws and the upper faces have it. Push it down as you snug up; it should not move.

### Reaction-rod clamshell (draft, unprinted)

Same double-vee outline as the keel, split down a vertical plane with a D-channel for the rod. The rod's
vise flats face the jaws, so the clamp goes straight through the flats and the torque is taken by the flat
edges, not by friction on the round. Loop two #64 rubber bands (doubled) or 1/16 in O-rings in the grooves
so the shell stays on the rod between jobs; the pins keep the halves from shearing before the vise is on.
The shell is 3.50 in, shorter than the keel, and goes at the **front** end of the jaws: the receiver cannot
sit over these jaws (the rod is 1 in below the jaw tops), so the shell length is what's left of the rod
behind the receiver once the lugs are in the barrel extension. Measure that before printing.

---

## Designing your own fixture

`Notes/Fixture-Handoff.md` is the one-page version: the vee, the keel section numbers, the pocket and bolt
interface, and the print rules. Start there if you want something that docks in these jaws.

---

## Regenerating

```
CAD/
  doyle_vee_jaw.scad     jaw, every dimension in inches at the top of the file; print_orientation
                         = true rotates it on end. Renders the plain jaw.
  deboss.py              cuts the artwork: jaw STL + SVG -> branded STL, with the 45° ceiling chamfers
                         for on-end printing. --upright for the upright variant, --public for the
                         DCV-AT.COM art, --flip for the fixed-jaw text rotation.
                         needs manifold3d, trimesh, shapely.
  art_logo_public.scad   the wedge artwork (DCV wordmark + URL) -> art_logo_public.svg via OpenSCAD.
  dock_keel.scad         keel; print_on_end = true.
- `CAD/rod_clamshell.scad` → `rod_clamshell_geissele_A_ONEND_PRINT.stl` (`print_on_end = true`; both halves and two pins on one plate).
  mag_insert.py          cuts the magwell stub from a vise-block STL and adds the nut-trap base.
```

Put your own logo in: any SVG of filled paths works in `art_logo_public.scad` in place of the
wordmark. Keep strokes ≥ 1.2 mm for a 0.6 mm nozzle, ≥ 2 mm if you print on end.

Other 4-1/2 in vises: measure the plate seat (jaw length), the casting top above the seat
(`seat_height_in`), and the screw spacing (`screw_cc_in`, `screw_height_in`). Everything else
follows.

---

## Attribution

The jaw, the keel and the deboss pipeline are original to DCV Applied Technology.

The **PMAG insert**'s stub is cloned PMAG geometry — the external form of a Magpul PMAG magazine body,
reproduced so the stub fits an AR-15 magwell the way the magazine does. It was taken from an AR
magazine vise-block STL rather than modelled from scratch; `mag_insert.py` cuts the stub from that
file and adds the base, nut pockets and keel interface, which are new. PMAG is a Magpul trademark;
no affiliation.

Artwork: DCV wordmark and logo © DCV Applied Technology; URL and handwheel lettering set in Orbitron (SIL OFL).

---

## License

Copyright © 2026 DCV Applied Technology, LLC.

Licensed under the **CERN Open Hardware Licence Version 2 — Strongly Reciprocal
(CERN-OHL-S v2)**. You may use, study, modify, manufacture and distribute this design, including
commercially, provided modified versions are released under the same licence with sources
available. See `LICENSE`.

Source location for the purposes of the licence: **https://dcv-at.com**

## Trademark notice

"DCV", "DCV Applied Technology" and "Offensive Physics" are trademarks of DCV Applied
Technology, LLC. The licence covers the design, **not** the marks. If you distribute a modified
version, remove or replace the DCV wordmark and DCV-AT.COM deboss — they are source identifiers,
and leaving them on a part DCV did not produce misrepresents its origin. The artwork is a
separate SVG and a one-line swap in `art_logo_public.scad`; the plain jaw carries no mark at all.
The same goes for the handwheel: use `vise_handwheel_D_plain_PRINT.stl`, or swap `dcv_logo_poly.svg`
in `handwheel_face.py` for your own art.
