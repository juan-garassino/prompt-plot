"""r03 survey: the slab and the view, together (SYNTH r02 -> r03).

For every (H_top, hinge, elevation) it measures, in UNIT screen coordinates
(k-independent, roll-independent -- roll and crop are a rigid screen motion
and are surveyed afterwards on the chosen row):

  X gaps     interior hidden stretches of the two index-0 strings (screen units)
  X end      hidden stretch at either end (allowed only if the frame crops it)
  angle      on-sheet crossing angle of the X (deg)
  circle     visible fraction of the waist circle, and its largest gap (units)
  pinch      every pencil member visible within 0.25 unit of p on BOTH sides
  graze      the 31.72 deg ellipse's z = -2 vertex is visible
  eye        height / width of the enclosed see-through lens (units)

Exact visibility: P hidden iff t* = -2 P.D.v / v.D.v > 0 and z(t*) in slab.

usage: .venv/bin/python studio/millennium-hodge/rounds/r03/survey.py [coarse|wide|fine]
"""

from __future__ import annotations

import math
import sys

import numpy as np

D = np.array([1.0, 1.0, -1.0])
ZLO = -2.0
PSI = (15.0, math.degrees(math.atan(2.0) / 2.0), 45.0, 60.0, 75.0)


def basis(e_deg):
    e = math.radians(e_deg)
    v = np.array([math.cos(e), 0.0, math.sin(e)])
    r = np.array([0.0, 1.0, 0.0])
    u = np.array([-math.sin(e), 0.0, math.cos(e)])
    return v, r, u


def visible(P, v, zhi):
    vDv = float((v * D) @ v)
    t = -2.0 * ((P * D) @ v) / vDv
    Z = P[..., 2] + t * v[2]
    return ~((t > 1e-9) & (Z >= ZLO - 1e-12) & (Z <= zhi + 1e-12))


def proj(P, r, u):
    return np.stack([P @ r, P @ u], -1)


def sA(a, s):
    return np.stack([np.cos(a) - s * np.sin(a), np.sin(a) + s * np.cos(a), s], -1)


def sB(a, s):
    return np.stack([np.cos(a) + s * np.sin(a), np.sin(a) - s * np.cos(a), s], -1)


def pencil(a0, psi, th):
    n = np.array([math.cos(a0), math.sin(a0), 0.0])
    l = np.array([-math.sin(a0), math.cos(a0), 0.0])
    zh = np.array([0.0, 0.0, 1.0])
    w = np.cos(th)[:, None] * l + np.sin(th)[:, None] * (math.cos(psi) * n + math.sin(psi) * zh)
    den = np.cos(th) ** 2 + np.sin(th) ** 2 * math.cos(2 * psi)
    lam = -2.0 * np.sin(th) * math.cos(psi) / den
    return n + lam[:, None] * w


def runs(mask):
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


def x_string(F, a0, zhi, v, r, u):
    s = np.linspace(ZLO, zhi, 6001)
    P = F(a0, s)
    S = proj(P, r, u)
    vis = visible(P, v, zhi)
    seg = np.hypot(*np.diff(S, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    hid = runs(~vis)
    interior = [cum[j] - cum[i] for i, j in hid if i > 0 and j < len(s) - 1]
    end_lo = cum[hid[0][1]] if hid and hid[0][0] == 0 else 0.0
    end_hi = cum[-1] - cum[hid[-1][0]] if hid and hid[-1][1] == len(s) - 1 else 0.0
    d = S[-1] - S[0]
    return dict(interior=interior, end_lo=end_lo, end_hi=end_hi, length=cum[-1], dir=d / np.linalg.norm(d),
                vis_frac=float(vis.mean()), S=S, vis=vis, s=s)


def eye(v, r, u, zhi, n=360):
    xs = np.linspace(-3.2, 3.2, n)
    ys = np.linspace(-3.2, 3.2, n)
    X, Y = np.meshgrid(xs, ys)
    O = X[..., None] * r + Y[..., None] * u
    a = float((v * D) @ v)
    b = 2.0 * ((O * D) @ v)
    c = (O * O * D).sum(-1) - 1.0
    disc = b * b - 4 * a * c
    sq = np.sqrt(np.maximum(disc, 0))
    hit = np.zeros(X.shape, bool)
    for sg in (-1, 1):
        t = (-b + sg * sq) / (2 * a)
        z = O[..., 2] + t * v[2]
        hit |= (disc >= 0) & (z >= ZLO) & (z <= zhi)
    free = ~hit
    # flood from the border: what is left free and unreached is the eye
    reach = np.zeros_like(free)
    reach[0, :] = free[0, :]
    reach[-1, :] = free[-1, :]
    reach[:, 0] = free[:, 0]
    reach[:, -1] = free[:, -1]
    while True:
        g = reach.copy()
        g[1:] |= reach[:-1]
        g[:-1] |= reach[1:]
        g[:, 1:] |= reach[:, :-1]
        g[:, :-1] |= reach[:, 1:]
        g &= free
        if (g == reach).all():
            break
        reach = g
    lens = free & ~reach
    if not lens.any():
        return 0.0, 0.0
    yy, xx = np.nonzero(lens)
    dx = xs[1] - xs[0]
    return float((ys[yy].max() - ys[yy].min()) + dx), float((xs[xx].max() - xs[xx].min()) + dx)


def survey_one(zhi, hinge, elev):
    v, r, u = basis(elev)
    a0 = math.radians(hinge)
    XA = x_string(sA, a0, zhi, v, r, u)
    XB = x_string(sB, a0, zhi, v, r, u)
    cosang = abs(float(XA["dir"] @ XB["dir"]))
    ang = math.degrees(math.acos(min(1.0, cosang)))
    # waist circle
    t = np.linspace(0, 2 * math.pi, 7201)
    C = np.stack([np.cos(t), np.sin(t), 0 * t], -1)
    vis = visible(C, v, zhi)
    S = proj(C, r, u)
    seg = np.hypot(*np.diff(S, axis=0).T)
    tot = seg.sum()
    visl = seg[vis[:-1] & vis[1:]].sum()
    gaps = []
    # wrap: rotate so we start at a visible sample
    k0 = int(np.argmax(vis))
    vr = np.roll(vis, -k0)
    sr = np.roll(np.concatenate([seg, [seg[0]]]), -k0)
    for i, j in runs(~vr):
        gaps.append(float(sr[i - 1 : j + 1].sum()))
    circ_frac = float(visl / tot)
    circ_gap = max(gaps) if gaps else 0.0
    # pinch: each member visible within 0.25 unit of p on both sides
    p = np.array([math.cos(a0), math.sin(a0), 0.0])
    ps = proj(p[None], r, u)[0]
    pinch_ok = True
    for psi in PSI:
        for th in (np.linspace(1e-4, 0.6, 400), np.linspace(math.pi - 0.6, math.pi - 1e-4, 400)):
            P = pencil(a0, math.radians(psi), th)
            fin = np.isfinite(P).all(-1)
            P = P[fin]
            Sp = proj(P, r, u)
            near = np.hypot(*(Sp - ps).T) < 0.25
            inside = (P[:, 2] >= ZLO) & (P[:, 2] <= zhi)
            m = near & inside
            if not m.any() or not visible(P[m], v, zhi).all():
                pinch_ok = False
    # graze: the z-min point of the 31.72 member
    th = np.linspace(1e-4, math.pi - 1e-4, 20001)
    P = pencil(a0, math.radians(PSI[1]), th)
    j = int(np.nanargmin(P[:, 2]))
    graze_vis = bool(visible(P[j][None], v, zhi)[0])
    ell = {}
    for psi in (PSI[0], PSI[1]):
        th = np.linspace(1e-5, math.pi - 1e-5, 20001)
        P = pencil(a0, math.radians(psi), th)
        vis = visible(P, v, zhi)
        Sx = proj(P, r, u)
        sg = np.hypot(*np.diff(Sx, axis=0).T)
        tot = sg.sum()
        gaps = [float(sg[i - 1 : j].sum()) for i, j in runs(~vis) if i > 0]
        ell[psi] = (float(sg[vis[:-1] & vis[1:]].sum() / tot), max(gaps, default=0.0))
    eh, ew = eye(v, r, u, zhi)
    return dict(
        zhi=zhi, hinge=hinge, elev=elev,
        gA=max(XA["interior"], default=0.0), gB=max(XB["interior"], default=0.0),
        nA=len(XA["interior"]), nB=len(XB["interior"]),
        endA=(XA["end_lo"], XA["end_hi"]), endB=(XB["end_lo"], XB["end_hi"]),
        lenA=XA["length"], lenB=XB["length"],
        ang=ang, circ=circ_frac, cgap=circ_gap, pinch=pinch_ok, graze=graze_vis,
        eye_h=eh, eye_w=ew, ell=ell,
    )


def main():
    grids = {
        "coarse": ([2.0, 1.6, 1.4, 1.2, 1.0, 0.9, 0.8, 0.7, 0.6], range(330, 361, 5), [48, 50, 52, 54, 56]),
        "wide": ([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0], range(300, 361, 5), [48, 49]),
        "fine": ([0.4, 0.5, 0.6, 0.7, 0.8], range(310, 361, 2), [48]),
    }
    g = sys.argv[1] if len(sys.argv) > 1 else "coarse"
    zhis, hinges, elevs = grids[g]
    rows = []
    for zhi in zhis:
        for h in hinges:
            for e in elevs:
                rows.append(survey_one(zhi, h, e))
    print("zhi  hinge elev | Xgap A/B (u)  endA lo/hi   endB lo/hi | angle | circ  cgap | pinch graze | eye h x w (u) | ell15 vis/gap  ell31.7 vis/gap")
    for q in rows:
        print(
            f"{q['zhi']:4.2f} {q['hinge']:5.0f} {q['elev']:4.0f} | {q['gA']:5.3f}/{q['gB']:5.3f} "
            f" {q['endA'][0]:4.2f}/{q['endA'][1]:4.2f}  {q['endB'][0]:4.2f}/{q['endB'][1]:4.2f} |"
            f" {q['ang']:5.1f} | {q['circ']:.3f} {q['cgap']:.3f} | {str(q['pinch'])[0]}     {str(q['graze'])[0]}"
            f"     | {q['eye_h']:.2f} x {q['eye_w']:.2f}"
            f" | {q['ell'][PSI[0]][0]:.3f}/{q['ell'][PSI[0]][1]:.3f}  {q['ell'][PSI[1]][0]:.3f}/{q['ell'][PSI[1]][1]:.3f}"
        )


if __name__ == "__main__":
    main()
