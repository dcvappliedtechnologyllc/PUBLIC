# Doyle Vee Jaws — design log

Why the parts look the way they do, what was tried and rejected, and what is still open.
Written so the reasoning survives without the conversation.

---

## Origin

Wanted: soft jaws for a Harbor Freight Doyle 4-1/2 in swivel vise (57737) that hold rifle
fore-ends and AR handguards on a few points of contact, print on a Bambu P1S with a 0.6 mm
hardened nozzle, and bolt on in the vise's own jaw-screw holes (thought to be M6 at the time; they are 1/4-20).

The vise was measured from ruler photos, not a drawing: plate seat 4.50 in, screw centres
~2.25 in, screw axis ~0.35 in above the plate bottom, and "4 mm hex button heads = M6" — which was wrong: a
1/4-20 button head takes a 5/32 hex (3.97 mm). The vise is imperial. That uncertainty
is absorbed by ±1/8 in slots rather than chased: "it could slide 1/8 inch and be okay."
`seat_height_in = 0.75` (casting top above the plate seat) is still an assumption to be checked
on the first fitted print.

---

## Vee geometry

150° included (faces 15° off vertical), ±1.00 in span, 0.27 in deep. For round stock of
diameter D the apex gap is 1.035·D, so the vee is shallow enough that fore-ends of 1.2–2.5 in
seat on two short lines well below centre and never touch the apex. Steeper vees were rejected:
they grip harder per pound but put the contact higher on the work and need more opening.

The apex is raised 2.00 in above the casting top so a handguard or a magwell has room around it.
Earlier revisions had the apex at the steel-plate height; the raise came from the observation
that a printed jaw can be any shape, so it may as well get the work clear of the vise body.

Contact points: "flattened pyramids" and interrupted (segmented) contact faces were considered
to save filament and cope with irregular fore-ends, and dropped — foam shims on a plain vee do
the same job with no geometry, and the user's stated preference was fewer clever features.

---

## Revision history

| Rev | Change | Why |
|---|---|---|
| A–B (8 in) | 8 in wide jaw, wings past the casting, apex at plate height | first pass; wings were for long fore-ends |
| C | Raised apex, saddle over the casting, transverse ribs on the back | ribs for stiffness with less plastic |
| C2 | **Ribs replaced by a solid back wedge** | ribs were unprintable on end — "how do those ribs support themselves in midair?" Every feature must be part of the extruded profile so it prints as a vertical wall. |
| D | Debossed branding; chamfered ceilings | OpenSCAD's CGAL could not finish the stepped cutter; moved the deboss to a manifold3d/shapely pipeline |
| F (4.5 in) | **Shortened to 4.50 in = the plate seat**; foam groove behind a lip rail | short ARs don't need wings; 4.5 in saves ~30 % filament and the ends now index on the casting sides. Keel dock and PMAG insert added. |
| G | Lip rail thinned to 0.155 | rail crush concern |
| G2/H | **Lip removed, band left as a flat shelf**; section trimmed 29 % (28.4 → 20.3 in³): back-to-apex 0.75 → 0.60, wedge 1.50 → 0.60, saddle 1.50 → 1.25 | "why not remove this? prevents that spot from ever seeing clamping load" — a flush lip was the one thin feature in the load path. Then "rethink the geometry, reduce the cross section, keep height" |
| I | **Slot back with a set-back lip**; saddle cut flush with the wedge base (tail removed); band 0.275 → 0.325 proud | the foam slot was wanted after all, but with a profile that keeps clamping load off it. Lip face 0.08 behind the band plane, 0.145 thick so it isn't fragile. The 0.65 in of saddle past the wedge did nothing structural. |
| O | Washer pockets Ø0.82 → **Ø1.06 for 1 in fender washers** | Only 1 in fenders on the shelf. Since the pocket is open through the bottom and the washer sits past the ledge, OD is free up to the pocket; 1 in hangs 0.15 below the jaw over air. Bearing ~350 psi. A small washer under the head bridges the fender's 5/16 hole. |
| N | **1/4-20 hardware throughout** (jaw, keel v7, insert v4) | The vise's jaw screws are 1/4-20, not M6 — 5/32 and 4 mm hexes are indistinguishable by eye; the pitch (20 tpi vs 1.0 mm) is the tell. Through-holes 0.26 → 9/32; washer is a 1/4 SAE flat (3/4 OD, fits the Ø0.82 pocket); insert nut pockets 10.2 → 11.4 mm AF for a 7/16 nut, ~0.19 of stub wall each side; keel head bore stays Ø0.52 (a 1/4-20 button head is 0.44), no washer there because the keel bottom is only 1.96 wide. |
| M | **Saddle and wedge 0.60 → 0.35**; vertical slot slop 0.04 → 0.08 | The casting has only ~1/4 in of rough flat behind the mounting face before the slide top rounds off, and the plate ledge is machined — so the ledge is the datum and the saddle only has to reach the flat. 11 % less plastic (19.1 → 17.1 in³), jaw 1.54 deep. Block bending at the casting top ~1,000 → ~1,600 psi, still 4× in PETG. The extra vertical slop means nobody has to get `seat_height_in` right: the jaw sits on the ledge and the saddle lands where it lands. Steeper wedge (82°) made the deboss cutter's chamfer steps touch edge-to-edge; a sub-micron jog per step in `deboss.py` keeps the output manifold. |
| L | **Screw centres 2.25 → 2.40**; pockets Ø0.82 for **20 mm** washers | Photos of the bare seat: holes 1.05 in from each end of the 4.47 in face, so 2.40 c-c — the 2.25 estimate was inside the slot range but with 0.05 to spare. The ledge under the plate is only ~3/8 in deep, so a washer 0.50 out from the face hangs over air and can be as big as the pocket allows. Bearing drops to ~600 psi. |
| K | **Washer pockets Ø0.66 for 16 mm washers, open through the jaw bottom**; vertical slot slop 0.06 → 0.04 | washer bearing was the governing number (~3,000 psi at 200 lbf on a 12 mm washer). A 16 mm washer halves it. It is the largest that fits with the screw axis 0.35 above the bottom; a 3/4 in fender washer would hang below the jaw. Ø0.66 lands tangent to the bottom face, so the pocket is opened through it rather than leaving a knife-edge sliver. Vertical through-bolts to post-tension the jaw were analysed and rejected: on end they lie in the layer plane and clamp nothing; upright they add < 200 psi of precompression that PETG creeps away, and cost section in the apex block. |
| J | Lengthwise edges eased | "she's pretty sharp." Chamfers on bed-side edges (safe overhangs upright), fillets on top/vee/band edges, 0.03 on the lip and slot mouth, slot floor sharp. End-face edges left at the plain 1/16 chamfer — a full round on a non-convex profile wasn't worth the hour. |

Dock:

| Rev | Change | Why |
|---|---|---|
| A | Keel + insert, screws from the top into nuts in the keel | **Wrong** — "does the nut actually clamp anything?" The nut had nothing to bear on. |
| B | Nuts in side-entry slots | **Wrong again** — the M6 still clamped nothing; "it would have to drop in from top" |
| C | **Screws up from under the keel into nuts dropped down hex pockets through the PMAG stub** | user's idea; the nut bears on the insert base, the head on the keel web, so base + web are clamped. Correct clamp stack. |
| D | Keel shortened to 4.50 in; set-tab in the foam groove; rail reliefs | "the base could have a mating tab to interface with the foam groove" |
| E | Set-tab full length; **keel printed on end ("like a pop can")** | tab, pocket and reliefs all become vertical walls — no support |
| v6 | Set-tab 0.10 → 0.07 | Rev I slot is 0.10 |
| v7 / insert v4 | 1/4-20 | see jaw Rev N. Insert stub also sunk 0.2 mm into its base so the union overlaps instead of sharing a face (the shared face came back as non-manifold edges after STL round-trip). |

Handwheel (Rev A): the sliding T-bar is always off-centre and needs flipping; a disc that clips onto the
exposed bar on both sides of the hub makes it a spinner. Snap lips were drawn first and replaced by two cable
ties at the user's request — a snap fit on a Ø15 bar lives on a couple of tenths of fit, a tie does not. The
through bore means the axial position of the bar in the hub (unmeasured) does not matter: the wheel seats on
the bar, the hub pokes out the front. Channel made deeper than the estimate ("a little deeper than your guess").
`hull()` for the rim chamfer silently convexified the scallops; replaced with stepped offsets.

Pattern worth noting: both clamp-stack mistakes were caught by the user asking one question,
not by analysis. Draw the bolt, the nut and what each bears on before modelling.

---

## The band and the lip

The steel plates the jaws replace are flat and proud, and they clamp flat stock parallel.
Rev I's parallel band reproduces that: 0.325 in proud of the vee-edge plane from the jaw bottom
to 1.45 in. It is the only flat bearing face.

The foam slot sits above it, against the vee. The **lip** in front of the slot is set 0.08 in
behind the band's clamp plane. A flat piece against the band cannot reach it; round stock in
the vee rides the faces above it. The lip is a foam holder and a keel locator, nothing else, and
the step is big enough to be obvious by eye.

Cost of the band: round stock smaller than ~1.15 in meets the bands before it seats in the vee
(was 1.05 at 0.275 proud). Accepted; barrels go in the pipe jaws.

---

## Print orientation

Every jaw feature is in the extruded (Y,Z) profile, so the plain jaw prints **on an end face**
with no support and the clamping bend stress in-plane. The branded jaw prints upright because
the user chose to see the artwork clean — the top text is then a flat-floor recess and the
logo sits on a 77° wall where the up-slope cavity walls overhang only 13°.

On end, every stroke of the artwork has a "ceiling" in the vertical wall. Left square, the
perimeter over each cavity hangs in air for the stroke length and sags. The deboss cutter is
stepped so the ceiling side of every stroke slopes 45° over the 1 mm depth. Penalty: one edge of
each letter is bevelled ("drop shadow"), and strokes thinner than the depth become shallow
ramps. That is why the public artwork is the wordmark + URL in a heavy face with ≥ 1.4 mm
strokes, and the small "APPLIED TECHNOLOGY" tagline was dropped from it.

The fixed-jaw branded variant rotates the top text 180° (never mirrors) so it reads from the
operator's side. A mirrored first attempt "was all fucked up reverse".

---

## Slicing findings (P1S, 0.6 mm, PETG+)

- The plate is flow-limited at 15 mm³/s (uncalibrated Inland PETG+). A 0.30 mm layer height on
  the plain jaw saved **nothing** against 0.24 — the slicer slowed it back down. Everything runs
  at 0.24.
- Infill combination (two sparse layers per pass) and 3 walls instead of 4 were the real wins:
  inner walls were 30 % of plate time, sparse infill 36 %.
- Tree support **on build plate only** for the upright branded jaw: 7–8 g, 15 min. "Support
  critical regions only" sits one row below it in Orca's panel and was clicked by mistake twice.
- Pair of Rev J jaws: 5 h 30 m, 282 g (275 model + 7 support).

---

## Material

Prototypes in Inland PETG+. Final jaws + insert in **PA612-CF** (Polymaker Fiberon, 500 g
spool on hand): low moisture uptake keeps the slot and vee stable, and unlike PA6-CF it wants
the P1S chamber *cool* (door open, top off, bed 40–50 °C with glue) so no chamber heater is
needed. Keel in PETG-CF — compression only. Spool budget: jaws ~260 g + insert ~60 g fits;
adding the keel (~130 g) does not leave margin for purge and a failed start.

PA6-CF works but needs conditioning and a warm chamber; PPA-CF wants more nozzle than the P1S
has; ASA and PLA rejected (ASA for no reason to accept the fumes, PLA for creep under sustained
clamp load).

For the nylon run: both jaws on end (CF nylon's layer adhesion is its weak axis), and re-check
the slot and screw-slot fits on the PETG proto first — CF nylon shrinks differently and the lip
will be much stiffer.

---

## Open items — close before publication

1. **Fit on the vise.** Rev J PETG+ pair is the first fitted print (2.25 nominal; the real 2.40
   spacing sits 0.075 out in each slot). Confirm `seat_height_in` (0.75) and how much flat the
   saddle actually lands on — the slide top is rounded behind a short flat. Bands parallel, ends
   index on the casting. Measure the true opening at the apex and between the bands.
2. **PMAG vise-block source.** The insert's stub is cut from a supplied STL, "AR Magazine Vice
   Block PMAG Version Final". Author, URL and licence unknown. If it does not permit
   derivatives, ship the keel with an empty pocket and a pocket drawing.
3. **Foam.** 2 mm craft foam assumed; slot is 0.10 in. Confirm it stands in the slot and leans
   on the face without bowing.
4. **Keel float.** Confirm the keel sits 0.04 low on the tab and lifts onto the vee faces as the
   jaws close, and that the 0.07 tab clears the 0.10 slot in nylon.
5. **PA612-CF.** No profile yet. Flow and temperature tower before committing the spool; check
   whether the URL deboss wants 0.6 mm depth on end.
6. **Photos** for the README: jaws on the vise with a handguard; keel + insert with a lower.
