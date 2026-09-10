"""Layer-support check for a print-oriented STL: slice every layer (0.24 mm); material in layer i+1 that is farther than
~one layer height from any material in layer i has nothing under it (cantilever or bridge). Self-supporting parts score ~0
apart from intentional bridges. Frames are the mesh's own XY, so layers compare correctly."""
import sys, trimesh, numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
LH=0.24; REACH=LH*1.05
def layer(m,z):
    sec=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    if sec is None: return None
    rings=[Polygon(np.asarray(d)[:,:2]) for d in sec.discrete if len(d)>=4]
    rings=[r for r in rings if r.is_valid and r.area>0]; rings.sort(key=lambda r:-r.area)
    out=[]; 
    for r in rings:
        depth=sum(1 for o in rings if o is not r and o.area>r.area and o.contains(r.representative_point()))
        out.append((r,depth))
    solid=unary_union([r for r,d in out if d%2==0]); holes=[r for r,d in out if d%2==1]
    return solid.difference(unary_union(holes)) if holes else solid
def check(f, verbose=True):
    m=trimesh.load(f); z0,z1=m.bounds[:,2]; tot=0; worst=[]
    prev=layer(m,z0+LH/2)
    for z in np.arange(z0+LH*1.5, z1-0.01, LH):
        cur=layer(m,z)
        if cur is None or prev is None: prev=cur; continue
        a=cur.difference(prev.buffer(REACH)).area
        if a>0.5: worst.append((round(a,1), round(z/25.4,2)))
        tot+=a; prev=cur
    worst.sort(reverse=True)
    if verbose: print(f'{f}: unsupported {tot:.0f} mm2 total; worst layers (mm2 @ print z in): {worst[:6]}')
    return tot
if __name__=='__main__':
    for f in sys.argv[1:]: check(f)
