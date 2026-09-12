"""2D plane-strain FE of the Doyle vee jaw section with the OEM steel pad clamped outboard of a printed tab.
Sweep the tab thickness t (casting face -> pad back face). Q4 bilinear elements on a raster mesh, penalty contact
(compression-only) against the casting face, the plate-seat ledge and the casting top under the saddle; screw preload +
screw axial stiffness at Z = 0.35 in. Loads: (a) keel — 1000 lbf per jaw split over both vee faces; (b) big round —
1000 lbf high on the upper face. Units: inch, lbf, psi. Per-unit-length model, jaw length 4.50 in.
"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
from shapely.geometry import Polygon, Point, LineString
from shapely import vectorized

JAW_L = 4.5
E_SOLID, E_CORE_FRAC, NU = 750e3, 0.25, 0.35     # PA612-CF15 solid (~5.2 GPa); 40 % 3D honeycomb core ~ 1/4 of solid
SKIN = 5 * 0.6 / 25.4                              # 5 walls x 0.6 mm
E_STEEL = 30e6
PAD_T, PAD_H = 0.30, 0.75                          # assumed pad
SCREW_Z, SCREW_A, N_SCREW = 0.35, 0.0318, 2
H = 0.025                                          # cell size

BAND_X = 1.195
def jaw_poly(t, rabbet=True, band_x=None):
    BAND_X = band_x or 1.2
    pts = [(0, 0), (0, 0.75), (-0.35, 0.75), (-0.35, 1.15), (0, 3.75), (0.87, 3.75), (0.60, 2.75), (0.87, 1.75),
           (0.87, 1.45), (0.97, 1.45), (0.97, 1.75), (1.115, 1.75), (1.115, 1.45), (BAND_X, 1.45)]
    if rabbet and t < BAND_X - 1e-9: pts += [(BAND_X, PAD_H), (t, PAD_H), (t, 0)]
    else: pts += [(BAND_X, 0)]
    return Polygon(pts)

def build(t, solid_tab=True, preload=2000.0, case='keel', F=1000.0, rabbet=True, pad=True, band_x=1.2):
    t = -0.35 + round((t + 0.35) / H) * H
    body = jaw_poly(t, rabbet, band_x)
    padpoly = Polygon([(t, 0), (t + PAD_T, 0), (t + PAD_T, PAD_H), (t, PAD_H)]) if pad else None
    y0, y1 = -0.35, max(band_x, t + PAD_T) + H; z0, z1 = 0.0, 3.75
    ny, nz = int(round((y1 - y0) / H)), int(round((z1 - z0) / H))
    yc = y0 + (np.arange(ny) + 0.5) * H; zc = z0 + (np.arange(nz) + 0.5) * H
    YC, ZC = np.meshgrid(yc, zc, indexing='ij')
    in_body = vectorized.contains(body, YC.ravel(), ZC.ravel()).reshape(YC.shape)
    in_pad = vectorized.contains(padpoly, YC.ravel(), ZC.ravel()).reshape(YC.shape) if pad else np.zeros_like(in_body)
    active = in_body | in_pad
    # material per cell
    bnd = body.exterior
    d = np.array([bnd.distance(Point(y, z)) for y, z in zip(YC[in_body], ZC[in_body])])
    E = np.zeros(YC.shape)
    Eb = np.where(d < SKIN, E_SOLID, E_SOLID * E_CORE_FRAC)
    if solid_tab: Eb = np.where(ZC[in_body] < PAD_H + 1e-9, E_SOLID, Eb)
    E[in_body] = Eb; E[in_pad] = E_STEEL
    # nodes
    nid = -np.ones((ny + 1, nz + 1), int)
    cells = np.argwhere(active)
    for i, j in cells:
        for a, b in ((i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)): nid[a, b] = 0
    nodes = np.argwhere(nid == 0); nid[nid == 0] = np.arange(len(nodes))
    NY = y0 + nodes[:, 0] * H; NZ = z0 + nodes[:, 1] * H
    ndof = 2 * len(nodes)
    # Q4 plane-strain stiffness (square element, 2x2 Gauss)
    g = 1 / np.sqrt(3); gp = [(-g, -g), (g, -g), (g, g), (-g, g)]
    def kel(Em):
        D = Em / ((1 + NU) * (1 - 2 * NU)) * np.array([[1 - NU, NU, 0], [NU, 1 - NU, 0], [0, 0, (1 - 2 * NU) / 2]])
        K = np.zeros((8, 8))
        for xi, eta in gp:
            dN = np.array([[-(1 - eta), (1 - eta), (1 + eta), -(1 + eta)], [-(1 - xi), -(1 + xi), (1 + xi), (1 - xi)]]) / 4 * (2 / H)
            B = np.zeros((3, 8))
            for a in range(4):
                B[0, 2 * a] = dN[0, a]; B[1, 2 * a + 1] = dN[1, a]; B[2, 2 * a] = dN[1, a]; B[2, 2 * a + 1] = dN[0, a]
            K += B.T @ D @ B * (H / 2) ** 2
        return K
    K1 = kel(1.0)
    rows, cols, vals = [], [], []
    for i, j in cells:
        n = [nid[i, j], nid[i + 1, j], nid[i + 1, j + 1], nid[i, j + 1]]
        dofs = np.array([[2 * k, 2 * k + 1] for k in n]).ravel()
        Ke = K1 * E[i, j]
        rows.append(np.repeat(dofs, 8)); cols.append(np.tile(dofs, 8)); vals.append(Ke.ravel())
    K = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), (ndof, ndof)).tocsr()
    # contact candidates (node sets)
    tol = 1e-6
    face = np.where((np.abs(NY) < tol) & (NZ <= PAD_H + tol))[0]                       # casting face, Y springs
    ledge = np.where((np.abs(NZ) < tol) & (NY >= -tol) & (NY <= 0.375 + tol))[0]       # plate seat, Z springs
    saddle = np.where((np.abs(NZ - 0.75) < tol) & (NY <= tol) & (NY >= -0.35 - tol))[0]  # casting top, Z springs
    # screw: pad front node nearest Z=0.35
    if pad:
        low = NZ < PAD_H - tol; front = np.where(low & (np.abs(NY - NY[low].max()) < tol))[0]
        sn = front[np.argmin(np.abs(NZ[front] - SCREW_Z))]
    else:
        low = NZ < PAD_H - tol; front = np.where(low & (np.abs(NY - NY[low].max()) < tol))[0]
        sn = front[np.argmin(np.abs(NZ[front] - SCREW_Z))]
    per_len = N_SCREW / JAW_L
    k_screw = E_STEEL * SCREW_A / ((t + PAD_T) if pad else t) * per_len
    # loads
    f = np.zeros(ndof)
    f[2 * sn] -= preload * per_len                                                  # screw preload pulls the pad onto the casting
    bnd_nodes = np.where(vectorized.contains(body.exterior.buffer(0.02), NY, NZ))[0]
    def face_nodes(p, q):
        L = LineString([p, q]); return np.array([n for n in bnd_nodes if L.distance(Point(NY[n], NZ[n])) < 0.02])
    up = face_nodes((0.60, 2.75), (0.87, 3.75)); lo = face_nodes((0.60, 2.75), (0.87, 1.75))
    n_up = np.array([-0.966, 0.259]); n_lo = np.array([-0.966, -0.259])              # pressing directions
    Fl = F / JAW_L
    if case == 'keel':
        for ns, nv in ((up, n_up), (lo, n_lo)):
            for n in ns: f[2 * n:2 * n + 2] += nv * Fl / 2 / len(ns)
    elif case == 'round':
        hi = up[NZ[up] > 3.45]
        for n in hi: f[2 * n:2 * n + 2] += n_up * Fl / len(hi)
    elif case == 'low':
        lw = lo[NZ[lo] < 2.05]
        for n in lw: f[2 * n:2 * n + 2] += n_lo * Fl / len(lw)
    # solve with compression-only penalty springs
    kc = 5e7 * H
    act_f = np.ones(len(face), bool); act_l = np.ones(len(ledge), bool); act_s = np.ones(len(saddle), bool)
    for it in range(30):
        diag = np.zeros(ndof)
        diag[2 * face[act_f]] += kc; diag[2 * ledge[act_l] + 1] += kc; diag[2 * saddle[act_s] + 1] += kc
        diag[2 * sn] += k_screw; diag[2 * sn + 1] += 1e6      # screw axial + shear/friction
        Ks = K + sp.diags(diag)
        u = spl.spsolve(Ks.tocsc(), f)
        nf = u[2 * face] < 0; nl = u[2 * ledge + 1] < 0; ns_ = u[2 * saddle + 1] < 0
        if (nf == act_f).all() and (nl == act_l).all() and (ns_ == act_s).all(): break
        act_f, act_l, act_s = nf, nl, ns_
    apex = np.argmin(np.hypot(NY - 0.60, NZ - 2.75)); top = np.argmin(np.hypot(NY - 0.87, NZ - 3.75))
    gap = max(0.0, u[2 * face[np.argmin(NZ[face])]])            # opening at the bottom of the casting face
    contact_len = act_f.sum() * H
    # screw tension = preload + spring extension
    T = preload + k_screw * u[2 * sn] / per_len
    # max principal stress in the plastic (element-wise, centre)
    smax = 0.0
    dNc = np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]) / 4 * (2 / H)
    for i, j in cells:
        if in_pad[i, j]: continue
        n = [nid[i, j], nid[i + 1, j], nid[i + 1, j + 1], nid[i, j + 1]]
        ue = np.array([[u[2 * k], u[2 * k + 1]] for k in n])
        exx = dNc[0] @ ue[:, 0]; ezz = dNc[1] @ ue[:, 1]; gxz = dNc[1] @ ue[:, 0] + dNc[0] @ ue[:, 1]
        Em = E[i, j]; D = Em / ((1 + NU) * (1 - 2 * NU))
        sxx = D * ((1 - NU) * exx + NU * ezz); szz = D * (NU * exx + (1 - NU) * ezz); sxz = D * (1 - 2 * NU) / 2 * gxz
        s1 = (sxx + szz) / 2 + np.hypot((sxx - szz) / 2, sxz)
        smax = max(smax, s1)
    return dict(t=t, apex_dy=u[2 * apex], apex_dz=u[2 * apex + 1], top_dy=u[2 * top], gap=gap, contact=contact_len,
                screw_T=T, smax=smax, nodes=len(nodes), u=u, NY=NY, NZ=NZ, E=E, cells=cells, nid=nid, in_pad=in_pad)

if __name__ == '__main__':
    import json
    out = []
    print("F = 1000 lbf per jaw, preload 2000 lbf/screw, pad 0.30 thick. band face at 1.20")
    for case in ('keel', 'round'):
        for t in (0.35, 0.475, 0.60, 0.80, 0.90, 1.00, 1.20):
            r = build(t, case=case)
            print(f"{case:5s} t={r['t']:5.3f} pad front={r['t']+PAD_T:5.3f}  apex dY={r['apex_dy']*1000:7.2f} mil  top dY={r['top_dy']*1000:7.2f} mil  "
                  f"gap={r['gap']*1000:5.2f} mil  contact={r['contact']:.2f} in  screw T={r['screw_T']:6.0f} lbf  s1max={r['smax']:6.0f} psi")
            out.append(dict(case=case, t=float(r['t']), apex=float(r['apex_dy']), top=float(r['top_dy']), gap=float(r['gap']), T=float(r['screw_T']), smax=float(r['smax'])))
    print("--- variants (keel case) ---")
    for label, kw in (('t=0.475, tab left at 40% infill', dict(t=0.475, solid_tab=False)),
                      ('t=0.475, preload 500', dict(t=0.475, preload=500.0)),
                      ('t=1.0, preload 500', dict(t=1.0, preload=500.0)),
                      ('t=0.475, band pulled back to 0.775 (pad flush)', dict(t=0.475, band_x=0.775)),
                      ('t=0.675, band pulled back to 0.975 (pad flush)', dict(t=0.675, band_x=0.975)),
                      ('no pad, fenders modelled as bonded face, t=1.2', dict(t=1.2, pad=False, rabbet=False)),
                      ('round case, t=0.475, preload 500', dict(t=0.475, preload=500.0, case='round')),
                      ('round case, t=1.0, preload 500', dict(t=1.0, preload=500.0, case='round'))):
        a = dict(case='keel'); a.update(kw)
        r = build(**a)
        print(f"{label:48s} apex dY={r['apex_dy']*1000:7.2f} mil  gap={r['gap']*1000:5.2f} mil  contact={r['contact']:.2f}  screw T={r['screw_T']:6.0f}  s1max={r['smax']:6.0f}")
    json.dump(out, open('/home/claude/jaw_fea_sweep.json', 'w'), indent=1)
