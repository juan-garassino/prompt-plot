"""Benchmark stroke ordering on random short strokes (CPU, pure Python).

    python -m evals.bench_ordering            # 2000 and 10000 strokes

Compares ``postprocess.optimize_stroke_order`` with the previous algorithm
(full-scan nearest neighbour over stroke starts, no reversal), reproduced here
as ``_legacy_nn`` for reference.
"""

import random
import sys
import time

from promptplot import postprocess as pp
from promptplot.models import GCodeCommand as C


def _strokes(n, seed=1):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(10, 200), rnd.uniform(10, 280)
        out.append(
            [
                C(command="G0", x=x, y=y),
                C(command="M3", s=1000),
                C(command="G1", x=x + rnd.uniform(-5, 5), y=y + rnd.uniform(-5, 5)),
                C(command="M5"),
            ]
        )
    return out


def _legacy_nn(strokes):
    remaining, pos, order = list(range(len(strokes))), (0.0, 0.0), []
    starts = [pp._stroke_start(s) for s in strokes]
    ends = [pp._stroke_end(s) for s in strokes]
    while remaining:
        best = min(remaining, key=lambda i: pp._distance(pos, starts[i]))
        remaining.remove(best)
        order.append(strokes[best])
        pos = ends[best]
    return order


def main(sizes=(2000, 10000)):
    print("strokes | input travel mm | legacy NN mm (s) | current mm (s)")
    for n in sizes:
        s = _strokes(n)
        t = time.time()
        legacy = _legacy_nn(s)
        t_legacy = time.time() - t
        t = time.time()
        cur = pp.optimize_stroke_order(s)
        t_cur = time.time() - t
        print(
            f"{n} | {pp._order_travel(s):.0f} | {pp._order_travel(legacy):.0f} ({t_legacy:.2f})"
            f" | {pp._order_travel(cur):.0f} ({t_cur:.2f})"
        )


if __name__ == "__main__":
    main(tuple(int(a) for a in sys.argv[1:]) or (2000, 10000))
