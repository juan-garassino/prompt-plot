"""A real toy latent-diffusion system — every number on the plate comes from here.

Nothing in this module draws. It builds, in plain numpy:

1. a real image distribution        64-D (an 8x8 field), 3 classes, N=1800 samples
2. a real autoencoder               E = PCA to d=6, D = its transpose.  The round
                                    trip x~ = D(E(x)) is genuinely lossy and the
                                    residual is the discarded eigenvalue mass.
3. a real forward schedule          cosine abar_t (Nichol & Dhariwal 2021),
                                    z_t = sqrt(abar) z0 + sqrt(1-abar) eps.
                                    The marginal q_t stays an exact Gaussian
                                    mixture, so its contours are closed form.
4. a real conditioning tower        tau: a ridge-regression read-out from a token
                                    bag y to class logits, c = softmax(W y / T).
                                    Fitted on a real 36-prompt corpus.
5. a real denoiser                  the ANALYTIC score of the latent mixture
                                    (this is a toy distribution, so no network is
                                    needed and none is claimed);
                                    eps_hat = -sqrt(1-abar) * grad log q_t,
                                    classifier-free guidance
                                    eps = eps_u + g (eps_c - eps_u).
6. a real sampler                   strided ancestral DDPM from fresh noise.

The one approximation, stated plainly: the class-conditional latent laws are
summarised by their empirical mean and covariance (a moment match), which makes
q_t a Gaussian mixture in closed form. Everything downstream of that is exact.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# 1. the image distribution — 8x8 fields built from smooth bumps
# ---------------------------------------------------------------------------

GRID = 8
DIM = GRID * GRID
N_SAMPLES = 1800
LATENT_DIM = 6

# The image law is a THREE-CLASS family of smooth bump fields.  One scalar
# "phase" phi opens or closes the pair of main lobes; the class sets phi's mean
# and each sample jitters it.  The ratio (class separation)/(within-class
# spread along the separating axis) is therefore a knob I set deliberately:
# at these values it is 3.8, which is what makes the conditioned latent
# landscape a WAISTED pair of wings rather than two disconnected needles.
PHI_CLASS = (0.105, -0.105, 0.0)
PHI_JITTER = 0.060
TILT_JITTER = 0.130          # the dominant WITHIN-class direction (the wings' height)
SWAP_JITTER = 0.160
_CLASS_W = (0.40, 0.35, 0.25)


def _cell_centres():
    g = (np.arange(GRID) + 0.5) / GRID
    uu, vv = np.meshgrid(g, g)
    return uu.ravel(), vv.ravel()


def _bumps_to_vector(bumps, uu, vv) -> np.ndarray:
    out = np.zeros(uu.shape[0])
    for (bu, bv, amp, wid) in bumps:
        out += amp * np.exp(-((uu - bu) ** 2 + (vv - bv) ** 2) / (2.0 * wid * wid))
    return out


def _sample_bumps(k: int, rs):
    ph = PHI_CLASS[k] + rs.normal(0.0, PHI_JITTER)
    tilt = rs.normal(0.0, TILT_JITTER)
    sw = rs.normal(0.0, SWAP_JITTER)
    if k < 2:
        return [
            (0.30 + ph, 0.62 + tilt, 1.00 * (1 + sw), 0.17 * (1 + rs.normal(0, 0.07))),
            (0.70 - ph, 0.62 - tilt, 0.95 * (1 - sw), 0.17 * (1 + rs.normal(0, 0.07))),
            (0.50 + 0.4 * ph, 0.30 + 0.6 * tilt, 0.44 * (1 + rs.normal(0, 0.12)), 0.14),
        ]
    return [
        (0.44 + 0.5 * ph, 0.44 + tilt, 1.18 * (1 + sw), 0.235 * (1 + rs.normal(0, 0.07))),
        (0.72 + 0.3 * ph, 0.76 - tilt, 0.42 * (1 + rs.normal(0, 0.12)), 0.12),
    ]


def build_dataset(seed: int = 11):
    """N x 64 images and their class labels. Real sampling, real jitter."""
    rs = np.random.RandomState(seed)
    uu, vv = _cell_centres()
    X = np.zeros((N_SAMPLES, DIM))
    y = rs.choice(3, size=N_SAMPLES, p=_CLASS_W)
    for n in range(N_SAMPLES):
        X[n] = _bumps_to_vector(_sample_bumps(int(y[n]), rs), uu, vv)
    return X, y


# ---------------------------------------------------------------------------
# 2. the autoencoder — PCA, so E and D are real matrices and D(E(x)) is a real
#    orthogonal projection with a real, reportable residual.
# ---------------------------------------------------------------------------


@dataclass
class AutoEncoder:
    mu: np.ndarray          # (64,)
    V: np.ndarray           # (64, 64) principal directions, columns
    lam: np.ndarray         # (64,) eigenvalues, descending
    d: int
    scale: float            # the latent rescale (SD's 0.18215 in spirit)

    def encode(self, X: np.ndarray) -> np.ndarray:
        return ((X - self.mu) @ self.V[:, : self.d]) * self.scale

    def decode(self, Z: np.ndarray) -> np.ndarray:
        return (Z / self.scale) @ self.V[:, : self.d].T + self.mu

    @property
    def explained(self) -> np.ndarray:
        return np.cumsum(self.lam) / np.sum(self.lam)


def fit_autoencoder(X: np.ndarray, d: int = LATENT_DIM) -> AutoEncoder:
    mu = X.mean(axis=0)
    Xc = X - mu
    # SVD of the centred data == PCA. No iteration, no randomness.
    _, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    lam = (s ** 2) / (X.shape[0] - 1)
    V = Vt.T
    if V.shape[1] < DIM:  # pad so column indexing is uniform
        V = np.concatenate([V, np.zeros((DIM, DIM - V.shape[1]))], axis=1)
        lam = np.concatenate([lam, np.zeros(DIM - lam.shape[0])])
    raw = (Xc @ V[:, :d])
    scale = 1.0 / float(raw.std())
    return AutoEncoder(mu=mu, V=V, lam=lam, d=d, scale=scale)


# ---------------------------------------------------------------------------
# 3. the schedule — cosine, exact
# ---------------------------------------------------------------------------

_S_OFF = 0.008
T_STEPS = 1000


def abar(u: float) -> float:
    """abar at normalised time u = t/T, cosine schedule, abar(0)=1 exactly."""
    u = min(1.0, max(0.0, u))
    f = math.cos(0.5 * math.pi * (u + _S_OFF) / (1.0 + _S_OFF)) ** 2
    f0 = math.cos(0.5 * math.pi * _S_OFF / (1.0 + _S_OFF)) ** 2
    return f / f0


def abar_grid(n: int = T_STEPS) -> np.ndarray:
    return np.array([abar(k / n) for k in range(n + 1)])


# ---------------------------------------------------------------------------
# 4. the latent mixture and its exact forward marginals
# ---------------------------------------------------------------------------


@dataclass
class Mixture:
    w: np.ndarray           # (K,)
    m: np.ndarray           # (K, d)
    S: np.ndarray           # (K, d, d)


def fit_latent_mixture(Z: np.ndarray, y: np.ndarray, K: int = 3) -> Mixture:
    w = np.array([(y == k).mean() for k in range(K)])
    m = np.array([Z[y == k].mean(axis=0) for k in range(K)])
    S = np.array([np.cov(Z[y == k].T) + 1e-6 * np.eye(Z.shape[1]) for k in range(K)])
    return Mixture(w=w, m=m, S=S)


def marginal(mix: Mixture, ab: float, weights: np.ndarray | None = None) -> Mixture:
    """q_t = sum_i w_i N(sqrt(abar) m_i, abar S_i + (1-abar) I) — exact."""
    d = mix.m.shape[1]
    w = mix.w if weights is None else np.asarray(weights, float)
    w = w / w.sum()
    return Mixture(
        w=w,
        m=math.sqrt(ab) * mix.m,
        S=ab * mix.S + (1.0 - ab) * np.eye(d)[None, :, :],
    )


def _log_gauss(pts: np.ndarray, mean: np.ndarray, cov: np.ndarray) -> np.ndarray:
    k = mean.shape[0]
    L = np.linalg.cholesky(cov)
    diff = pts - mean
    sol = np.linalg.solve(L, diff.T)
    quad = (sol ** 2).sum(axis=0)
    logdet = 2.0 * np.log(np.diag(L)).sum()
    return -0.5 * (quad + logdet + k * math.log(2.0 * math.pi))


def log_density(mix: Mixture, pts: np.ndarray) -> np.ndarray:
    comp = np.stack(
        [np.log(mix.w[i] + 1e-300) + _log_gauss(pts, mix.m[i], mix.S[i])
         for i in range(len(mix.w))]
    )
    mx = comp.max(axis=0)
    return mx + np.log(np.exp(comp - mx).sum(axis=0))


def score(mix: Mixture, pts: np.ndarray) -> np.ndarray:
    """grad_z log q(z) for a Gaussian mixture — exact, responsibility weighted."""
    K = len(mix.w)
    comp = np.stack(
        [np.log(mix.w[i] + 1e-300) + _log_gauss(pts, mix.m[i], mix.S[i]) for i in range(K)]
    )
    mx = comp.max(axis=0)
    r = np.exp(comp - mx)
    r /= r.sum(axis=0, keepdims=True)
    out = np.zeros_like(pts)
    for i in range(K):
        gi = -np.linalg.solve(mix.S[i], (pts - mix.m[i]).T).T
        out += r[i][:, None] * gi
    return out


def project_mixture(mix: Mixture, U: np.ndarray) -> Mixture:
    """Exact 2-D marginal of a Gaussian mixture onto the columns of U (d x 2)."""
    return Mixture(
        w=mix.w,
        m=mix.m @ U,
        S=np.stack([U.T @ mix.S[i] @ U for i in range(len(mix.w))]),
    )


# ---------------------------------------------------------------------------
# 5. conditioning tower — a real ridge read-out from a token bag
# ---------------------------------------------------------------------------

VOCAB = 16
# tokens 0-4 point at class 0, 5-9 at class 1, 10-13 at class 2, 14-15 are noise.
_TOKEN_CLASS = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, -1, -1])


def _corpus(seed: int = 5, n: int = 36) -> Tuple[np.ndarray, np.ndarray]:
    rs = np.random.RandomState(seed)
    Y = np.zeros((n, VOCAB))
    lab = np.zeros((n, 3))
    for i in range(n):
        k = i % 3
        idx = np.where(_TOKEN_CLASS == k)[0]
        for j in rs.choice(idx, size=3, replace=False):
            Y[i, j] = 1.0
        for j in rs.choice(np.where(_TOKEN_CLASS == -1)[0], size=1):
            Y[i, j] = 0.6                      # a real distractor token
        lab[i, k] = 1.0
    return Y, lab


def fit_tower(ridge: float = 0.35, seed: int = 5):
    """W (3 x 16) by closed-form ridge regression. Returns (W, train accuracy)."""
    Y, lab = _corpus(seed)
    A = Y.T @ Y + ridge * np.eye(VOCAB)
    W = np.linalg.solve(A, Y.T @ lab).T
    pred = (Y @ W.T).argmax(axis=1)
    acc = float((pred == lab.argmax(axis=1)).mean())
    return W, acc


def condition(W: np.ndarray, y: np.ndarray, temp: float = 0.32) -> np.ndarray:
    lg = (W @ y) / temp
    lg = lg - lg.max()
    e = np.exp(lg)
    return e / e.sum()


def prompt(tokens: List[int], weight: float = 1.0) -> np.ndarray:
    v = np.zeros(VOCAB)
    for t in tokens:
        v[t] = weight
    return v


# ---------------------------------------------------------------------------
# 6. denoiser + sampler
# ---------------------------------------------------------------------------


def eps_hat(mix: Mixture, z: np.ndarray, ab: float, weights: np.ndarray | None) -> np.ndarray:
    """Tweedie: eps = -sqrt(1-abar) * grad log q_t.  Analytic, no network."""
    q = marginal(mix, ab, weights)
    return -math.sqrt(max(1e-12, 1.0 - ab)) * score(q, z)


def guided_eps(mix, z, ab, c, w_uncond, g) -> np.ndarray:
    eu = eps_hat(mix, z, ab, w_uncond)
    ec = eps_hat(mix, z, ab, c)
    return eu + g * (ec - eu)


@dataclass
class Run:
    zs: np.ndarray          # (S+1, d) trajectory, index 0 is z_T
    ts: np.ndarray          # (S+1,) normalised times, 1.0 -> 0.0
    steps: np.ndarray       # (S,) per-step displacement norms


def ancestral_sample(
    mix: Mixture,
    c: np.ndarray,
    w_uncond: np.ndarray,
    g: float = 4.0,
    steps: int = 60,
    seed: int = 3,
    z_init: np.ndarray | None = None,
    noise: np.ndarray | None = None,
) -> Run:
    """Strided ancestral DDPM in the latent.  Fresh noise, real per-step update."""
    rs = np.random.RandomState(seed)
    d = mix.m.shape[1]
    idx = np.linspace(T_STEPS, 0, steps + 1).astype(int)
    z = rs.normal(size=d) if z_init is None else z_init.copy()
    zs = [z.copy()]
    disp = []
    for k in range(steps):
        t_now, t_prev = idx[k], idx[k + 1]
        ab_t = abar(t_now / T_STEPS)
        ab_p = abar(t_prev / T_STEPS)
        a_t = ab_t / max(ab_p, 1e-12)
        a_t = min(a_t, 0.999999)
        e = guided_eps(mix, z[None, :], ab_t, c, w_uncond, g)[0]
        mean = (z - (1.0 - a_t) / math.sqrt(max(1e-12, 1.0 - ab_t)) * e) / math.sqrt(a_t)
        if t_prev > 0:
            var = (1.0 - ab_p) / (1.0 - ab_t) * (1.0 - a_t)
            xi = rs.normal(size=d) if noise is None else noise[k]
            z_new = mean + math.sqrt(max(var, 0.0)) * xi
        else:
            z_new = mean
        disp.append(float(np.linalg.norm(z_new - z)))
        z = z_new
        zs.append(z.copy())
    return Run(
        zs=np.array(zs),
        ts=idx / float(T_STEPS),
        steps=np.array(disp),
    )


# ---------------------------------------------------------------------------
# 7. display basis — u is the between-class axis, v the within-class axis.
#    This is the only *choice* in the pipeline and it is a principled one:
#    it guarantees the two conditioned modes sit on a horizontal line, which is
#    what makes the guided landscape read as a waisted, two-winged mass.
# ---------------------------------------------------------------------------


def display_basis(mix: Mixture, a: int, b: int) -> np.ndarray:
    u = mix.m[a] - mix.m[b]
    u = u / np.linalg.norm(u)
    Sw = sum(mix.w[i] * mix.S[i] for i in range(len(mix.w)))
    P = np.eye(u.shape[0]) - np.outer(u, u)
    Sp = P @ Sw @ P
    ev, evec = np.linalg.eigh(Sp)
    v = evec[:, -1]
    v = v - np.dot(v, u) * u
    v = v / np.linalg.norm(v)
    return np.stack([u, v], axis=1)


# ---------------------------------------------------------------------------
# 8. the whole system, assembled once
# ---------------------------------------------------------------------------


@dataclass
class System:
    X: np.ndarray
    labels: np.ndarray
    ae: AutoEncoder
    Z: np.ndarray
    mix: Mixture
    U: np.ndarray
    W: np.ndarray
    tower_acc: float
    c_main: np.ndarray
    c_alt: np.ndarray
    y_main: np.ndarray
    y_alt: np.ndarray
    x_demo: np.ndarray
    x_recon: np.ndarray
    recon_rel: float
    z_demo: np.ndarray


def build(seed: int = 11) -> System:
    X, labels = build_dataset(seed)
    ae = fit_autoencoder(X)
    Z = ae.encode(X)
    mix = fit_latent_mixture(Z, labels)
    U = display_basis(mix, 0, 1)
    W, acc = fit_tower()
    # an AMBIGUOUS prompt: two class-0 tokens, two class-1 tokens, one distractor
    y_main = prompt([1, 3, 6, 8, 15])
    # an UNAMBIGUOUS prompt: three class-2 tokens
    y_alt = prompt([10, 11, 13])
    c_main = condition(W, y_main)
    c_alt = condition(W, y_alt)
    # the demo image: the class-0 sample whose round-trip error is the class
    # MEDIAN, so the red nests on the sheet are typical of the autoencoder and
    # not a flattering or a damning pick.
    idx0 = np.where(labels == 0)[0]
    Zc = ae.encode(X[idx0])
    Rc = ae.decode(Zc) - X[idx0]
    rel_all = np.linalg.norm(Rc, axis=1) / np.linalg.norm(X[idx0] - ae.mu, axis=1)
    i0 = int(idx0[int(np.argsort(rel_all)[len(rel_all) // 2])])
    x_demo = X[i0]
    z_demo = ae.encode(x_demo[None, :])[0]
    x_recon = ae.decode(z_demo[None, :])[0]
    rel = float(np.linalg.norm(x_demo - x_recon) / np.linalg.norm(x_demo - ae.mu))
    return System(
        X=X, labels=labels, ae=ae, Z=Z, mix=mix, U=U, W=W, tower_acc=acc,
        c_main=c_main, c_alt=c_alt, y_main=y_main, y_alt=y_alt,
        x_demo=x_demo, x_recon=x_recon, recon_rel=rel, z_demo=z_demo,
    )


# ---------------------------------------------------------------------------
# 9. field rendering — the one fixed operator that turns a 64-vector into the
#    picture we contour.  Applied identically to x and to x~, so the difference
#    between the two red nests is EXACTLY the PCA residual and nothing else.
# ---------------------------------------------------------------------------


def render_field(vec: np.ndarray, n: int = 130, sigma_cells: float = 0.95) -> np.ndarray:
    uu, vv = _cell_centres()
    g = np.linspace(0.02, 0.98, n)
    gx, gy = np.meshgrid(g, g)
    s = sigma_cells / GRID
    F = np.zeros_like(gx)
    for p in range(vec.shape[0]):
        F += vec[p] * np.exp(-((gx - uu[p]) ** 2 + (gy - vv[p]) ** 2) / (2 * s * s))
    return F


def grid_log_density(mix2: Mixture, x0, y0, x1, y1, n: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    gx, gy = np.meshgrid(xs, ys)
    pts = np.stack([gx.ravel(), gy.ravel()], axis=1)
    L = log_density(mix2, pts).reshape(n, n)
    return xs, ys, L


# ---------------------------------------------------------------------------
# 10. the report — every claim on the plate, checkable
# ---------------------------------------------------------------------------


def count_modes(mix: Mixture, ab: float, U: np.ndarray, n: int = 181,
                half: float = 5.0, weights=None):
    """Local maxima of the exact 2-D marginal on the display plane."""
    q2 = project_mixture(marginal(mix, ab, weights), U)
    xs = np.linspace(-half, half, n)
    gx, gy = np.meshgrid(xs, xs)
    L = log_density(q2, np.stack([gx.ravel(), gy.ravel()], 1)).reshape(n, n)
    inner = L[1:-1, 1:-1]
    m = ((inner > L[:-2, 1:-1]) & (inner > L[2:, 1:-1])
         & (inner > L[1:-1, :-2]) & (inner > L[1:-1, 2:]))
    idx = np.argwhere(m)
    pk = np.array([[xs[j + 1], xs[i + 1]] for i, j in idx]) if len(idx) else np.zeros((0, 2))
    return int(len(idx)), pk


def class_histogram(mix: Mixture, c: np.ndarray, g: float, n: int = 240,
                    seed: int = 77, steps: int = 40) -> np.ndarray:
    rs = np.random.RandomState(seed)
    d = mix.m.shape[1]
    counts = np.zeros(len(mix.w))
    for k in range(n):
        r = ancestral_sample(mix, c, mix.w, g=g, steps=steps, seed=seed + k,
                             z_init=rs.normal(size=d))
        z = r.zs[-1]
        counts[int(np.argmin([np.linalg.norm(z - m) for m in mix.m]))] += 1
    return counts / counts.sum()


def report() -> str:
    sysm = build()
    ae, mix = sysm.ae, sysm.mix
    out: List[str] = []
    p = out.append
    p("AUTOENCODER (PCA, closed form)")
    p(f"  pixel dim D            = {DIM}   (8x8 field)")
    p(f"  latent dim d           = {ae.d}")
    p(f"  N samples              = {N_SAMPLES}")
    p(f"  latent rescale s       = {ae.scale:.5f}   (so std(z) = 1; SD uses 0.18215)")
    ex = ae.explained
    p(f"  explained variance     g1={ex[0]:.4f} g2={ex[1]:.4f} g6={ex[5]:.4f} g12={ex[11]:.4f}")
    p(f"  discarded variance     1-g6 = {1-ex[5]:.5f}")
    p(f"  eigenvalues 1..8       {np.array2string(ae.lam[:8], precision=4)}")
    p(f"  demo x: ||x-x~||/||x-mu|| = {sysm.recon_rel:.5f}   (round trip is LOSSY)")
    p(f"  demo x: max|x-x~|      = {np.abs(sysm.x_demo-sysm.x_recon).max():.5f}"
      f"   max|x| = {np.abs(sysm.x_demo).max():.5f}")
    ZZ = ae.encode(sysm.X)
    R = ae.decode(ZZ) - sysm.X
    p(f"  dataset mean rel error = "
      f"{float(np.mean(np.linalg.norm(R,axis=1)/np.linalg.norm(sysm.X-ae.mu,axis=1))):.5f}")
    p("")
    p("SCHEDULE (cosine, Nichol & Dhariwal, s=0.008)")
    for u in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        ab = abar(u)
        p(f"  t/T={u:.2f}  abar={ab:.6f}  sqrt(abar)={math.sqrt(ab):.4f}"
          f"  sqrt(1-abar)={math.sqrt(1-ab):.4f}")
    p("")
    p("FORWARD MARGINAL ISOTROPY  (exact covariance eigenvalues of q_t)")
    for u in (0.0, 0.6, 0.8, 1.0):
        q = marginal(mix, abar(u))
        # total covariance of the mixture = E[SS] + cov of means
        mm = (q.w[:, None] * q.m).sum(axis=0)
        C = sum(q.w[i] * (q.S[i] + np.outer(q.m[i] - mm, q.m[i] - mm))
                for i in range(len(q.w)))
        ev = np.sort(np.linalg.eigvalsh(C))[::-1]
        p(f"  t/T={u:.2f}  eig(cov)= {np.array2string(ev, precision=4)}"
          f"   ratio max/min = {ev[0]/ev[-1]:.4f}")
    rs = np.random.RandomState(99)
    zT = math.sqrt(abar(1.0)) * sysm.Z[rs.choice(len(sysm.Z), 4000)] \
        + math.sqrt(1 - abar(1.0)) * rs.normal(size=(4000, ae.d))
    ev = np.sort(np.linalg.eigvalsh(np.cov(zT.T)))[::-1]
    p(f"  4000 real z_T draws: eig ratio max/min = {ev[0]/ev[-1]:.4f}  (target 1.0)")
    p("")
    p("MODE RESOLUTION — local maxima of the exact 2-D marginal q_t on the")
    p("display plane. This is the criterion the plate uses to decide when a")
    p("state stops being drawn as CONTOURS and becomes a DOT CLOUD.")
    U = sysm.U
    for u in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0):
        n, pk = count_modes(mix, abar(u), U)
        p(f"  t/T={u:.2f}  abar={abar(u):.4f}  modes = {n}   at {np.round(pk,2).tolist()}")
    p("")
    p("CONDITIONING TOWER (ridge read-out, closed form)")
    p(f"  vocab={VOCAB}  corpus=36 prompts  train accuracy = {sysm.tower_acc:.3f}")
    p(f"  y      (ambiguous) nonzero tokens {list(np.nonzero(sysm.y_main)[0])}")
    p(f"  c      = {np.array2string(sysm.c_main, precision=4)}")
    p(f"  y'     (unambiguous) nonzero tokens {list(np.nonzero(sysm.y_alt)[0])}")
    p(f"  c'     = {np.array2string(sysm.c_alt, precision=4)}")
    p("")
    p("SAMPLER — SAME NOISE, TWO CONDITIONINGS")
    rs = np.random.RandomState(1234)
    z_init = rs.normal(size=ae.d)
    nz = rs.normal(size=(60, ae.d))
    ra = ancestral_sample(mix, sysm.c_main, mix.w, g=4.0, steps=60,
                          z_init=z_init, noise=nz)
    rb = ancestral_sample(mix, sysm.c_alt, mix.w, g=4.0, steps=60,
                          z_init=z_init, noise=nz)
    za, zb = ra.zs[-1], rb.zs[-1]
    p(f"  z0 | c   = {np.array2string(za, precision=3)}")
    p(f"  z0 | c'  = {np.array2string(zb, precision=3)}")
    p(f"  ||z0|c - z0|c'||       = {np.linalg.norm(za-zb):.4f}")
    p(f"  ||z_T||  (shared start)= {np.linalg.norm(z_init):.4f}")
    p(f"  latent RMS radius      = {float(np.sqrt((sysm.Z**2).sum(1).mean())):.4f}")
    p(f"  nearest class mean of z0|c   = {int(np.argmin([np.linalg.norm(za-m) for m in mix.m]))}")
    p(f"  nearest class mean of z0|c'  = {int(np.argmin([np.linalg.norm(zb-m) for m in mix.m]))}")
    xa, xb = ae.decode(za[None])[0], ae.decode(zb[None])[0]
    p(f"  ||D(z0|c) - D(z0|c')|| / ||D(z0|c)-mu|| = "
      f"{np.linalg.norm(xa-xb)/np.linalg.norm(xa-ae.mu):.4f}  (pixel space)")
    p(f"  per-step displacement  first={ra.steps[0]:.4f} "
      f"mid={ra.steps[len(ra.steps)//2]:.4f} last={ra.steps[-1]:.4f}")
    p(f"  total path length      = {ra.steps.sum():.4f}")
    p("")
    p("GUIDANCE IS A REAL KNOB — 240 independent samples per setting, each")
    p("assigned to its nearest class mean. g=0 is the unconditional prior.")
    p(f"  prior weights w = {np.array2string(mix.w, precision=3)}"
      f"    target c = {np.array2string(sysm.c_main, precision=3)}")
    for g in (0.0, 1.0, 2.0, 4.0, 8.0):
        h = class_histogram(mix, sysm.c_main, g=g, n=240, seed=77)
        p(f"  g={g:>4.1f}  class shares = {np.array2string(h, precision=3)}")
    p("")
    p("DISPLAY BASIS (u = between-class axis, v = within-class axis)")
    m2 = project_mixture(mix, U)
    p(f"  projected class means: {np.array2string(m2.m, precision=3)}")
    p(f"  |m0 - m1| in the plane = {np.linalg.norm(m2.m[0]-m2.m[1]):.4f}")
    return "\n".join(out)


if __name__ == "__main__":
    print(report())
