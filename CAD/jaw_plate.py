"""Doyle vee jaw — Rev S steel plate (laser cut, 1/4" mild steel). DRAFT: tab depth assumes a 0.30" OEM pad.
Section coordinates: Y from the casting mounting face (+ toward the work), Z from the jaw bottom, inches.
The plate is the Rev R2 jaw profile with:
  FLUSH (bears on the vise / pad): back face Y=0 (Z 0-0.75), bottom (plate seat ledge), saddle underside (casting top),
        tab front at Y = band + pad_proud - pad_thk (the OEM pad clamps this edge), band underside (sits on the pad top)
  RECESSED 0.06 (only plastic touches the work): both vee faces + apex, band face, band top (plate stops under the foam slot)
  RECESSED 0.04 (plate hides under the plastic): back wedge / logo face, saddle riser, top face
Holes: three 11/32" round on one column (Y = 0.33, Z = 0.80 / 2.10 / 3.35) for 5/16-18 x 5" SHCS + Grade 8 hex nuts. The bottom
  one cannot go lower: the 1/4-20 mounting screws cross the jaw at Z = 0.35 (hole Z 0.21-0.49). Same DXF for every plate.
Outputs: jaw_plate_S.dxf (inches, closed LWPOLYLINEs on layer CUT), jaw_plate_S.png, coordinates printed.
"""
import math, ezdxf
from shapely.geometry import Polygon

# Rev R2 jaw numbers
SEAT_H = 0.75; APEX_Z = 2.75; VH = 1.00; B2A = 0.60; ANG = 15.0
SADDLE_D = 0.35; SADDLE_T = 0.40; TOP_Z = APEX_Z + VH
t = math.tan(math.radians(ANG)); c = math.cos(math.radians(ANG))
VEE_EDGE_Y = B2A + VH * t                     # 0.868
BAND_Y = VEE_EDGE_Y + 0.325                   # 1.193
BAND_TOP_Z = APEX_Z - VH - 0.30               # 1.45
PAD_T = 0.30                                  # ASSUMED — measure the pad
PAD_PROUD = 0.10
TAB_Y = BAND_Y + PAD_PROUD - PAD_T            # 0.993
R_WORK, R_COSM = 0.06, 0.04
HOLE_D = 0.344; HOLES = [(0.33, 0.80), (0.33, 2.10), (0.33, 3.35)]   # 11/32 round, one column, 3x 5/16-18 SHCS + hex nut
HEAD_D = 0.469
EASE = 0.03

def lower_face_y(z, r=0.0): return B2A + (APEX_Z - z) * t - r / c      # lower vee face, recessed r inward
def upper_face_y(z, r=0.0): return B2A + (z - APEX_Z) * t - r / c
# back wedge line (-SADDLE_D, SEAT_H+SADDLE_T) -> (0, TOP_Z), recessed r toward +Y
wl = math.hypot(SADDLE_D, TOP_Z - SEAT_H - SADDLE_T); nx, nz = (TOP_Z - SEAT_H - SADDLE_T) / wl, -SADDLE_D / wl
def wedge_y(z, r=0.0):
    z0 = SEAT_H + SADDLE_T + nz * r; y0 = -SADDLE_D + nx * r
    return y0 + (z - z0) * SADDLE_D / (TOP_Z - SEAT_H - SADDLE_T)

ZT = TOP_Z - R_COSM; ZB = BAND_TOP_Z - R_WORK
pts = [
    (0, 0), (TAB_Y, 0), (TAB_Y, SEAT_H),                       # bottom, tab front (pad bears here)
    (BAND_Y - R_WORK, SEAT_H), (BAND_Y - R_WORK, ZB),           # band underside on the pad top, band face recessed
    (lower_face_y(ZB, R_WORK), ZB),                             # band top recessed, meets the recessed lower face
    (B2A + R_WORK / c, APEX_Z),                                 # recessed apex
    (upper_face_y(ZT, R_WORK), ZT), (wedge_y(ZT, R_COSM), ZT),  # recessed upper face to the recessed top
    (wedge_y(SEAT_H + SADDLE_T, R_COSM), SEAT_H + SADDLE_T),    # recessed wedge line down to the saddle riser top
    (-SADDLE_D + R_COSM, SEAT_H + SADDLE_T), (-SADDLE_D + R_COSM, SEAT_H),   # riser recessed 0.04
    (0, SEAT_H),                                                # saddle underside flush on the casting top
]
plate = Polygon(pts)
assert plate.is_valid
plate = plate.buffer(-EASE, join_style=1).buffer(EASE, join_style=1).simplify(0.001)
outline = list(plate.exterior.coords)

doc = ezdxf.new('R2010'); doc.header['$INSUNITS'] = 1
msp = doc.modelspace()
msp.add_lwpolyline(outline, close=True, dxfattribs={'layer': 'CUT'})
for (hx, hy) in HOLES: msp.add_circle((hx, hy), HOLE_D / 2, dxfattribs={'layer': 'CUT'})
doc.saveas('/mnt/user-data/outputs/jaw_plate_S.dxf')

b = plate.bounds
print(f"plate: {b[2]-b[0]:.3f} wide x {b[3]-b[1]:.3f} tall, area {plate.area:.2f} in^2, {plate.area*0.25*0.284:.2f} lb in 1/4 steel")
print(f"tab front Y={TAB_Y:.3f} (pad front {TAB_Y+PAD_T:.3f}, band {BAND_Y:.3f})")
for (hx, hy) in HOLES:
    from shapely.geometry import Point
    print(f"hole ({hx}, {hy}): min wall {plate.exterior.distance(Point(hx, hy)) - HOLE_D/2:.3f}")
print('profile points:'); [print(f"  ({y:7.3f}, {z:6.3f})") for y, z in pts]

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Rectangle, Circle
plastic = [(0, 0), (0, SEAT_H), (-SADDLE_D, SEAT_H), (-SADDLE_D, SEAT_H + SADDLE_T), (0, TOP_Z), (VEE_EDGE_Y, TOP_Z), (B2A, APEX_Z),
           (VEE_EDGE_Y, APEX_Z - VH), (VEE_EDGE_Y, BAND_TOP_Z), (BAND_Y, BAND_TOP_Z), (BAND_Y, SEAT_H), (TAB_Y, SEAT_H), (TAB_Y, 0)]
fig, ax = plt.subplots(figsize=(7, 9)); ax.set_aspect('equal')
ax.add_patch(Rectangle((-2.0, -0.6), 2.0, 1.35, fc='#c8443a', alpha=0.25)); ax.add_patch(Rectangle((0, -0.6), 0.375, 0.6, fc='#c8443a', alpha=0.25))
ax.add_patch(MP(plastic, closed=True, fc='#bbb', ec='#666', lw=0.8, alpha=0.5, label='plastic segment (Rev R2 profile)'))
ax.add_patch(MP(outline, closed=True, fc='#9aa7b5', ec='k', lw=1.5, label='steel plate, 1/4"'))
ax.add_patch(Rectangle((TAB_Y, 0), PAD_T, SEAT_H, fc='none', ec='k', lw=1, ls='--', label='OEM pad (0.30 assumed)'))
ax.add_patch(Rectangle((-0.05, 0.35 - 0.14), TAB_Y + PAD_T + 0.1, 0.28, fc='#c8443a', alpha=0.35, ec='none', label='1/4-20 mounting screw path (in the plastic)'))
for (hx, hy) in HOLES:
    ax.add_patch(Circle((hx, hy), HOLE_D/2, fc='white', ec='k'))
    ax.add_patch(Circle((hx, hy), HEAD_D/2, fc='none', ec='k', ls=':', lw=0.8))   # SHCS head footprint
ax.set_xlim(-1.0, 2.0); ax.set_ylim(-0.7, 4.1); ax.grid(alpha=0.3); ax.legend(loc='upper right', fontsize=8)
ax.set_xlabel('Y from casting face (in)'); ax.set_ylabel('Z from jaw bottom (in)')
ax.set_title('Rev S plate: flush on the casting/pad side, 0.06 under the work faces, 0.04 under logo/top\n'
             f'three 11/32" holes on one column at Y=0.33 (Z 0.80 / 2.10 / 3.35), 5/16-18 SHCS (dotted = head).  DRAFT — pad assumed', fontsize=9)
fig.savefig('/mnt/user-data/outputs/jaw_plate_S.png', dpi=120, bbox_inches='tight')
