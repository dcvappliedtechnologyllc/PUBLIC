import trimesh, numpy as np, base64, json
IN=25.4
def pack(m, target=None):
    m=m.copy(); m.merge_vertices()
    if target and len(m.faces)>target: m=m.simplify_quadric_decimation(face_count=target)
    v=np.asarray(m.vertices,np.float32); f=np.asarray(m.faces)
    idx=f.astype(np.uint16 if len(v)<65535 else np.uint32)
    return dict(v=base64.b64encode(v.tobytes()).decode(), i=base64.b64encode(idx.tobytes()).decode(),
                i32=bool(len(v)>=65535), nf=int(len(f)), nv=int(len(v)))
parts={
 'jaw_plain': pack(trimesh.load('jaw45r2_plain.stl')),
 'jaw_dcv':   pack(trimesh.load('jaw45r2_DCV_public_upright.stl')),
 'keel':      pack(trimesh.load('dock_keel_v9.stl')),
 'insert':    pack(trimesh.load('dock_mag_insert_v5.stl'), 24000),
 'wheel':     pack(trimesh.load('handwheel_E.stl'), 14000),
 'clam':      pack(trimesh.load('rod_clamshell_viewer.stl')),
 'rod':       pack(trimesh.load('rod_viewer.stl')),
 'sPlastic':  pack(trimesh.load('jawS_plastic.stl')),
 'sPlates':   pack(trimesh.load('jawS_plates.stl')),
 'sPad':      pack(trimesh.load('jawS_pad.stl')),
 'sBolts':    pack(trimesh.load('jawS_bolts.stl')),
}
for k,p in parts.items(): print(k,p['nf'],p['nv'],len(p['v'])+len(p['i']))
json.dump(parts,open('viewer_geo.json','w'))
print('total bytes',sum(len(p['v'])+len(p['i']) for p in parts.values()))
