"""Mag insert for the keel dock: the PMAG stub cut from David's 'AR Magazine Vice Block PMAG Version' STL,
sitting on a new base that drops into the keel pocket and traps a 1/4-20 nut (v4: 1/4-20 hardware).
v5 (2026-09-10, David: 'mag insert was a bit too short to engage the mag catch'): cut at z = 39 instead of 52. The source block's shoulder is not a tang, it is the magwell SEAT: a shoulder sloped 13 mm
over the mag's length (11 deg, the rake of the magwell mouth) so the lower sits flat on it with the stub fully home. v4 cut
that off and stood the bare stub on a flat base, so the raked magwell mouth touched the base at one end with the stub ~13 mm
short of home and the catch never reached the notch (notch band is z = 82-88 in the source, 30-36 above the v4 base)."""
import numpy as np, trimesh
from manifold3d import Manifold, CrossSection, Mesh, OpType

IN = 25.4
CUT_Z = 39.0            # mm: top of the source block's tang. Keeps the sloped magwell seat (z 39-52) under the stub (v5)
BASE_L, BASE_W, BASE_T = 2.64*IN, 1.34*IN, 0.40*IN   # Rev C: no ears, bolts from below
BOLT_CC = 1.60*IN
NUT_AF_POCKET = 11.4                                  # hex pocket AF for a 1/4-20 nut (7/16 = 11.1 AF); flats face the stub's side walls
NUT_AF, NUT_T = 11.4, 6.0       # 1/4-20 nut 7/16 AF x 7/32 thick, with clearance
BOLT_D = 0.28*IN                # 9/32 clearance for 1/4-20
RELIEF_D, RELIEF_H = 7.0, 10.0  # blind hole above the nut for the bolt tip

def to_manifold(tm):
    return Manifold(Mesh(vert_properties=np.asarray(tm.vertices, np.float32), tri_verts=np.asarray(tm.faces, np.uint32)))

src = trimesh.load('magblock.stl')
# The source STL is two overlapping shells: the vise block (z 0-51.8, with a shoulder that slopes from z=52 at the mag's front
# to z=39 at its rear -- that slope is the magwell seat, matching the rake of the magwell mouth) and a solid PMAG body whose
# bottom sits inside the block at z=39. A straight boolean union of the two re-merges into non-manifold edges along the
# seat/mag intersection, so the seat is rebuilt parametrically instead: the mag cut clean at z=52 (as v4), standing on a
# prism of its own z=52 outline down to z=39, plus the sloped wedge. Same shape, clean topology.
bodies = src.split(only_watertight=False)
block = [b for b in bodies if b.bounds[1][2] < 60][0]; mag = [b for b in bodies if b.bounds[1][2] > 100][0]
mag = mag.simplify_quadric_decimation(face_count=30000)   # the scan-grade mag mesh is full of sliver triangles; 30k faces is plenty for a 0.6 nozzle
mag.merge_vertices(); mag.update_faces(mag.nondegenerate_faces()); mag.remove_unreferenced_vertices()
print('mag decimated', len(mag.faces), 'watertight', mag.is_watertight)
mag_m = to_manifold(mag)
stub  = mag_m.trim_by_plane([0, 0, 1], 52.0)                       # clean mag stub, z 52..116
sec   = mag_m.slice(52.1).offset(-0.15, 0).simplify(0.05)                         # its outline just above the cut, pulled 0.15 mm inside the wall so no faces coincide
prism = Manifold.extrude(sec, 52.0 - CUT_Z + 0.1).translate([0, 0, CUT_Z + 0.1])   # straight-sided plinth z 39.1..52.2 (overlaps the stub and the wedge, coincides with neither)
bb = block.bounds
# sloped seat: full block footprint in X, z = 52 at the front (min y) falling to z = 39 at the rear (max y)
wedge_cs = CrossSection([[(bb[0][1], CUT_Z), (bb[1][1], CUT_Z), (bb[0][1], 52.3)]])          # (y, z) triangle; 52.3 so it overlaps the stub bottom (52.0) instead of touching it on a line
wedge = Manifold.extrude(wedge_cs, bb[1][0] - bb[0][0]).rotate([90, 0, 90]).translate([bb[0][0], 0, 0])
seat_m = wedge + prism + stub
b6 = seat_m.bounding_box(); c = [(b6[0] + b6[3]) / 2, (b6[1] + b6[4]) / 2]
print('stub+seat bounds', [round(v, 1) for v in b6])
stub_m = seat_m.translate([-c[0], -c[1], -CUT_Z + BASE_T - 0.2]).rotate([0, 0, 90])   # centred, sunk 0.2 into the base, long axis along X
stub_m = stub_m ^ Manifold.cube([BASE_L - 0.6, BASE_W - 0.6, 300], center=True).translate([0, 0, 150])   # seat 0.3 inside the base walls
print('stub manifold status', stub_m.status())

base = Manifold.cube([BASE_L, BASE_W, BASE_T], center=True).translate([0, 0, BASE_T/2])
part = base + stub_m
top = part.bounding_box()[5] if hasattr(part, 'bounding_box') else 80.0
for sx in (-1, 1):
    bx = sx * BOLT_CC / 2
    part = part - Manifold.cylinder(BASE_T + 2, BOLT_D/2, BOLT_D/2, 48).translate([bx, 0, -1])
    # hex nut pocket from the base top all the way out the top of the stub: drop the nut in from above
    hexcs = CrossSection.circle(NUT_AF_POCKET/np.sqrt(3), 6)          # vertex on +X -> flats face +/-Y
    part = part - Manifold.extrude(hexcs, 200).translate([bx, 0, BASE_T])
mesh = part.to_mesh64()
tm = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)   # manifold's own topology
print('raw manifold output watertight', tm.is_watertight)
if not tm.is_watertight:
    tm = trimesh.Trimesh(tm.vertices, tm.faces, process=True)
    tm.update_faces(tm.nondegenerate_faces()); tm.update_faces(tm.unique_faces()); tm.remove_unreferenced_vertices()
    trimesh.repair.fill_holes(tm); trimesh.repair.fix_normals(tm)
tm.export('dock_mag_insert_v5.stl')
chk = trimesh.load('dock_mag_insert_v5.stl')
print('insert watertight', chk.is_watertight, 'bounds in', (chk.bounds/IN).round(2).tolist(), 'vol in3', round(chk.volume/16387.064, 2), 'faces', len(chk.faces))
