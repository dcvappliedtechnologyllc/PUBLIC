"""Chamfered deboss of the DCV logo + FUCK YEAH into the Rev N jaw, done with manifold3d
(OpenSCAD 2021's CGAL chokes on the stepped cutter).  Geometry mirrors doyle_vee_jaw.scad.
Print orientation is +X up, so the +X wall of every stroke (the cavity ceiling) gets a 45deg chamfer."""
import re, sys, numpy as np, trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
from manifold3d import Manifold, CrossSection, Mesh

IN = 25.4
# ---- jaw params (keep in sync with the .scad) ----
L = 4.50*IN; SEAT = 0.75*IN; ZA = SEAT + 2.00*IN; VH = 1.00*IN; H = ZA + VH
TA = 0.60*IN; TE = TA + VH*np.tan(np.radians(15)); FT = 0.40*IN; BT = 0.35*IN
DB = 0.04*IN; STEPS = 4; FLIP = "--flip" in sys.argv; UPRIGHT = "--upright" in sys.argv

def svg_polys(path):
    s = open(path).read()
    d = re.search(r'<path d="(.*?)"', s, re.S).group(1)
    rings = []
    for sub in re.findall(r'M([^Mz]*)z', d):
        pts = [(float(a), -float(b)) for a, b in re.findall(r'(-?[\d.]+),(-?[\d.]+)', sub)]  # SVG y is flipped
        if len(pts) >= 3: rings.append(Polygon(pts))
    # outer/hole assignment by even-odd nesting
    rings.sort(key=lambda p: -p.area)
    polys = []
    for r in rings:
        depth = sum(1 for o in rings if o is not r and o.area > r.area and o.contains(r.representative_point()))
        polys.append((r, depth))
    shape = unary_union([r for r, dpt in polys if dpt % 2 == 0])
    shape = shape.difference(unary_union([r for r, dpt in polys if dpt % 2 == 1])) if any(dpt % 2 for _, dpt in polys) else shape
    return shape

def to_cs(shape):
    if shape.is_empty: return None
    geoms = shape.geoms if isinstance(shape, MultiPolygon) else [shape]
    contours = []
    for g in geoms:
        ext = np.array(g.exterior.coords[:-1]); contours.append(ext if Polygon(ext).exterior.is_ccw else ext[::-1])
        for h in g.interiors:
            arr = np.array(h.coords[:-1]); contours.append(arr[::-1] if Polygon(arr).exterior.is_ccw else arr)
    return CrossSection(contours)

def chamfered_cutter(shape, dx=-1.0, dy=0.0):
    """z=0 is the surface; cut extends to z=-DB. The wall on the (dx,dy) side of every stroke is stepped back 45deg
    (that wall is the cavity ceiling in the chosen print orientation). dx=dy=0 -> plain cut."""
    st = DB/STEPS; parts = []
    for i in range(STEPS):
        t = (i+1)*st
        sl = shape.intersection(affinity.translate(shape, xoff=-dx*t, yoff=-dy*t)) if (dx or dy) else shape
        cs = to_cs(sl)
        if cs is None: continue
        parts.append(Manifold.extrude(cs, st + 0.002).translate([0.0007 * i, 0.0007 * i, -t]))   # sub-micron jog: slabs overlap instead of touching edge-to-edge (no non-manifold edges)
    parts.append(Manifold.extrude(to_cs(shape), 2.0))
    return Manifold.batch_boolean(parts, __import__('manifold3d').OpType.Add)

def load_manifold(stl):
    m = trimesh.load(stl)
    return Manifold(Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32)))

def save(man, path):
    """manifold3d's output is watertight by construction; keep it as-is. trimesh's vertex merge and
    degenerate-face pruning can open thin triangles at the chamfers, so only fall back to them if needed."""
    mesh = man.to_mesh64()
    raw = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=False)
    if raw.is_watertight:
        raw.export(path); return trimesh.load(path, process=False)
    tm = trimesh.Trimesh(raw.vertices, raw.faces, process=True)
    tm.update_faces(tm.nondegenerate_faces()); tm.update_faces(tm.unique_faces()); tm.remove_unreferenced_vertices()
    trimesh.repair.fill_holes(tm); trimesh.repair.fix_normals(tm)
    tm.export(path)
    return trimesh.load(path, process=False)

jaw = load_manifold('jaw_4.5in_N_plain_UPRIGHT_PRINT.stl')
PUBLIC = '--public' in sys.argv
text = None if PUBLIC else svg_polys('art_text.svg'); logo = svg_polys('art_logo_public.svg' if PUBLIC else 'art_logo.svg')
if FLIP and text is not None:   # fixed jaw: operator stands on its vee side, so the top text is rotated 180deg (never mirrored);
           # the wedge logo faces the back of the vise and stays as-is
    text = affinity.rotate(text, 180, origin=(0, 0))

# text on the top face: local xy -> model xy, surface at z=H
# on end: +X is up -> chamfer +X walls.  upright: top text is a top-surface recess -> no chamfer;
#          logo on the 60deg slope -> its up-slope (+y local) walls are the ceilings -> chamfer those.
text_cut = None if text is None else (chamfered_cutter(text, 0, 0) if UPRIGHT else chamfered_cutter(text, 1, 0)).translate([L/2, TE/2, H])
# logo on the wedge slope: rotate local frame about X by slope angle, then place at slope center
ang = np.degrees(np.arctan2(H - (SEAT+FT), BT))
logo_cut = (chamfered_cutter(logo, 0, 1) if UPRIGHT else chamfered_cutter(logo, 1, 0)).rotate([ang, 0, 0]).translate([L/2, -BT/2, (SEAT+FT+H)/2])

out = ((jaw - logo_cut) if text_cut is None else (jaw - text_cut - logo_cut)).simplify(0.001)
tag = ('DCV_public' if PUBLIC else 'DCV_FY') + ('_fixedjaw' if FLIP else '') + ('_UPRIGHT' if UPRIGHT else '')
up = save(out, f'jaw_4.5in_N_{tag}_upright.stl')
pr = up if UPRIGHT else save(out.rotate([0, -90, 0]), f'jaw_4.5in_N_{tag}_print_on_end.stl')
chk = lambda p: trimesh.load(p).is_watertight   # merged, like a slicer
print(tag, 'watertight', chk(f'jaw_4.5in_N_{tag}_upright.stl'), (UPRIGHT or chk(f'jaw_4.5in_N_{tag}_print_on_end.stl')), 'vol in3', round(up.volume/16387.064, 2), 'faces', len(up.faces),
      'print bounds in', (pr.bounds/IN).round(2).tolist())
