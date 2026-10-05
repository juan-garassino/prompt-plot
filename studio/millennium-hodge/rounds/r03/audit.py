"""Gcode audit for millennium-hodge r03 (iterate).  Reads the RENDERED gcode and
re-checks every r03 mandate a critic can re-run.  The exact model (view, conics,
visibility) is recomputed here from first principles; only the view numbers and
the slab are read from piece.py.

  1  straight: every GOLD / BLUE stroke is collinear within 0.01 mm
  2  same-colour near-parallel spacing (X / rebus band passes are one mark)
  3  the eye: area, size, ink inside
  4  A1  the X: each index-0 centre pass as runs along its line -- gaps, ends,
         length, on-sheet angle; X band passes per colour
  5  A3  blue / gold fragments shorter than 8 mm (rebus excluded)
  6  S1 / A2  green: per pencil member, visible length vs drawn; every
         UNDRAWN visible stretch, classified (stagger at p / other); the waist
         circle's drawn fraction and largest gap; stop distances from p; the
         31.72 deg graze vertex drawn or not
  7  length / strokes per layer (minutes: use `promptplot plot plate --dry-run`)

usage: .venv/bin/python studio/millennium-hodge/rounds/r03/audit.py <file.gcode>
(A3 portrait, margin 15: design sheet == paper)
"""

from __future__ import annotations

import importlib.util
import math
import re
import sys
from pathlib import Path

import numpy as np


def load(path):
    strokes, cur, col, pos = [], None, None, (0.0, 0.0)
    for ln in open(path):
        body = ln.split(";", 1)[0].strip()
        m = re.search(r"color=(\d+)", ln)
        if body.startswith("M3"):
            cur, col = [pos], int(m.group(1)) if m else col
        elif body.startswith("M5"):
            if cur and len(cur) > 1:
                strokes.append((col, np.array(cur)))
            cur = None
        elif body.startswith(("G0", "G1")):
            x = re.search(r"X([-\d.]+)", body)
            y = re.search(r"Y([-\d.]+)", body)
            pos = (float(x.group(1)) if x else pos[0], float(y.group(1)) if y else pos[1])
            if body.startswith("G1") and cur is not None:
                cur.append(pos)
    return strokes


def seg_dist_many(q, P):
    """min distance from points q (n,2) to polyline P (m,2)."""
    a, b = P[:-1], P[1:]
    ab = b - a
    L2 = np.maximum((ab * ab).sum(-1), 1e-18)
    t = np.clip(((q[:, None, :] - a[None]) * ab[None]).sum(-1) / L2[None], 0, 1)
    d = a[None] + t[..., None] * ab[None] - q[:, None, :]
    return np.sqrt((d * d).sum(-1)).min(1)


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


def main(path):
    st = load(path)
    spec = importlib.util.spec_from_file_location("pc", Path(__file__).with_name("piece.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["pc"] = m
    spec.loader.exec_module(m)
    view = m.View(**m.VIEW)
    ZLO, ZHI = m.ZLO, m.ZHI
    m.hodge_circle_is_two_lines(None, (15, 15, 282, 405), 4)  # fills STATS
    rb = m.STATS["rebus_box"]
    names = {0: "GOLD", 1: "BLUE", 2: "GREEN", 3: "TEXT"}
    in_rebus = [all(rb[0] - 1 <= x <= rb[2] + 1 and rb[1] - 1 <= y <= rb[3] + 1 for x, y in p) for c, p in st]
    a0 = view.a0
    xa = view.proj(m.string_A(a0, [ZLO, ZHI]))
    xb = view.proj(m.string_B(a0, [ZLO, ZHI]))

    def on_line(p, e):
        d = (e[1] - e[0]) / np.linalg.norm(e[1] - e[0])
        nrm = np.array([-d[1], d[0]])
        return np.abs((p - e[0]) @ nrm)

    band = set()
    for k, (c, p) in enumerate(st):
        if c in (0, 1) and len(p) == 2 and not in_rebus[k]:
            e = xa if c == 1 else xb
            if on_line(p, e).max() < 0.6:
                band.add(k)
    # 1 straightness
    worst, n_multi = 0.0, 0
    for c, p in st:
        if c in (0, 1) and len(p) > 2:
            n_multi += 1
            a, b = p[0], p[-1]
            d = (b - a) / max(np.linalg.norm(b - a), 1e-9)
            worst = max(worst, float(np.abs((p - a) @ np.array([-d[1], d[0]])).max()))
    print(f"1. straight: {n_multi} gold/blue strokes with >2 points; worst deviation {worst:.4f} mm")

    # 2 same-colour near-parallel spacing
    lines = {}
    for k, (c, p) in enumerate(st):
        if len(p) == 2:
            d = (p[1] - p[0]) / max(np.linalg.norm(p[1] - p[0]), 1e-9)
            nrm = np.array([-d[1], d[0]])
            lines[k] = (nrm, float(nrm @ p[0]))

    def same_line(i, j):
        if i not in lines or j not in lines:
            return False
        (n1, o1), (n2, o2) = lines[i], lines[j]
        dot = float(n1 @ n2)
        return abs(dot) > 0.99999 and abs(o1 - np.sign(dot) * o2) < 0.03

    for c in (0, 1, 2):
        pts, tan, sid = [], [], []
        for k, (cc, p) in enumerate(st):
            if cc != c or in_rebus[k]:
                continue
            for a, b in zip(p[:-1], p[1:]):
                L = float(np.linalg.norm(b - a))
                if L < 1e-9:
                    continue
                n = max(2, int(L / 0.25))
                t = np.linspace(0, 1, n)[:, None]
                pts.append(a + t * (b - a))
                tan.append(np.repeat(((b - a) / L)[None], n, 0))
                sid.append(np.full(n, k))
        P = np.concatenate(pts)
        T = np.concatenate(tan)
        S = np.concatenate(sid)
        keys = np.floor(P).astype(int)
        grid = {}
        for i, kk in enumerate(map(tuple, keys)):
            grid.setdefault(kk, []).append(i)
        dmin, where = 9.9, None
        for i in range(0, len(P), 3):
            kx, ky = keys[i]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for j in grid.get((kx + dx, ky + dy), ()):
                        if S[j] == S[i] or (S[j] in band and S[i] in band) or same_line(S[i], S[j]):
                            continue
                        d = float(np.hypot(*(P[j] - P[i])))
                        if d < dmin and abs(float(T[i] @ T[j])) > 0.93:
                            dmin, where = d, tuple(np.round(P[i], 1))
        print(f"2. {names[c]}: min near-parallel gap between different strokes {dmin:.2f} mm at {where}")

    # 3 the eye
    X, Y = np.meshgrid(np.arange(15, 282, 0.25), np.arange(15, 405, 0.25))
    eye = view.in_eye(X, Y)
    ink, where = 0, []
    for c, p in st:
        for a_, b_ in zip(p[:-1], p[1:]):
            n = max(2, int(np.linalg.norm(b_ - a_) / 0.2))
            q = a_ + np.linspace(0, 1, n)[:, None] * (b_ - a_)
            ok = view.in_eye(q[:, 0], q[:, 1])
            for dx, dy in ((0.3, 0), (-0.3, 0), (0, 0.3), (0, -0.3)):
                ok &= view.in_eye(q[:, 0] + dx, q[:, 1] + dy)
            if ok.any():
                ink += int(ok.sum())
                where.append((names[c], tuple(np.round(q[ok][0], 1))))
    pts = np.stack([X[eye], Y[eye]], 1)
    c0 = pts.mean(0)
    _, _, vt = np.linalg.svd(pts - c0, full_matrices=False)
    pr = (pts - c0) @ vt.T
    print(
        f"3. eye: area {eye.sum() * 0.0625:.0f} mm^2, long {np.ptp(pr[:, 0]):.1f} x thick {np.ptp(pr[:, 1]):.1f} mm,"
        f" vertical extent {np.ptp(pts[:, 1]):.1f} mm; ink samples >0.3 mm inside: {ink} {where[:6]}"
    )

    # 4 the X
    print("4. the X (A1):")
    dirs = {}
    for c, e, lab in ((0, xb, "GOLD [B]"), (1, xa, "BLUE [A]")):
        d = (e[1] - e[0]) / np.linalg.norm(e[1] - e[0])
        dirs[c] = d
        centre = [p for k, (cc, p) in enumerate(st) if cc == c and k in band and on_line(p, e).max() < 0.02]
        passes = len([k for k in band if st[k][0] == c])
        iv = sorted(tuple(sorted(((p - e[0]) @ d).tolist())) for p in centre)
        merged = []
        for lo, hi in iv:
            if merged and lo <= merged[-1][1] + 0.05:
                merged[-1][1] = max(merged[-1][1], hi)
            else:
                merged.append([lo, hi])
        gaps = [round(b[0] - a[1], 2) for a, b in zip(merged, merged[1:])]
        L = sum(hi - lo for lo, hi in merged)
        full = float(np.linalg.norm(e[1] - e[0]))
        ends = [tuple(np.round(e[0] + d * merged[0][0], 1)), tuple(np.round(e[0] + d * merged[-1][1], 1))]
        print(
            f"   {lab}: {len(merged)} run(s), gaps {gaps}, drawn {L:.1f} of {full:.1f} mm rim-to-rim,"
            f" ends {ends}, {passes} passes, angle {math.degrees(math.atan2(d[1], d[0])):.2f} deg"
        )
    ang = math.degrees(math.acos(abs(float(dirs[0] @ dirs[1]))))
    print(f"   crossing angle {ang:.2f} deg (acute), {180 - ang:.2f} (obtuse)")

    # 5 fragments
    for c in (0, 1):
        lens = [
            (float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum()), tuple(np.round(p[0], 1)))
            for k, (cc, p) in enumerate(st)
            if cc == c and not in_rebus[k]
        ]
        short = sorted(q for q in lens if q[0] < 8.0)
        print(f"5. {names[c]}: {len(lens)} strokes, {len(short)} shorter than 8 mm {short[:8]}; shortest {min(lens)[0]:.2f} mm")

    # 6 the green pencil, recomputed
    green = [p for k, (c, p) in enumerate(st) if c == 2 and not in_rebus[k]]
    G = [g for g in green]
    p_scr = view.proj(np.array([[math.cos(a0), math.sin(a0), 0.0]]))[0]
    print(f"6. green (S1 / A2): p = {tuple(np.round(p_scr, 2))}")
    for psi in m.PSI_DEG:
        th = np.linspace(1e-6, math.pi - 1e-6, 40001)
        P = m.pencil_point(view, math.radians(psi), th)
        fin = np.isfinite(P).all(-1)
        P = np.where(fin[:, None], P, 0.0)
        S = view.proj(P)
        good = fin & (P[:, 2] >= ZLO) & (P[:, 2] <= ZHI) & view.visible(P) & m.in_frame(S)
        dd = np.full(len(S), 9e9)
        for g in G:
            box = (g[:, 0].min() - 1, g[:, 1].min() - 1, g[:, 0].max() + 1, g[:, 1].max() + 1)
            sel = good & (S[:, 0] > box[0]) & (S[:, 0] < box[2]) & (S[:, 1] > box[1]) & (S[:, 1] < box[3])
            if sel.any():
                idx = np.nonzero(sel)[0]
                for ch in range(0, len(idx), 4000):
                    ii = idx[ch : ch + 4000]
                    dd[ii] = np.minimum(dd[ii], seg_dist_many(S[ii], g))
        drawn = good & (dd < 0.12)
        seg = np.hypot(*np.diff(S, axis=0).T)
        seg[~(good[:-1] & good[1:])] = 0.0
        vis_len = float(seg.sum())
        dr_len = float(seg[drawn[:-1] & drawn[1:]].sum())
        und = []
        stops = []
        for i0, i1 in runs(good & ~drawn):
            Ls = float(seg[max(i0 - 1, 0) : i1 + 1].sum())
            if Ls < 0.3:
                continue
            dp0 = float(np.hypot(*(S[i0] - p_scr)))
            dp1 = float(np.hypot(*(S[i1] - p_scr)))
            at_p = min(dp0, dp1) < 12.0  # near p every member is tangent to the circle
            if at_p:
                stops.append(round(max(dp0, dp1), 1))
            else:
                und.append((round(Ls, 1), tuple(np.round(S[i0], 1)), tuple(np.round(S[i1], 1))))
        extra = ""
        if psi == 0.0:
            circ_len = float(np.hypot(*np.diff(S, axis=0).T).sum())
            gaps = []
            for i0, i1 in runs(~drawn):
                gaps.append(float(np.hypot(*np.diff(S[max(i0 - 1, 0) : i1 + 2], axis=0).T).sum()))
            # wrap-around (the circle is closed): join the first and last gaps
            if not drawn[0] and not drawn[-1] and len(gaps) > 1:
                gaps = [gaps[0] + gaps[-1]] + gaps[1:-1]
            extra = f"; CIRCLE drawn {dr_len / circ_len * 100:.1f} % of its full length, largest gap {max(gaps, default=0):.1f} mm"
        if abs(psi - m.PSI_LAST_ELLIPSE) < 1e-6:
            j = int(np.argmin(np.where(fin, P[:, 2], 9)))
            gv = S[j]
            gd = min(float(seg_dist_many(gv[None], g)[0]) for g in G)
            extra = f"; graze vertex z={P[j, 2]:.6f} at {tuple(np.round(gv, 1))}, visible {bool(view.visible(P[j][None])[0])}, nearest green {gd:.2f} mm"
        print(
            f"   psi {psi:5.2f}: visible {vis_len:6.1f} mm, drawn {dr_len:6.1f}; stagger stops from p {sorted(stops)};"
            f" other undrawn visible {und}{extra}"
        )

    # 7 budget
    for c in (0, 1, 2, 3):
        L = sum(float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum()) for cc, p in st if cc == c)
        n = sum(1 for cc, p in st if cc == c)
        print(f"7. {names[c]}: draw {L / 1000:.2f} m, {n} strokes")


if __name__ == "__main__":
    main(sys.argv[1])
