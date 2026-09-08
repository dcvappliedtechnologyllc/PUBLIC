"""Mag insert for the keel dock: the PMAG stub cut from David's 'AR Magazine Vice Block PMAG Version' STL,
sitting on a new base that drops into the keel pocket and traps a 1/4-20 nut (v4: 1/4-20 hardware)."""
import numpy as np, trimesh
from manifold3d import Manifold, CrossSection, Mesh, OpType

IN = 25.4
CUT_Z = 52.0            # mm: above the tang/slant transition in the source block (stub is clean from ~z=52 up)
BASE_L, BASE_W, BASE_T = 2.64*IN, 1.34*IN, 0.40*IN   # Rev C: no ears, bolts from below
BOLT_CC = 1.60*IN
NUT_AF_POCKET = 11.4                                  # hex pocket AF for a 1/4-20 nut (7/16 = 11.1 AF); flats face the stub's side walls
NUT_AF, NUT_T = 11.4, 6.0       # 1/4-20 nut 7/16 AF x 7/32 thick, with clearance
BOLT_D = 0.28*IN                # 9/32 clearance for 1/4-20
RELIEF_D, RELIEF_H = 7.0, 10.0  # blind hole above the nut for the bolt tip

def to_manifold(tm):
    return Manifold(Mesh(vert_properties=np.asarray(tm.vertices, np.float32), tri_verts=np.asarray(tm.faces, np.uint32)))

src = trimesh.load('magblock.stl')
stub = src.slice_plane(plane_origin=[0, 0, CUT_Z], plane_normal=[0, 0, 1], cap=True)
stub = trimesh.Trimesh(stub.vertices, stub.faces, process=True); stub.update_faces(stub.nondegenerate_faces()); stub.remove_unreferenced_vertices()
print('stub watertight', stub.is_watertight, 'bounds', stub.bounds.round(1).tolist())
c = stub.bounds.mean(axis=0)               # center the stub in XY, sit it at z = BASE_T
stub.apply_translation([-c[0], -c[1], -CUT_Z + BASE_T - 0.2])   # sink 0.2 mm into the base so the union overlaps instead of sharing a face
# stub long axis is the block's Y (front-to-back of the mag); rotate so it runs along X (the keel / barrel axis)
stub.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [0, 0, 1]))
stub_m = to_manifold(stub)
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
tm.export('dock_mag_insert_v4.stl')
chk = trimesh.load('dock_mag_insert_v4.stl')
print('insert watertight', chk.is_watertight, 'bounds in', (chk.bounds/IN).round(2).tolist(), 'vol in3', round(chk.volume/16387.064, 2), 'faces', len(chk.faces))
