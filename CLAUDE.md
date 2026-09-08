# Doyle Vee Jaws — project context

Printed light-vee soft jaws + keel dock for the Harbor Freight Doyle 4-1/2 in swivel vise
(57737). **DCV Applied Technology, LLC.** Intended for free download on DCV-AT.COM.

## What this is

- **Jaw** — one extruded profile: 150° vee raised 2 in above the casting, parallel clamping band
  below it, foam slot with a set-back non-bearing lip, saddle over the casting top, solid back
  wedge carrying the artwork. Bolts on with 1/4-20 × 1-1/4 button heads and 3/4 in SAE washers through ±1/8 in slots (the vise is 1/4-20, not M6).
  Plain and DCV-branded (wordmark + DCV-AT.COM) variants. Current rev **N**.
- **Keel dock** — double-vee block, the negative of the jaw vee, drops between the jaws and
  carries a swappable insert. Current **v7**.
- **PMAG insert** — magwell stub on a nut-trap base for the keel pocket. **v4**.
- **Handwheel** — clips over the vise's Ø15 sliding T-bar, rides on the Ø38 hub, two cable ties. **Rev A**, unprinted.

## Ground rules for this project

- **Imperial units throughout** in every parameter and every document; models are built in mm.
- Working clamp load **200 lbf** at the apex. The vise can make 7,700 lb; the jaws are not for that.
- **Everything on the jaw is in the extruded profile.** No feature may exist that is not a
  corner of `profile_2d()`. That is what lets it print on end with no support and keeps the
  bending load in-plane. Ribs, bosses, anything transverse: no.
- **The lip never bears.** Its face stays behind the band's clamp plane. Do not "improve" it
  into a rail.
- Bottom-of-feature edges get chamfers (upright print overhangs), top edges get fillets.
  Slot floor stays sharp.
- Draw the clamp stack (bolt, nut, what each bears on) before modelling any fastened joint.
  Two dock revisions were wrong because this was skipped.
- All hardware is **1/4-20**. Do not reintroduce M6 anywhere.
- Never mirror the artwork for the fixed jaw; rotate the text 180°.
- New rev = new file names. Never overwrite a delivered STL in place.

## Files

```
CAD/        doyle_vee_jaw.scad, deboss.py, art_logo_public.scad + .svg, dcv_wordmark.svg,
            dock_keel.scad, mag_insert.py, vise_handwheel.scad, print-ready STLs, the Orca 3MF, previews/
README.md   the published doc (repo root, so GitHub renders it)
LICENSE     CERN-OHL-S v2
Notes/      Design-Log.md — why it looks like this, what was rejected, open items
```

Working files, all prior revisions and the private "FUCK YEAH" variant live in
`~/Documents/3D Printing/Doyle Vee Jaws/` (CURRENT/ and _old/). This folder is the publishable
subset.

## Toolchain

OpenSCAD 2021.01 for the solids (`print_orientation`, `print_on_end` flags), Python
manifold3d + trimesh + shapely for the debosses and the insert (OpenSCAD's CGAL cannot finish
the stepped cutter). The deboss output needs the trimesh cleanup loop (nondegenerate faces,
merge, fill_holes, fix_normals) to come out watertight. OpenSCAD's SVG export flips Y.
Fonts: Orbitron Bold (URL), Bangers (private variant), from Google Fonts.

## Before touching the geometry

Read `Notes/Design-Log.md`. Several obvious-looking changes were tried and reverted — the lip
in particular has been removed and reinstated once already, on purpose both times.

## Open items

In the Design Log. Do not publish until the fit check and the PMAG-block licence are closed.
