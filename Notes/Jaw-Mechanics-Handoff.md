# Doyle Vee Jaws — mechanics handoff

What we learned about how a soft jaw actually carries load, written for someone who might design the next one — or the
vise under it — from a clean sheet. Companion to `Fixture-Handoff.md` (the keel and pocket interface) and the Design Log
(the blow-by-blow). Inches throughout. The numbers come from printed parts on a Harbor Freight Doyle 4-1/2 in vise
(57737) and from a 2D plane-strain finite-element model of the jaw section (`CAD/jaw_fea.py`); where a number is from
the model it says so.

## 1. What the jaw is, structurally

A soft jaw on this vise is a **cantilever off a 0.75 in tall mounting face**. That one sentence drives everything.

The casting offers three surfaces: a machined vertical face 0.75 in tall with two blind 1/4-20 holes at 0.35 in up and
2.40 in apart; a machined ledge about 3/8 in deep under it (the plate seat the OEM steel pad sits on); and a rough cast
top with roughly 1/4 in of usable flat behind the face before it rounds away. Above the top there is nothing to lean on.

Our jaw puts the vee apex 2.00 in above the casting top and the jaw top 3.00 in above it, because a rifle upper, a
handguard or a magazine well needs that clearance over the vise body. So the clamp load enters 2–3 in above the last
point of support. Everything below is about what that does.

## 2. The load path under clamp

The clamp load pushes each jaw *toward its own casting*. With the vee faces symmetric the resultant is normal to the
mounting face; with a big round object high on the upper face there is an upward component as well. The moment of
that load about the casting's top edge tips the jaw back over the casting.

Three things resist the tip:

1. **The mounting face in compression.** The jaw's back face bears on the casting from Z = 0 to 0.75. As the moment
   grows the bearing concentrates at the top edge.
2. **The saddle in compression.** The jaw hooks over the casting top (0.35 in reach, 0.40 in thick). Tipping back
   presses the saddle's rear onto the casting top. The arm is short — the flat is only ~1/4 in — but it is there.
3. **The screws in tension.** The screw axis is 0.35 in up; the pivot is at 0.75; the arm is 0.40 in. Against a load
   2.0 in above the pivot that is a **5:1 lever**: screw tension rises five times faster than clamp force *if* the
   joint opens.

The model's answer, which surprised us: with the joint preloaded even modestly (500 lbf per screw) **it never opens
under clamp load.** The clamp pushes the jaw into the casting harder than the moment pulls the bottom away; screw
tension actually *falls* as the vise is tightened (2000 → ~1200 lbf at 1000 lbf of clamp). The 5:1 lever only bites on
pull-away loads — prying a part out, a hammer blow outward — where the joint sees real tension. That is where preload
matters, and where a screw head bearing on printed honeycomb fails first (see §5).

So under clamp the screws are not the spring. What is?

## 3. Where the flex comes from (a stiffness ladder)

Apex deflection toward the casting at 1000 lbf clamp per jaw, from the 2D model, PA612-CF15 as printed (5 walls solid,
40 % 3D-honeycomb core taken as ¼ of solid modulus), ordered from softest to stiffest:

| Configuration | Apex, mil | Note |
|---|---|---|
| R2 jaw, fenders in pockets (idealised as a bonded face) | ~13 | real fenders on honeycomb are worse — local crush |
| Pad outboard, thin printed tab (0.475) | 15.2 | the band overhangs the pad with nothing under it |
| Pad outboard, tab to the band face (0.90–1.00) | 11.4 | the knee; more tab buys nothing |
| + vertical steel tie bolts through the jaw | 10.1–11.0 | prestress does nothing; steel ties buy 5–10 % |
| + 2 × 1/2 in flat-bar ribs in the section plane | 7.1 | |
| + 100 % infill instead of 40 % | 6.4 | the single biggest plastic-only lever |
| + 2 × L-ribs from 1 in bar (1 in below the vee, 1/2 in above) | 4.6 | depth cubed — the foot matters more than a third rib |
| + 4 × L-ribs | 3.3 | |
| **+ 4 × full-profile 1/4 in laser-cut plates (Rev S)** | **1.2** | infill stops mattering (1.19 vs 1.22 at 100 %) |
| Raise 2.0 → 1.5 in (plastic jaw, no steel) | 7.0 | the geometry lever, if the clearance allows it |

Three lessons in that table:

- **Prestress is not stiffness.** Bolts squeezing the plastic do not change its modulus. A steel member only helps if
  it is in the load path *as steel* — a tie on the tension side, or a rib carrying bending.
- **Depth cubed.** Any steel that stays behind the apex line (so the plastic keeps the vee) is worth far more when it
  is wide low down, where the moment is, than when it is tall.
- **Below ~2 mil the vise is the spring.** A 4-1/2 in slide in its ways plus the leadscrew moves several mil on its
  own. Past that point you are polishing the wrong part; four plates is where we stopped.

## 4. The mounting interface — lessons

- **The head must bear on something that does not creep.** A 1 in fender on 40 % honeycomb is ~0.7 in² of cells; at
  2000 lbf that is ~3000 psi and it crushes and creeps, which is exactly what "the flex is at the screws" felt like.
  Putting the OEM steel pad *outboard* — pad → printed tab → casting — spreads each screw over ~1 in² of solid plastic,
  or, with the Rev S plates, onto steel edges directly. Nose-bleed torque becomes safe.
- **Do not thin the root.** A rabbet at the casting face to save screw length is a hinge at the exact section with the
  most moment. The tab should be the full section; the pad stands proud of it.
- **A thin plastic layer in the stack is stiffer than a thick one** (compression stiffness ∝ 1/t), but that term is
  small; what matters is that the pad backs the whole band, not the tab thickness.
- **The blind holes set the screw length**, and the screw length sets how thick the stack can be. Measure hole depth
  early. A 3/4 in screw bottomed through a 0.35 in wall; two M6 flats fixed it that day; the design fix was the wall.
- **Slots versus holes.** Horizontal slots (±1/8) let the jaw find the casting's hole spacing; vertical slop (0.08)
  lets the machined ledge set the height while the saddle lands wherever the rough top puts it. Once the spacing is
  confirmed, holes locate better than slots and the pad takes the shear.
- **Preload is a take-up-the-slop lever**, not a stiffness lever. It flattens the printed face onto the rough casting
  and it is what holds the joint shut under pull-away. Plain Grade 8 nuts on a preloaded joint; no nylocks.

## 5. Material and print orientation

- **Print on end.** Every feature of the jaw lives in the extruded profile, so standing the part on its end face
  turns pockets, slots, roofs and holes into vertical walls. It also puts the layer lines *along the length*, so
  bending in the section plane never loads a layer interface — CF nylon's weak axis is the interlayer, and it is out
  of the load path.
- **"A roof is only a roof in one orientation."** A 45° ceiling that grows off solid in the upright print grows out of
  open air on end. Face-angle checks are not enough — slice it (`CAD/printcheck.py`) and look for material that has
  nothing under it a layer down.
- **Walls vs infill.** With five 0.6 mm walls the skin carries the vee; the core mostly carries compression. Going 40 →
  100 % infill halves the deflection of an all-plastic jaw and does nothing once there is steel inside. Choose infill
  by which jaw you are building.
- Materials as used: PETG for shape protos; PA612-CF15 for jaws and inserts (295/290 °C, high-temp plate 60 °C + glue,
  fan 0–15 %, 9 mm³/s, 5 walls, 40 % 3D honeycomb; door open, dryer feed); PET-CF17 for the keel (290 °C, textured PEI
  80 °C + glue, fan 0–10 %, 15 mm³/s, 4 walls, 30 %; door open).

## 6. The vee

- **15° off vertical (150° included) is a light vee.** It self-locates a round or a keel but it will not self-centre
  against friction: the centering component is tan 15° = 0.27, and plastic-on-plastic friction is 0.3–0.5. Anything
  that sits in the vee must be located *before* the handle moves. That is why the keel grew a tee flange that rests on
  the jaw tops and a 0.015 in lift so its upper faces engage first and push it down onto the flange.
- **Apex height sets the lever.** Every inch of raise is a linear increase in moment and a cubic increase in cantilever
  deflection. Put the apex as low as the clearance behind the jaw allows and no lower than the work needs.
- **The lip never bears.** The band below the vee carries a foam slot and a lip that holds a foam sheet against the
  face; nothing structural hangs on it, and the keel's history (v1–v8 cocked on a tab in that slot) is the reason.

## 7. If you were designing the vise itself

The soft jaw fights the vise it sits on. A vise built for tall soft jaws would:

- **Make the mounting face tall** — 2–3 in, not 0.75 — so the jaw is a plate bolted to a wall, not a cantilever off a
  curb. Every problem in §2–4 shrinks with the face height.
- **Put the screws high and spread them**, or use four. With the pivot at the top edge of the face, screws near the
  top have the long arm; ours sit 0.40 in below the pivot. Even two screws at mid-height on a 2.5 in face would cut the
  lever from 5:1 to about 1:1.
- **Give the jaw a keyed seat**: a machined step or a pair of dowels that take shear and locate the jaw, so the screws
  only preload. Then slots and slop go away.
- **Provide a steel backer as part of the vise** — the equivalent of our outboard pad, but designed in: a full-height
  steel plate the soft jaw bolts to, with the vise's own screws bearing on steel. That is the Rev S plate stack done
  once in the casting instead of four times in every jaw.
- **Keep the jaw tops as a datum.** The tee-flange trick only works because both jaw tops are co-planar; make that a
  machined feature and every fixture can hang from it.
- **Know the slide's own stiffness.** Ours is the floor at a couple of mil per 1000 lbf; a heavier slide or a shorter
  overhang raises the floor and makes the jaw improvements visible.

## 8. Where the numbers came from

`CAD/jaw_fea.py`: 2D plane-strain Q4 raster mesh of the section at 0.025 in, compression-only penalty contact on the
casting face, ledge and casting top, screw preload and axial stiffness at Z = 0.35, PA612-CF15 as 750 ksi solid with a
core at ¼ of that, steel at 30 Msi, 1000 lbf per jaw split on both vee faces (keel case) or high on the upper face
(big-round case). It is a section model: it cannot see local crush under a washer, and it smears ribs over the length.
Treat the ratios as solid and the absolute mils as ±30 %.

Files: `CAD/doyle_vee_jaw.scad` (jaw, Rev R2), `CAD/jaw_plate.py` (Rev S steel plate DXF), `CAD/build_revS_chunk.py`
(one-piece Rev S test jaw), `CAD/printcheck.py`, `Notes/Design-Log.md`, and the 3D viewer in `CAD/viewer/`.
