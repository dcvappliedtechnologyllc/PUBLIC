"""Face art for the Doyle vise handwheel (Rev E): full DCV logo in the bottom sector, "<- LEFTY LOOSE . RIGHTY TIGHT ->"
arced across the top, debossed 0.68 mm (first layer + 2 x 0.24) into the FRONT face. The wheel prints face down, so the
art is cut at z = 0 and the model is the mirror of what you see: model (x, y) = viewer (u, -v).
Direction words sit on the TOP arc on purpose: up there the reader's left is counter-clockwise (loose) and right is
clockwise (tight), so the arrows point the way the wheel actually turns. On the bottom arc it would be backwards.
Usage: python3 handwheel_face.py  ->  vise_handwheel_E_PRINT.stl (+ handwheel_face_art.svg, handwheel_face_preview.png)"""
import re, numpy as np, trimesh
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from manifold3d import Manifold, CrossSection, Mesh

DEPTH   = 0.68            # deboss depth (mm): 0.20 first layer + 2 x 0.24
BORE_R  = (38 + 0.4) / 2  # from handwheel.scad Rev D (hub_dia + hub_clear)/2
RIM_R   = 82.5 - 2 * 4 - 3.5  # scallop trough radius minus a margin
LAND    = 2.5             # solid ring left around the bore
TIE_RECT = [box(s * 52 - 3.25, -17.2, s * 52 + 3.25, 17.2) for s in (-1, 1)]   # strap recesses on the front face
FONT = FontProperties(fname='/root/.fonts/Orbitron.ttf', weight='bold')

def rings_to_shape(rings):
    rings = [r for r in rings if r.is_valid and r.area > 1e-6]
    rings.sort(key=lambda p: -p.area)
    polys = []
    for r in rings:
        depth = sum(1 for o in rings if o is not r and o.area > r.area and o.contains(r.representative_point()))
        polys.append((r, depth))
    outer = unary_union([r for r, d in polys if d % 2 == 0])
    holes = [r for r, d in polys if d % 2 == 1]
    return outer.difference(unary_union(holes)) if holes else outer

def svg_polys(path):
    s = open(path).read()
    d = re.search(r'<path d="(.*?)"', s, re.S).group(1)
    rings = []
    for sub in re.findall(r'M([^Mz]*)z', d):
        pts = [(float(a), -float(b)) for a, b in re.findall(r'(-?[\d.]+),(-?[\d.]+)', sub)]
        if len(pts) >= 3: rings.append(Polygon(pts))
    return rings_to_shape(rings)

def text_shape(s, cap):
    tp = TextPath((0, 0), s, size=cap / 0.72, prop=FONT)      # Orbitron cap height = 0.72 em
    rings = [Polygon(p) for p in tp.to_polygons() if len(p) >= 3]
    sh = rings_to_shape(rings)
    b = sh.bounds
    return affinity.translate(sh, -b[0], 0)                   # left edge at x = 0

def warp_to_arc(shape, r_base, x_center=0.0):
    """text-space (x right, y up, baseline y=0) -> circle: angle = 90deg - (x - x_center)/r_base, radius = r_base + y.
    Reader's left = counter-clockwise, glyph tops point outward (upright text on the top arc)."""
    def f(pts):
        pts = np.asarray(pts); th = np.pi / 2 - (pts[:, 0] - x_center) / r_base; rr = r_base + pts[:, 1]
        return np.c_[rr * np.cos(th), rr * np.sin(th)]
    geoms = shape.geoms if isinstance(shape, MultiPolygon) else [shape]
    out = []
    for g in geoms:
        out.append(Polygon(f(g.exterior.coords), [f(h.coords) for h in g.interiors]))
    return unary_union(out)

def arrow(x0, x1, cap, left):
    """shaft + head in text space, spanning x0..x1, centred on the cap height"""
    yc = cap / 2; sh_h = 1.6; head_l = 6.0; head_h = 5.0
    if left:
        head = Polygon([(x0, yc), (x0 + head_l, yc + head_h / 2), (x0 + head_l, yc - head_h / 2)])
        shaft = box(x0 + head_l - 0.5, yc - sh_h / 2, x1, yc + sh_h / 2)
    else:
        head = Polygon([(x1, yc), (x1 - head_l, yc + head_h / 2), (x1 - head_l, yc - head_h / 2)])
        shaft = box(x0, yc - sh_h / 2, x1 - head_l + 0.5, yc + sh_h / 2)
    return unary_union([head, shaft])

# ---------------- top arc: arrows + direction words ----------------
CAP = 4.8; R_TEXT = 62.0
left_t = text_shape('LEFTY LOOSE', CAP); right_t = text_shape('RIGHTY TIGHT', CAP)
lw = left_t.bounds[2]; rw = right_t.bounds[2]
ARROW_L = 14.0; GAP = 4.0; DOT_GAP = 9.0
total = ARROW_L + GAP + lw + DOT_GAP + rw + GAP + ARROW_L
x = -total / 2
parts = [arrow(x, x + ARROW_L, CAP, left=True)]; x += ARROW_L + GAP
parts.append(affinity.translate(left_t, x, 0)); x += lw
parts.append(box(x + DOT_GAP / 2 - 0.9, CAP / 2 - 0.9, x + DOT_GAP / 2 + 0.9, CAP / 2 + 0.9))   # separator dot
x += DOT_GAP
parts.append(affinity.translate(right_t, x, 0)); x += rw + GAP
parts.append(arrow(x, x + ARROW_L, CAP, left=False))
top_art = warp_to_arc(unary_union(parts), R_TEXT)
print(f'top arc: {total:.1f} mm of text at r={R_TEXT} -> {np.degrees(total / R_TEXT):.0f} deg span')

# ---------------- bottom sector: full DCV logo ----------------
logo = svg_polys('dcv_logo_poly.svg')                  # full DCV logo, polygonised by OpenSCAD (resize 3.80 in wide, import dcv_logo.svg)
# thicken the thin rule under the wordmark (0.5 mm at this scale would vanish under a 0.6 mm nozzle)
geoms = list(logo.geoms)
rule_i = max(range(len(geoms)), key=lambda i: (geoms[i].bounds[2] - geoms[i].bounds[0]) / (geoms[i].bounds[3] - geoms[i].bounds[1]))
rule = geoms[rule_i]; rb = rule.bounds
geoms[rule_i] = box(rb[0], (rb[1] + rb[3]) / 2 - 0.55, rb[2], (rb[1] + rb[3]) / 2 + 0.55)   # 1.1 mm before scaling
logo = unary_union(geoms)
lb = logo.bounds
logo = affinity.translate(logo, -(lb[0] + lb[2]) / 2, -lb[3])          # top edge at y = 0, centred

def place_logo(s, du):
    return affinity.translate(affinity.scale(logo, s, s, origin=(0, 0)), du, -(BORE_R + LAND))
def fits(sh):
    xy = np.array([c for g in (sh.geoms if isinstance(sh, MultiPolygon) else [sh]) for c in g.exterior.coords])
    return np.all(np.hypot(xy[:, 0], xy[:, 1]) <= RIM_R)
best = None
for s in np.arange(0.60, 1.00, 0.005):
    for du in np.arange(-7, 7.1, 0.5):
        if fits(place_logo(s, du)) and (best is None or s > best[0]): best = (s, du)
s, du = best; bottom_art = place_logo(s, du)
bb = bottom_art.bounds
print(f'logo scale {s:.3f} (width {bb[2]-bb[0]:.1f} mm, height {bb[3]-bb[1]:.1f} mm), shifted {du:+.1f} mm')

# ---------------- checks, mirror, cut ----------------
art_view = unary_union([top_art, bottom_art])          # viewer coords (u, v)
for r in TIE_RECT: assert not art_view.intersects(r), 'art hits a tie strap recess'
assert art_view.distance(Polygon([(BORE_R * np.cos(t), BORE_R * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 180)])) >= LAND - 0.05
art_model = affinity.scale(art_view, 1, -1, origin=(0, 0))   # mirror: face down, seen from -z

def to_cs(shape):
    geoms = shape.geoms if isinstance(shape, MultiPolygon) else [shape]
    contours = []
    for g in geoms:
        ext = np.array(g.exterior.coords[:-1]); contours.append(ext if Polygon(ext).exterior.is_ccw else ext[::-1])
        for h in g.interiors:
            arr = np.array(h.coords[:-1]); contours.append(arr[::-1] if Polygon(arr).exterior.is_ccw else arr)
    return CrossSection(contours)

m = trimesh.load('vise_handwheel_D_plain_PRINT.stl')   # plain Rev D solid rendered from vise_handwheel.scad
wheel = Manifold(Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32)))
cutter = Manifold.extrude(to_cs(art_model), DEPTH + 1.0).translate([0, 0, -1.0])
out = wheel - cutter
mesh = out.to_mesh64()
tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=False)
print('watertight:', tm.is_watertight, 'volume', round(tm.volume / 1000, 1), 'cm3 (Rev D', round(m.volume / 1000, 1), ')')
tm.export('vise_handwheel_E_PRINT.stl')

# records: SVG of the art (viewer orientation) and a preview
with open('handwheel_face_art.svg', 'w') as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-85 -85 170 170" width="170mm" height="170mm">\n')
    f.write('<circle r="82.5" fill="#e8dcc8"/><circle r="%.2f" fill="white"/>\n' % BORE_R)
    for g in (art_view.geoms if isinstance(art_view, MultiPolygon) else [art_view]):
        d = 'M' + ' L'.join(f'{x:.3f},{-y:.3f}' for x, y in g.exterior.coords) + ' Z'
        for h in g.interiors: d += ' M' + ' L'.join(f'{x:.3f},{-y:.3f}' for x, y in h.coords) + ' Z'
        f.write(f'<path d="{d}" fill="#222" fill-rule="evenodd"/>\n')
    f.write('</svg>\n')

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Polygon as MplPoly, Rectangle
from matplotlib.path import Path
fig, ax = plt.subplots(figsize=(7, 7)); ax.set_aspect('equal'); ax.axis('off')
t = np.radians(np.arange(0, 360)); rr = 82.5 - 4 + 4 * np.cos(12 * t)
ax.add_patch(MplPoly(np.c_[rr * np.cos(t), rr * np.sin(t)], fc='#e8dcc8', ec='#6b4f2a'))
ax.add_patch(plt.Circle((0, 0), BORE_R, fc='white', ec='#6b4f2a'))
for r in TIE_RECT: b = r.bounds; ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fc='#999', alpha=0.5, ec='none'))
for g in (art_view.geoms if isinstance(art_view, MultiPolygon) else [art_view]):
    verts = list(g.exterior.coords); codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
    if not Polygon(verts).exterior.is_ccw: verts = verts[::-1]
    for h in g.interiors:
        hv = list(h.coords); hv = hv[::-1] if Polygon(hv).exterior.is_ccw else hv; verts += hv; codes += [Path.MOVETO] + [Path.LINETO] * (len(hv) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), fc='#3a2a10', ec='none'))
ax.set_xlim(-90, 90); ax.set_ylim(-90, 90)
ax.set_title('Handwheel Rev E face, as seen on the vise (deboss 0.68 mm, printed face down)')
fig.savefig('handwheel_face_preview.png', dpi=130, bbox_inches='tight')
