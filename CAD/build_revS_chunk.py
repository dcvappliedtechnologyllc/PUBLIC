"""Rev S test chunk in PA612-CF: ONE 4.50 in jaw with the Rev S profile — full tab to the OEM pad (pad outboard, proud of the
band), R2 vee/band/lip/saddle, the two 9/32 mounting holes (teardropped, horizontal on end) and the three 3/8 through-bolt
holes on the Y = 0.33 column (so the column can be checked against the pad and screws before the steel plates are ordered).
No segments, no plates. Prints on end like the R2 jaws. Tab depth assumes a 0.30 in pad (jaw_plate.PAD_T)."""
import numpy as np, trimesh, io, contextlib, math
from build_revS_print import prism_x, cyl_x, teardrop_y, export, JP, BOLT_HOLE_PLASTIC, SCREW_HOLE, SCREW_Z, HOLES
L = 4.5; SCREW_X = [1.05, 3.45]
chunk = prism_x(JP.plastic, L)
for (hy, hz) in HOLES: chunk = chunk - cyl_x(BOLT_HOLE_PLASTIC, -1, L + 1, hy, hz)
for sx in SCREW_X: chunk = chunk - teardrop_y(SCREW_HOLE, sx, SCREW_Z, -1, 2)
R = trimesh.transformations.rotation_matrix(-math.pi / 2, [0, 1, 0])
export(chunk, 'jaw_S_chunk_4.5in_PA612_ONEND_PRINT.stl', R)
