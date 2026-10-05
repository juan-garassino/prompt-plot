"""Precompute the r06 RG sample cache for a seed (the piece does this itself on first render)."""
import logging, sys, time
sys.path.insert(0, __import__("os").path.dirname(__file__))
import ising_rg as R
logging.basicConfig(level=logging.INFO)
for seed in [int(a) for a in sys.argv[1:]] or [7]:
    t = time.time()
    R.sample(seed)
    print("seed", seed, "done in", round(time.time() - t, 1), "s", flush=True)
