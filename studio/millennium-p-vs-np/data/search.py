"""Exact data for the P vs NP plate (dossier §3, §7). Stdlib only, deterministic.

Instance: SATLIB uf20-03.cnf (uniform random 3-SAT, 20 vars, 91 clauses; set uf20-91,
https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/RND3SAT/uf20-91.tar.gz), sha256 of the file:
23bbf1dba20738f0b09cd18199d261e0cdf23e904e808264c7d61a16d3234f62.

Algorithm (the ONE search the plate draws): chronological backtracking, variables x1..x20 in
index order, value False before True; a node is a conflict leaf the moment some clause whose
variables are all assigned is falsified. Node = generated partial assignment (root counted).

Layout convention (measure layout): node p = (b1..bd) owns the angular interval
[k/2^d, (k+1)/2^d) of one turn, k = int(b1..bd as binary, x1 = most significant, True = 1).
Its subcube holds exactly 2^(20-d) of the 2^20 assignments. With False-first, DFS preorder
== increasing start angle (ties: shallower first), so search TIME runs clockwise as ANGLE.

    .venv/bin/python studio/millennium-p-vs-np/data/search.py            # summary
    .venv/bin/python studio/millennium-p-vs-np/data/search.py --json out.json   # full tree
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CNF = HERE / "uf20-03.cnf"
N = 20


def load(path: Path) -> list[list[int]]:
    clauses = []
    for line in path.read_text().splitlines():
        s = line.split()
        if not s or s[0] in ("c", "p"):
            continue
        if s[0] == "%":
            break
        lits = [int(x) for x in s if x != "0"]
        if lits:
            clauses.append(lits)
    return clauses


def build(clauses):
    by_max = collections.defaultdict(list)
    for c in clauses:
        by_max[max(abs(l) for l in c)].append(c)

    def conflict(p):  # clause whose max var == len(p) now fully false
        return any(all(p[abs(l) - 1] != (l > 0) for l in c) for c in by_max[len(p)])

    nodes = []  # preorder: (bits tuple, is_conflict)
    stack = [()]
    while stack:
        p = stack.pop()
        bad = bool(p) and conflict(p)
        nodes.append((p, bad))
        if bad or len(p) == N:
            continue
        stack.append(p + (True,))
        stack.append(p + (False,))  # False popped first -> False-first DFS
    return nodes


def dpll(clauses):
    """DPLL with unit propagation; same order (smallest free var, False first). Counts nodes."""
    st = collections.Counter()

    def up(A):
        A = dict(A)
        while True:
            unit = None
            for c in clauses:
                vals = [A.get(abs(l)) for l in c]
                if any(v is not None and v == (l > 0) for v, l in zip(vals, c)):
                    continue
                free = [l for v, l in zip(vals, c) if v is None]
                if not free:
                    return None
                if len(free) == 1:
                    unit = free[0]
                    break
            if unit is None:
                return A
            A[abs(unit)] = unit > 0
            st["implied"] += 1

    def rec(A):
        st["nodes"] += 1
        A = up(A)
        if A is None:
            st["conflicts"] += 1
            return
        if len(A) == N:
            st["models"] += 1
            st.setdefault("first", st["nodes"])
            return
        v = min(x for x in range(1, N + 1) if x not in A)
        for b in (False, True):
            rec({**A, v: b})

    rec({})
    return dict(st)


def k_of(p):
    return int("".join("1" if b else "0" for b in p), 2) if p else 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    a = ap.parse_args()
    cl = load(CNF)
    print("sha256", hashlib.sha256(CNF.read_bytes()).hexdigest())
    print("clauses", len(cl), "vars", N, "ratio", len(cl) / N)
    nodes = build(cl)
    gen = collections.Counter(len(p) for p, _ in nodes)
    con = collections.Counter(len(p) for p, b in nodes if b)
    sols = [p for p, b in nodes if len(p) == N and not b]
    print("tree nodes", len(nodes), "conflict leaves", sum(con.values()), "models", len(sols))
    print("generated/depth", [gen[d] for d in range(N + 1)])
    print("conflicts/depth", [con[d] for d in range(N + 1)])
    print("live/depth     ", [gen[d] - con[d] for d in range(N + 1)])
    s = sols[0]
    k = k_of(s)
    print("model bits x1..x20", "".join("1" if b else "0" for b in s), "k", k)
    print("model DIMACS", " ".join(str(i + 1 if b else -(i + 1)) for i, b in enumerate(s)))
    print("model angle deg", k / 2**N * 360)
    pre = [p for p, _ in nodes].index(s) + 1
    print("found at preorder node", pre, "of", len(nodes), f"({pre / len(nodes):.4f})")
    mass = sum(con[d] * 2 ** (N - d) for d in con)
    print("refuted assignment mass", mass, "+ model =", mass + 1, "== 2^20", 2**N)
    # certificate path: node-centre angle at each depth
    print("red path centre angles (deg) d=0..20:")
    print([round((k_of(s[:d]) + 0.5) / 2**d * 360, 4) if d else None for d in range(N + 1)])
    tl = [sum(1 for l in c if s[abs(l) - 1] == (l > 0)) for c in cl]
    print("verify: clauses", len(cl), "literal lookups", sum(map(len, cl)),
          "true-literal histogram", dict(sorted(collections.Counter(tl).items())))
    # check order for the verification line: first true literal of each clause
    print("verify: per clause (#true literals) in file order", tl)
    print("DPLL (unit propagation) same instance:", dpll(cl))
    if a.json:
        out = [{"bits": "".join("1" if b else "0" for b in p), "depth": len(p), "k": k_of(p),
                "conflict": bad} for p, bad in nodes]
        Path(a.json).write_text(json.dumps({"nodes_preorder": out, "model": k}, indent=0))
        print("wrote", a.json)


if __name__ == "__main__":
    main()
