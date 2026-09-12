"""Rev S test-print set in PA612-CF: the segmented jaw with the plates printed in plastic as stand-ins for the laser-cut steel.
Same geometry as the Rev S concept (jaw_plate.py numbers): tab to the OEM pad, three 5/16 through-bolt holes on one column,
1/4-20 mounting holes, plate outline with the 0.06/0.04 recesses.
  jaw_S_segment_PA612_PRINT.stl  — one symmetric 1.167 in segment, print THREE per jaw. Stands on an end face; the through-bolt
                                   holes are vertical; the two 9/32 mounting holes (0.367 and 0.80 from either end, so the part
                                   is the same either way round) are horizontal and get teardrop roofs.
  jaw_S_plate_PA612_PRINT.stl    — the plate outline, 0.25 in, print FOUR per jaw flat on the bed. Steel later.
Frame while building: X along the jaw, Y from the casting face (+ toward the work), Z from the jaw bottom, inches.
"""
import numpy as np, trimesh, io, contextlib, math
from manifold3d import Manifold, CrossSection, Mesh
with contextlib.redirect_stdout(io.StringIO()):
    import jaw_plate as JP
IN = 25.4
L = 4.5; T_PLATE = 0.25; SEG = (L - 4 * T_PLATE) / 3      # 1.1667
SCREW_Z = 0.35; SCREW_HOLE = 0.281
SCREW_IN_SEG = [1.05 - T_PLATE, SEG - (1.05 - T_PLATE)]   # 0.80 and 0.367 from the segment's start: symmetric set
BOLT_HOLE_PLASTIC = 0.375
HOLES = JP.HOLES

def to_manifold(v, f): return Manifold(Mesh(vert_properties=np.asarray(v, np.float32), tri_verts=np.asarray(f, np.uint32)))
def ccw(pts):
    from shapely.geometry import Polygon
    from shapely.geometry.polygon import orient
    return np.array(orient(Polygon(pts), 1.0).exterior.coords[:-1], float).tolist()
def prism_x(poly_yz, length):                       # profile in (Y,Z) extruded along X
    m = Manifold.extrude(CrossSection([ccw(poly_yz)]), length).to_mesh()
    v = np.asarray(m.vert_properties)[:, :3][:, [2, 0, 1]]; f = np.asarray(m.tri_verts)
    return to_manifold(v, f)
def prism_y(poly_xz, y0, y1):                       # profile in (X,Z) extruded along Y  (odd permutation -> flip winding)
    m = Manifold.extrude(CrossSection([ccw(poly_xz)]), y1 - y0).to_mesh()
    v = np.asarray(m.vert_properties)[:, :3][:, [0, 2, 1]]; f = np.asarray(m.tri_verts)[:, [0, 2, 1]]
    return to_manifold(v, f).translate([0, y0, 0])
def cyl_x(d, x0, x1, y, z, fn=48): return Manifold.cylinder(x1 - x0, d/2, d/2, fn).rotate([0, 90, 0]).translate([x0, y, z])
def teardrop_y(d, x, z, y0, y1, fn=48):
    """horizontal hole along Y, printed with +X up: circle + 45deg roof pointing +X"""
    r = d / 2
    hole = Manifold.cylinder(y1 - y0, r, r, fn).rotate([-90, 0, 0]).translate([x, y0, z])
    roof = prism_y([(x + r / math.sqrt(2), z + r / math.sqrt(2)), (x + r * math.sqrt(2), z), (x + r / math.sqrt(2), z - r / math.sqrt(2))], y0, y1)
    return hole + roof
def export(man, name, rot=None):
    mesh = man.to_mesh(); v = np.asarray(mesh.vert_properties)[:, :3] * IN; f = np.asarray(mesh.tri_verts)
    tm = trimesh.Trimesh(v, f, process=False)
    if rot is not None: tm.apply_transform(rot)
    tm.apply_translation(-tm.bounds[0])          # sit on the bed at the origin
    tm.export(name)
    print(f"{name}: {len(tm.faces)} faces, watertight {tm.is_watertight}, {tm.volume/IN**3:.2f} in^3, bbox {(tm.extents/IN).round(2).tolist()} in")
    return tm

if __name__ == "__main__":
    # ---- segment
    seg = prism_x(JP.plastic, SEG)
    for (hy, hz) in HOLES: seg = seg - cyl_x(BOLT_HOLE_PLASTIC, -1, SEG + 1, hy, hz)
    for sx in SCREW_IN_SEG: seg = seg - teardrop_y(SCREW_HOLE, sx, SCREW_Z, -1, 2)
    # on end: +X (segment length) becomes +Z
    R = trimesh.transformations.rotation_matrix(-math.pi / 2, [0, 1, 0])
    seg_tm = export(seg, 'jaw_S_segment_PA612_PRINT.stl', R)

    # ---- plate stand-in (flat, same outline + holes as the steel DXF)
    plate = prism_x(list(JP.outline)[:-1], T_PLATE)
    for (hy, hz) in HOLES: plate = plate - cyl_x(JP.HOLE_D, -1, T_PLATE + 1, hy, hz)
    Rp = trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0])   # X (thickness) -> Z: flat on the bed
    plate_tm = export(plate, 'jaw_S_plate_PA612_PRINT.stl', Rp)

    # ---- reference: the whole jaw assembled (for the viewer / a sanity picture)
    X_PLATES = [0, T_PLATE + SEG, 2 * (T_PLATE + SEG), 3 * (T_PLATE + SEG)]
    X_SEGS = [T_PLATE, 2 * T_PLATE + SEG, 3 * T_PLATE + 2 * SEG]
    asm = None
    for x0 in X_SEGS:
        p = seg.translate([x0, 0, 0]); asm = p if asm is None else asm + p
    for x0 in X_PLATES: asm = asm + plate.translate([x0, 0, 0])
    export(asm, 'jaw_S_assembled_reference.stl')
    print('per jaw: 3 segments =', round(3 * seg_tm.volume / IN**3, 2), 'in^3, 4 plates =', round(4 * plate_tm.volume / IN**3, 2), 'in^3')
