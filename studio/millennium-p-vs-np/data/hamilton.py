"""Rank-2/3 data (dossier §2b, §2c): exhaustive simple-path search trees from vertex 0.

Dodecahedron (Hamilton's Icosian game, 1856) via LCF [10,7,4,-4,-7,10,-4,7,-7,4]^2;
Petersen graph (outer 5-cycle, inner pentagram, 5 spokes). The tree of all simple paths
from a start vertex is independent of neighbour order and (both graphs are
vertex-transitive) of the start vertex, so its counts are labelling-free.

    .venv/bin/python studio/millennium-p-vs-np/data/hamilton.py
"""
from __future__ import annotations

import collections


def lcf(n, pat, rep):
    adj = {i: set() for i in range(n)}
    for i in range(n):
        adj[i].add((i + 1) % n)
        adj[(i + 1) % n].add(i)
    p = pat * rep
    for i in range(n):
        j = (i + p[i]) % n
        adj[i].add(j)
        adj[j].add(i)
    return {k: sorted(v) for k, v in adj.items()}


def petersen():
    adj = {i: set() for i in range(10)}
    for i in range(5):
        for a, b in [(i, (i + 1) % 5), (5 + i, 5 + (i + 2) % 5), (i, 5 + i)]:
            adj[a].add(b)
            adj[b].add(a)
    return {k: sorted(v) for k, v in adj.items()}


def tree(adj, start=0):
    n = len(adj)
    per = collections.Counter()
    dead = full = cyc = 0
    path, seen = [start], {start}

    def rec():
        nonlocal dead, full, cyc
        per[len(path) - 1] += 1
        if len(path) == n:
            full += 1
            cyc += start in adj[path[-1]]
            return
        kids = [w for w in adj[path[-1]] if w not in seen]
        dead += not kids
        for w in kids:
            seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)

    rec()
    return sum(per.values()), dead, full, cyc, [per[d] for d in range(n)]


for name, g in [("dodecahedron", lcf(20, [10, 7, 4, -4, -7, 10, -4, 7, -7, 4], 2)),
                ("petersen", petersen())]:
    nodes, dead, full, cyc, per = tree(g)
    print(f"{name}: V={len(g)} E={sum(map(len, g.values()))//2} tree nodes={nodes} "
          f"dead ends={dead} hamiltonian paths={full} closing to a cycle={cyc}")
    print("  nodes/depth", per)
