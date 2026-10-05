"""Recompute the millennium-bsd §7 check numbers (pure numpy + fractions; ~15 s).

    .venv/bin/python studio/millennium-bsd/data/verify_bsd.py [--edsac]

--edsac also runs the Birch–Swinnerton-Dyer product to X=10^4 (~20 s more).
"""
from __future__ import annotations
import math, sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from lfun_lib import Lfun, ap_dict  # noqa: E402

def add(P, Q):  # group law on y^2 + y = x^3 - x (a1=a2=a6=0, a3=1, a4=-1)
    if P is None: return Q
    if Q is None: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 + y2 + 1 == 0: return None
    lam = (3 * x1 * x1 - 1) / (2 * y1 + 1) if x1 == x2 else (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    return (x3, -(lam * x3 + y1 - lam * x1) - 1)

on = lambda x, y: y * y + y == x ** 3 - x
print("reference points on E? (1,1):", on(1, 1), " (1,-2):", on(1, -2), " (-1,0):", on(-1, 0))
P = (F(0), F(0)); Q = None
for n in range(1, 9):
    Q = add(Q, P); print(f"{n}P = ({Q[0]}, {Q[1]})  {'egg' if Q[0] < 0.2696 else 'branch'}")
Q = None
for n in range(1, 101): Q = add(Q, P)
print("digits of denominator of x(100P):", len(str(Q[0].denominator)))
E = Lfun("37a1")
print("L(E,1) =", round(E.L(1.0, -1), 12), "  L(E,0.5) =", round(E.L(0.5, -1), 6),
      "  L(E,1.5) =", round(E.L(1.5, -1), 6), "  L(E,2) =", round(E.L(2.0, -1), 6))
print("Lambda(1.5), Lambda(0.5) =", round(E.Lam(1.5, -1), 6), round(E.Lam(0.5, -1), 6))
from lfun_lib import upper_gamma
Lp = 2 * (E.A / E.n * upper_gamma(0.0, E.x)).sum()
print("L'(E,1) =", Lp, "  Omega*Reg =", 5.986917292463918 * 0.0511114082399688,
      "  crossing angle deg =", math.degrees(math.atan(Lp)))
if "--edsac" in sys.argv:
    ap = ap_dict([0, 0, 1, -1, 0], 10000); pr = 1.0
    for p in sorted(ap):
        if p != 37: pr *= (p + 1 - ap[p]) / p
    print("prod_{p<=1e4} N_p/p =", round(pr, 4), " /log X =", round(pr / math.log(1e4), 4))
