"""Read every data channel of the r05 plate back off the EMITTED gcode.

    .venv/bin/python studio/lstm-spirals/rounds/r05/check_plate.py <render>.gcode [trace.json]

The designed values come from ``trace.json`` (written by ``piece.write_trace``);
the drawn values are measured from the gcode only (strokes grouped by pen, in
emitted order). Nothing here re-runs the piece's geometry.

1. pen job per layer: strokes, draw, travel, max hop, pen cycles, minutes
   (Leo: F600 draw, 2000 mm/min travel, 1.0 s per lift+drop incl. dwells);
   red chain order and inter-chunk travel
2. c_t: red half-turn count about the eye, per-half-turn radial growth -> gap_t
   -> recovered mean forget gate; N/E/S/W ray gaps per turn (isotropy)
3. o_t: grey threads re-assembled from their dashes; start radius -> which
   half-turn; end -> distance to the designed comet birth; inked fraction vs
   mean o_t
4. h_t: comet roots (first black stroke at each birth) -> length / 14 mm vs RMS
5. spacing: near-parallel pairs closer than 0.8 mm within and across layers
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from statistics import median

import numpy as np

HERE = Path(__file__).resolve().parent
DRAW_F, TRAVEL_F, LIFT_S = 600.0, 2000.0, 1.0


def strokes(path):
    """[(pen, [(x,y)...]), ...] in emitted order, plus the travel before each."""
    out, cur, col, down = [], [], None, False
    pos = (0.0, 0.0)
    trav_start = None
    for line in open(path):
        m = re.search(r"color=(\d+)", line)
        cmd = line.split(";")[0].strip()
        if not cmd:
            continue
        mx, my = re.search(r"X(-?[\d.]+)", cmd), re.search(r"Y(-?[\d.]+)", cmd)
        if cmd.startswith("M3"):
            down, col = True, int(m.group(1)) if m else col
            cur = [pos]
        elif cmd.startswith("M5"):
            if down and len(cur) > 1:
                out.append((col, cur))
            down = False
        elif cmd.startswith(("G0", "G1")) and mx and my:
            p = (float(mx.group(1)), float(my.group(1)))
            if down and cmd.startswith("G1"):
                cur.append(p)
                if m:
                    col = int(m.group(1))
            pos = p
    return out


def plen(p):
    return sum(math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]) for i in range(1, len(p)))


def main():
    gpath = sys.argv[1]
    tr = json.loads(Path(sys.argv[2] if len(sys.argv) > 2 else HERE / "trace.json").read_text())
    S = strokes(gpath)
    steps = tr["steps"]
    T = len(steps)
    zr = complex(*tr["geometry"]["red_eye"])
    names = {0: "grey  o_t threads", 1: "crimson c_t coil", 2: "black h_t comets", 3: "black type"}

    # ---------------------------------------------------------------- 1 pen job
    print("## 1. pen job (emitted order)")
    print("| layer | strokes | draw mm | travel mm | max hop mm | hops>50 | cycles | min |")
    print("|---|---|---|---|---|---|---|---|")
    tot = [0, 0.0, 0.0, 0, 0.0]
    pens_seen = []
    pos = (0.0, 0.0)
    for pen in sorted({p for p, _ in S}):
        ss = [s for p, s in S if p == pen]
        pens_seen.append(pen)
        draw = sum(plen(s) for s in ss)
        hops = [math.hypot(ss[0][0][0] - pos[0], ss[0][0][1] - pos[1])]  # entry from previous layer
        for a, b in zip(ss, ss[1:]):
            hops.append(math.hypot(b[0][0] - a[-1][0], b[0][1] - a[-1][1]))
        travel = sum(hops[1:])
        pos = ss[-1][-1]
        minutes = draw / DRAW_F + (travel + hops[0]) / TRAVEL_F + len(ss) * LIFT_S / 60.0
        print(f"| {pen} {names.get(pen, '')} | {len(ss)} | {draw:.0f} | {travel:.0f} | {max(hops[1:] or [0]):.1f} | "
              f"{sum(h > 50 for h in hops[1:])} | {len(ss)} | {minutes:.1f} |")
        tot[0] += len(ss); tot[1] += draw; tot[2] += travel; tot[4] += minutes
    print(f"| total | {tot[0]} | {tot[1]:.0f} | {tot[2]:.0f} (in-layer) | | | {tot[0]} | {tot[4]:.1f} + {len(pens_seen) - 1} swaps |")
    # layer re-entry: each pen must be one contiguous block
    seq = [p for p, _ in S]
    blocks = [seq[0]] + [b for a, b in zip(seq, seq[1:]) if a != b]
    print("layer blocks in emitted order:", blocks, "(clean)" if len(blocks) == len(set(blocks)) else "(RE-ENTERED)")
    red = [s for p, s in S if p == 1]
    gaps_red = [math.hypot(b[0][0] - a[-1][0], b[0][1] - a[-1][1]) for a, b in zip(red, red[1:])]
    print(f"red: {len(red)} chunks, inter-chunk travel {sum(gaps_red):.3f} mm "
          f"(max {max(gaps_red or [0]):.3f}); first chunk starts {math.hypot(red[0][0][0] - zr.real, red[0][0][1] - zr.imag):.2f} mm from the eye")
    for a in red[1:]:
        ang = math.degrees(math.atan2(a[0][1] - zr.imag, a[0][0] - zr.real))
        print(f"   seam at ({a[0][0]:.1f}, {a[0][1]:.1f})  bearing from eye {ang:.1f} deg")

    # ---------------------------------------------------------------- 2 c_t
    print("\n## 2. c_t: the one red line")
    zs = complex(*tr["geometry"]["saddle"])
    G0, K = tr["mapping"]["G0_mm"], tr["mapping"]["K_mm"]
    line = [red[0][0]]
    for s in red:
        line.extend(s[1:])
    L = np.array([complex(*p) for p in line])
    z = L - zr
    ang = np.unwrap(np.angle(z))
    swr = ang[0] - ang  # clockwise angle swept about the red eye
    rr = np.abs(z)
    angs = np.unwrap(np.angle(L - zs))
    sws = angs[0] - angs  # ... about the saddle
    # where the line leaves the coil: radial growth per radian (over 5 deg)
    # jumps from the coil's ~0.2 mm/rad to the hand-off's ramp
    k5 = max(1, int(np.searchsorted(swr, swr[0] + math.radians(5))))
    slope = np.full(len(L), 0.0)
    for i in range(len(L) - 1):
        j = int(np.searchsorted(swr, swr[i] + math.radians(5)))
        if j < len(L) and swr[j] > swr[i]:
            slope[i] = (rr[j] - rr[i]) / (swr[j] - swr[i])
    i_dep = int(np.argmax(slope > 1.0))
    # the hand-off ends on its first crossing of the ray due WEST of the eye
    # (the coil starts due west, so that ray is swr = 0 mod 2 pi)
    lap0 = math.floor(swr[i_dep] / (2 * math.pi))
    i_w = i_dep + int(np.argmax(np.floor(swr[i_dep:] / (2 * math.pi)) > lap0))
    n_coil = swr[i_dep] / math.pi
    n_hand = (swr[i_w] - swr[i_dep]) / math.pi
    n_wrap = (sws[-1] - sws[i_w]) / math.pi
    kinds = [st["red_stretch"]["kind"] for st in steps]
    print(f"coil: the line runs on as a coil for {n_coil:.3f} half-turns about the red eye before it peels "
          f"(designed: {kinds.count('coil')} coil letters, then the hand-off hugs {tr['mapping']['handoff_hug_deg']:.0f} deg more)")
    print(f"hand-off (coil -> first ray due west of the eye): {n_hand:.3f} half-turn about the red eye; "
          f"half-turns about the red eye in all before the wraps: {swr[i_w] / math.pi:.3f}  (designed {kinds.count('coil') + 1})")
    print(f"half-turns about the saddle from there to the end: {n_wrap:.3f}  (designed {kinds.count('wrap')}, "
          f"the letters {''.join(st['ch'] for st in steps if st['red_stretch']['kind'] == 'wrap')!r})")
    print(f"total red {plen(line):.0f} mm in one chain")
    # coil: per half-turn radial growth -> gap_t -> recovered mean f
    rows = []
    for t in range(kinds.count("coil")):
        m = (swr >= t * math.pi - 1e-9) & (swr <= (t + 1) * math.pi + 1e-9) & (np.arange(len(L)) <= i_dep)
        slope_t = np.polyfit(swr[m], rr[m], 1)[0]
        gap = slope_t * 2 * math.pi
        rows.append((t, gap, (gap - G0) / K))
    err = [abs(fb - steps[t]["f_mean"]) for t, _, fb in rows]
    print(f"coil gap_t read back: {min(g for _, g, _ in rows):.3f}..{max(g for _, g, _ in rows):.3f} mm; "
          f"recovered mean f vs trace: max |err| {max(err):.4f}; distinct gaps {len({round(g, 4) for _, g, _ in rows})}/{len(rows)}")
    print("coil per-turn gaps on the rays from the eye (mm)  E / N / W / S   max/min")
    ray_rows = []
    for ray in (0.0, 0.5 * math.pi, math.pi, 1.5 * math.pi):
        rs = []
        for i in range(1, i_dep + 1):
            a, b_ = ang[i - 1], ang[i]
            n_a = math.floor((a - ray) / (2 * math.pi))
            n_b = math.floor((b_ - ray) / (2 * math.pi))
            if n_a != n_b:
                u = (a - (ray + 2 * math.pi * n_a)) / (a - b_)
                rs.append(abs(z[i - 1] + (z[i] - z[i - 1]) * u))
        ray_rows.append(np.diff(rs))
    n = min(len(r) for r in ray_rows)
    worst = 0.0
    for j in range(n):
        g = [r[j] for r in ray_rows]
        worst = max(worst, max(g) / min(g))
        if j % 4 == 0 or j == n - 1:
            print(f"   turn {j + 1:2d}: " + " / ".join(f"{x:.2f}" for x in g) + f"   {max(g) / min(g):.2f}")
    print(f"coil: worst per-turn ray ratio over {n} turns: {worst:.2f}  (mandate <= 1.5)")

    # wraps: split at every half-turn about the saddle; the spacing from each
    # half-wrap to the lap inside it (the half two earlier, or the level part
    # of the hand-off) is read off the gcode and solved for every gap_k
    wid = [t for t, k in enumerate(kinds) if k == "wrap"]
    hw = []
    for j in range(len(wid)):
        m = (sws >= sws[i_w] + j * math.pi - 1e-9) & (sws <= sws[i_w] + (j + 1) * math.pi + 1e-9) & (np.arange(len(L)) >= i_w)
        idx = np.nonzero(m)[0]
        hw.append(idx)
    # the hand-off's LEVEL part: from where it is fully on the first offset
    # level (designed angle past the coil's end, 33 pi) to the west ray
    lvl_from = kinds.count("coil") * math.pi + math.radians(tr["mapping"]["handoff_level_from_deg"])
    hand_idx = np.arange(i_dep, i_w + 1)
    hand_lvl = hand_idx[swr[hand_idx] >= lvl_from]
    A, y, dev = [], [], []
    n_u = len(wid)
    for j, idx in enumerate(hw):
        if j >= 2:
            inner = L[hw[j - 2]]
        elif j == 1:
            inner = L[hand_lvl]
        else:
            continue
        for i in idx[:: max(1, len(idx) // 60)]:
            u = (sws[i] - sws[i_w] - j * math.pi) / math.pi
            if u < 0.03 or u > 0.97:
                continue
            d = float(np.min(np.abs(inner - L[i])))
            row = np.zeros(n_u)
            if j >= 2:  # level(j,u) - level(j-2,u) = ((1-u) g_{j-2} + g_{j-1} + u g_j) / 2
                row[j - 2] += (1 - u) / 2
                row[j - 1] += 0.5
                row[j] += u / 2
            else:  # half-wrap 2 over the hand-off's level part: g_1/2 + u g_2/2 ... (0-based j-1, j)
                if d > 1.8:
                    continue
                row[j - 1] += 0.5
                row[j] += u / 2
            A.append(row)
            y.append(d)
    A, y = np.array(A), np.array(y)
    g_hat, *_ = np.linalg.lstsq(A, y, rcond=None)
    fit = A @ g_hat
    f_hat = (g_hat - G0) / K
    ferr = [abs(f_hat[j] - steps[t]["f_mean"]) for j, t in enumerate(wid)]
    g_des = np.array([steps[t]["gap_mm"] for t in wid])
    pred = A @ g_des
    print(f"wraps: {len(y)} lap-to-lap spacings read (samples on {len(hw)} half-wraps); vs designed spacing "
          f"max |err| {np.max(np.abs(y - pred)):.3f} mm, median {np.median(np.abs(y - pred)):.3f} mm")
    print(f"wrap gap_k solved from the spacings: {g_hat.min():.3f}..{g_hat.max():.3f} mm; recovered mean f vs trace: "
          f"max |err| {max(ferr):.4f}; distinct {len({round(g, 3) for g in g_hat})}/{len(wid)}")
    S_hat = g_hat[:-1] + g_hat[1:]
    S_des = g_des[:-1] + g_des[1:]
    print(f"wrap adjacent-gap sums g_k + g_k+1 (what a lap-to-lap spacing measures): max |err| "
          f"{np.max(np.abs(S_hat - S_des)):.3f} mm = {np.max(np.abs(S_hat - S_des)) / (2 * K):.3f} in mean f "
          f"(single gaps are pinned only by the hand-off, hence the looser per-letter figure)")
    ratio = y / pred
    print(f"wrap isotropy: measured / designed spacing over every direction: {ratio.min():.2f}..{ratio.max():.2f}")

    # ---------------------------------------------------------------- 3 o_t threads
    print("\n## 3. o_t: grey threads")
    grey = [s for p, s in S if p == 0]
    # assign every emitted grey dash to the designed thread path it lies on
    # (trace.json thread_path), then read each thread's drawn start, end and
    # inked fraction off the dashes alone
    births = [complex(*st["birth"]) for st in steps]
    paths = [np.array([complex(*p) for p in st["thread_path"]]) for st in steps]
    cum = [np.concatenate([[0.0], np.cumsum(np.abs(np.diff(p)))]) for p in paths]
    def proj(t, q):
        """arc position of q projected onto thread t's path (segment-exact)."""
        p, cm = paths[t], cum[t]
        i = int(np.argmin(np.abs(p - q)))
        best = (abs(p[i] - q), cm[i])
        for j in (i - 1, i):
            if 0 <= j < len(p) - 1:
                a_, b_ = p[j], p[j + 1]
                L = abs(b_ - a_)
                if L == 0:
                    continue
                u = max(0.0, min(1.0, ((q - a_) * (b_ - a_).conjugate()).real / L ** 2))
                d = abs(a_ + (b_ - a_) * u - q)
                if d < best[0]:
                    best = (d, cm[j] + u * L)
        return float(best[1])

    owned = {t: [] for t in range(T)}
    off_path = 0.0
    for dsh in grey:
        a, b = complex(*dsh[0]), complex(*dsh[-1])
        mid = complex(*dsh[len(dsh) // 2])
        dists = [float(np.min(np.abs(p - mid))) for p in paths]
        t = int(np.argmin(dists))
        off_path = max(off_path, dists[t])
        sa, sb = proj(t, a), proj(t, b)
        owned[t].append((min(sa, sb), max(sa, sb), a if sa <= sb else b, b if sa <= sb else a, plen(dsh)))
    threads = []
    redpts = L
    for t in range(T):
        ds = sorted(owned[t])
        if not ds:
            threads.append(dict(t=t, n=0, end_err=1e9, duty=0.0, start_err=1e9, half=-1))
            continue
        p0, p1 = ds[0][2], ds[-1][3]
        # inked fraction per period: dash length / distance to the next dash start
        per = [d[4] / (e[0] - d[0]) for d, e in zip(ds, ds[1:]) if e[0] > d[0]]
        inked, span = (float(np.median(per)), 1.0) if per else (0.0, 1.0)
        i_red = int(np.argmin(np.abs(redpts - p0)))
        # distance to the red POLYLINE (segments either side of the nearest sample)
        dseg = abs(redpts[i_red] - p0)
        for j in (i_red - 1, i_red):
            if 0 <= j < len(redpts) - 1:
                a_, b_ = redpts[j], redpts[j + 1]
                L = abs(b_ - a_)
                if L:
                    u = max(0.0, min(1.0, ((p0 - a_) * (b_ - a_).conjugate()).real / L ** 2))
                    dseg = min(dseg, abs(a_ + (b_ - a_) * u - p0))
        if i_red < i_w:
            half = int(swr[i_red] // math.pi)
        else:
            half = len(steps) - len(wid) + int((sws[i_red] - sws[i_w]) // math.pi)
        threads.append(dict(t=t, n=len(ds), end_err=abs(p1 - births[t]), duty=inked / span if span else 0.0,
                            start_err=float(dseg), half=half))
    print(f"dash-to-path max offset {off_path:.3f} mm (every dash sits on exactly one designed thread)")
    ok_end = sum(th["end_err"] <= 1.5 for th in threads)
    duty_err = [abs(th["duty"] - steps[th["t"]]["o_mean"]) for th in threads]
    ok_half = sum(th["half"] == th["t"] for th in threads)
    print(f"threads re-assembled: {len(threads)} ({sum(th['n'] for th in threads)} dashes of {len(grey)})")
    print(f"start on its own red stretch (half-turn / hand-off / half-wrap): {ok_half}/{T}; drawn start within 0.1 mm of the red line: "
          f"{sum(th['start_err'] < 0.1 for th in threads)}/{T} (max {max(th['start_err'] for th in threads):.3f})")
    print(f"end within 1.5 mm of its comet birth: {ok_end}/{T}  (max {max(th['end_err'] for th in threads):.2f} mm)")
    print(f"inked fraction vs mean o_t: max |err| {max(duty_err):.3f}, corr "
          f"{np.corrcoef([th['duty'] for th in threads], [s['o_mean'] for s in steps])[0, 1]:.4f}")

    # ---------------------------------------------------------------- 4 h_t roots
    print("\n## 4. h_t: comet roots")
    black = [s for p, s in S if p == 2]
    errs = []
    for t, st in enumerate(steps):
        b = births[t]
        best = min(black, key=lambda s: min(abs(complex(*s[0]) - b), abs(complex(*s[-1]) - b)))
        L = plen(best)
        errs.append(abs(L / tr["mapping"]["root_mm"] - st["h_rms"]) / st["h_rms"])
    print(f"root length / {tr['mapping']['root_mm']} mm vs RMS(h): max rel err {100 * max(errs):.2f} %  "
          f"({sum(e <= 0.05 for e in errs)}/{T} within 5 %)")
    swept = [st["comet_drawn_turn"] for st in steps]
    print(f"comets drawn to full sweep: {sum(st['comet_uncut'] for st in steps)}/{T}")

    # ---------------------------------------------------------------- 5 spacing
    print("\n## 5. spacing (samples every 0.4 mm; near-parallel = |cos| > 0.93)")
    samp = []
    for si, (pen, s) in enumerate(S):
        if pen == 3:
            continue
        for a, b in zip(s, s[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L == 0:
                continue
            n = max(1, int(L / 0.4))
            for j in range(n):
                q = j / n
                samp.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q,
                             (b[0] - a[0]) / L, (b[1] - a[1]) / L, si, pen))
    grid = {}
    for k, s in enumerate(samp):
        grid.setdefault((int(s[0] / 0.8), int(s[1] / 0.8)), []).append(k)
    bad, where = {}, {}
    for s in samp:
        ci, cj = int(s[0] / 0.8), int(s[1] / 0.8)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for k in grid.get((ci + di, cj + dj), ()):
                    o = samp[k]
                    if o[4] == s[4]:
                        continue
                    d = math.hypot(o[0] - s[0], o[1] - s[1])
                    if d < 0.8 and abs(s[2] * o[2] + s[3] * o[3]) > 0.93:
                        perp = abs((o[0] - s[0]) * s[3] - (o[1] - s[1]) * s[2])
                        if perp > 0.2:
                            key = tuple(sorted((s[5], o[5])))
                            bad[key] = bad.get(key, 0) + 1
                            where.setdefault(key, {}).setdefault((int(s[0] // 10) * 10, int(s[1] // 10) * 10), []).append(d)
    print("side-by-side near-parallel sample pairs < 0.8 mm, by pen pair:", bad or "none")
    for key, cells in where.items():
        top = sorted(cells.items(), key=lambda kv: -len(kv[1]))[:8]
        print("  ", key, "; ".join(f"({x},{y}) n={len(v)} min {min(v):.2f}" for (x, y), v in top))


if __name__ == "__main__":
    main()
