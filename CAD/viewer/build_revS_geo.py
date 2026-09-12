"""Rev S jaw stack for the viewer: 3 printed segments + 4 laser-cut plates + OEM pad + 3 through-bolts + 2 mounting screws.
Frame = the jaw frame used by the viewer: X along the jaw (0..4.5), Y from the casting face (+ toward the work), Z from the jaw bottom.
Geometry is built in inches with manifold3d (profiles extruded along X) and exported in mm.
Outputs: jawS_plastic.stl, jawS_plates.stl, jawS_pad.stl, jawS_bolts.stl
"""
import numpy as np, trimesh, io, contextlib
from manifold3d import Manifold, CrossSection
with contextlib.redirect_stdout(io.StringIO()):
    import jaw_plate as JP                       # plate outline + plastic profile + hole positions (inches)
IN = 25.4
L = 4.5; T_PLATE = 0.25; SEG = (L - 4 * T_PLATE) / 3          # 1.1667
X_PLATES = [0, T_PLATE + SEG, 2 * (T_PLATE + SEG), 3 * (T_PLATE + SEG)]
X_SEGS = [T_PLATE, 2 * T_PLATE + SEG, 3 * T_PLATE + 2 * SEG]
SCREW_X = [1.05, 3.45]; SCREW_Z = 0.35
BOLT_D = 0.3125; BOLT_HOLE_PLATE = JP.HOLE_D; BOLT_HOLE_PLASTIC = 0.375
HOLES = JP.HOLES

def prism(poly_pts, length):
    """polygon in (Y, Z) inches extruded along X from 0 to length -> Manifold in the jaw frame"""
    from shapely.geometry import Polygon
    from shapely.geometry.polygon import orient
    pts = np.array(orient(Polygon(poly_pts), 1.0).exterior.coords[:-1], float)     # CCW for manifold's fill rule
    cs = CrossSection([pts.tolist()])
    m = Manifold.extrude(cs, length)            # extruded along local z = X
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]; f = np.asarray(mesh.tri_verts)
    v = v[:, [2, 0, 1]]                          # (Y, Z, X) -> (X, Y, Z)
    return Manifold(trimesh_to_mesh(v, f))

def trimesh_to_mesh(v, f):
    from manifold3d import Mesh
    return Mesh(vert_properties=np.asarray(v, np.float32), tri_verts=np.asarray(f, np.uint32))

def cyl_x(d, x0, x1, y, z, fn=48):
    c = Manifold.cylinder(x1 - x0, d / 2, d / 2, fn)          # along local z
    return c.rotate([0, 90, 0]).translate([x0, y, z])
def cyl_y(d, y0, y1, x, z, fn=48):
    c = Manifold.cylinder(y1 - y0, d / 2, d / 2, fn)
    return c.rotate([-90, 0, 0]).translate([x, y0, z])
def hexprism_x(af, x0, x1, y, z):
    r = af / 2 / np.cos(np.pi / 6)
    return Manifold.cylinder(x1 - x0, r, r, 6).rotate([0, 90, 0]).translate([x0, y, z])

def export(man, name):
    mesh = man.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3] * IN; f = np.asarray(mesh.tri_verts)
    tm = trimesh.Trimesh(v, f, process=False)
    tm.export(name); print(name, len(tm.faces), 'faces, watertight', tm.is_watertight, 'bounds', tm.bounds.round(1).tolist())

# ---- segments
seg_parts = []
for i, x0 in enumerate(X_SEGS):
    s = prism(JP.plastic, SEG).translate([x0, 0, 0])
    for (hy, hz) in HOLES: s = s - cyl_x(BOLT_HOLE_PLASTIC, x0 - 1, x0 + SEG + 1, hy, hz)
    for sx in SCREW_X:
        if x0 < sx < x0 + SEG: s = s - cyl_y(0.281, -1, 2, sx, SCREW_Z)
    seg_parts.append(s)
plastic = seg_parts[0] + seg_parts[1] + seg_parts[2]
export(plastic, 'jawS_plastic.stl')

# ---- plates
plates = None
for x0 in X_PLATES:
    p = prism(list(JP.outline)[:-1], T_PLATE).translate([x0, 0, 0])
    for (hy, hz) in HOLES: p = p - cyl_x(BOLT_HOLE_PLATE, x0 - 1, x0 + T_PLATE + 1, hy, hz)
    plates = p if plates is None else plates + p
export(plates, 'jawS_plates.stl')

# ---- pad (OEM, assumed 4.47 x 0.75 x 0.30, button-head counterbores)
pad = Manifold.cube([4.47, JP.PAD_T, 0.75]).translate([(L - 4.47) / 2, JP.TAB_Y, 0])
for sx in SCREW_X:
    pad = pad - cyl_y(0.281, JP.TAB_Y - 1, JP.TAB_Y + 1, sx, SCREW_Z) - cyl_y(0.46, JP.TAB_Y + JP.PAD_T - 0.13, JP.TAB_Y + 1, sx, SCREW_Z)
export(pad, 'jawS_pad.stl')

# ---- hardware: 3 x 5/16-18 x 5 SHCS + washer + nut, 2 x 1/4-20 button heads in the pad
hw = None
for (hy, hz) in HOLES:
    b = cyl_x(BOLT_D, 0, 5.0, hy, hz) + cyl_x(0.469, -0.3125, 0, hy, hz, 32) \
        - cyl_x(0.25, -0.35, -0.10, hy, hz, 6)                                    # shank+head, hex socket
    b = b + cyl_x(0.688, L, L + 0.06, hy, hz, 32) + hexprism_x(0.5, L + 0.06, L + 0.06 + 0.266, hy, hz)
    hw = b if hw is None else hw + b
for sx in SCREW_X:
    yf = JP.TAB_Y + JP.PAD_T - 0.13                                              # head seat in the counterbore
    s = cyl_y(0.25, yf - 1.75, yf, sx, SCREW_Z) + cyl_y(0.437, yf, yf + 0.132, sx, SCREW_Z, 32) - cyl_y(0.156, yf + 0.05, yf + 0.2, sx, SCREW_Z, 6)
    hw = hw + s
export(hw, 'jawS_bolts.stl')
