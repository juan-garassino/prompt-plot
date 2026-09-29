"""Directions: the approach behind a render (scripts/gallery_directions.py).

The ledger fixtures below are the real ``## Rounds`` tables of studio/ising,
studio/gan, studio/convolutions and studio/millennium-riemann (notes trimmed),
so the expectations are the ones Juan reviews against. A smoke test also walks
every real ledger when studio/ is present.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gallery_directions as gd  # noqa: E402
import gallery_feedback as fb  # noqa: E402
import studio_sync  # noqa: E402

ISING = r"""# Ledger

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | CRITICAL: Tc hero + 5-plate axo deck + m(T) chart + footer | gallery/studio/ising/current/pp_ising_v6.png | — | — | uncritiqued (baseline) | Seeded the ledger via DESCRIPTION.md. No |
| r02 | r01 | COOLING STRIP: one landscape lattice, T 0.70→1.80 Tc along x. Ruled sea = held FK droplet, crimson hull = the frontier at 1.03 Tc | gallery/studio/ising/current/pp_ising_COOLING_STRIP_v9.png | 5.86 / 4 | 8 / 7 / 7 | FAIL / FAIL | Physics verified independently. Failed o |
| r03 | r01 | COASTLINE: full-bleed Tc torus, log8 ladder, dust as touches, Mandelbrot divider walk | gallery/studio/ising/current/pp_ising_COASTLINE_v8.png | 5.43 / 4 | 7 / 7 / 6 | FAIL / FAIL | Kept on disk as the COASTLINE flavour (S |
| r04 | r02 | MERGE: r02 sheet + closed dual-lattice FK hulls (cut 30, 1/2/3 passes at 30/50/155), vertical 18 mm CRITICAL spine, FK key, Onsager-m check | gallery/studio/ising/current/pp_ising_r04_iterate_v5.png | 6.71 / 6 | 8 / 7 / 7 | FAIL / FAIL | rank 2. Its bare hot edge (x 250–287) is |
| r05 | r04 | ITERATE: r04 + the hot half as heat. Hull cut lowered to 13, 13–29 as a 3rd grey pen, pass gap 0.35 mm, title/type moved off the field, 1.178 mm display pitch | gallery/studio/ising/trials/pp_ising_r05_iterate_v8.png | 6.71 / 5 | 9 / 9 / 8 | FAIL / **PASS** | **rank 1 (best).** Closed A15 A16 A17 S3 |
| r06 | r04 (nominal) | WILDCARD: THE SUNBURST. RG block-spin flow as an Art Deco half-sunburst. Angle = KW-dual T, ring = 3×3 blocking level, dash = block spin with length = correlation, crimson ξ(T) arch + Tc ray, T=0 / T=∞ cartouches | gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png | 7.00 / 6 | 7 / 7 / 8 | FAIL / FAIL | rank 2 in this pair (rank 3 overall behi |
| r07 | r05 | ITERATE: r05 + the Schotter ending by physics. T axis extended 1.80 → 2.30 Tc at the same cut 13. Black and grey keep 0.85 mm off the crimson. Field 137 → 129 rows for footer air. S9 lines added, `A` of CRITICAL rebuilt | gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png | 7.43 / 7 | 9 / 8 / 9 | FAIL / **PASS** | **rank 1 (best).** Closed A18 (strictnes |

## Mandates
| id | text |
|---|---|
| A1 | not a round |
"""

GAN = r"""# Ledger

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | Dirac-GAN saddle: the exact V = f(ψθ) as a 3D polar mesh, with the GDA run scattered over it as occupancy-thinned G/D dashes. The equilibrium is a paper hole with a crimson `+` | `gallery/studio/gan/current/pp_gan_v1.png` | — | — | unscored benchmark | Never run through the critic pair. Sourc |
| r02 | r01 | escape-spiral (Kandinsky): the run in plan view as a θ/ψ-leg staircase, with a crawl hairline, knives, the full h→0 circle, and a giant title | `gallery/studio/gan/current/pp_gan_escape-spiral_v8.png` | 6.0/4 | 4/6/6 | FAIL · rank 6 | A phase-plane figure with turn-taking vo |
| r03 | r01 | two-players-interlaced (Albers): the run as a woven tape, G = crimson weft, D = blue warp | `gallery/studio/gan/current/pp_gan_two-players-interlaced_v10.png` | 6.57/6 | 6/5/6 | FAIL · rank 5 | Centred target, float ≠ leg, orbit only  |
| r04 | r03 (+ r02's circle) | iterate: outward L-blocks of summed moves, turn squares, `+` at (78, 117), 52 mm/unit | `gallery/studio/gan/trials/pp_gan_iterate_v16.png` | 6.29/6 | 8/7/8 | FAIL · rank 4 | Tape broke into rubble (A1), and the fli |
| r05 | r04 | iterate on encoding rev 1 (Red Meander proper): the whole window is cloth, with one reed 2.8 mm. The ribbon is the chord polygon × [0.9, 1.1], its face is sign(ψθ) per crossing, with double-pass floats on a 2/2 basket ground | `gallery/studio/gan/trials/pp_gan_iterate_v24.png` | 7.14/6 | 9/8/7 | FAIL · rank 2 | A1 and A7 fixed, 0 ink-on-ink. Weaknesse |
| r06 | r04 (name only) | wildcard, De Stijl / *Broadway Boogie Woogie*: the run squared into a lane spiral, 6.5 mm cells blue / crimson / gold | `gallery/studio/gan/current/pp_gan_wildcard_v7.png` | 6.57/6 | 8/7/8 | FAIL · rank 3 · kept as the `boogie` flavour | Undermassed, over-keyed, order undocumen |
| **r07** | r05 | **iterate on rev 1 + rev 1.1**: each ribbon cell takes the face of the step that owns it (ψ_kθ_k), so the seams lean off the axes. The ribbon is shifted at the rim (full 0.2ρ from ρ_min = r0 + 1 mm), with `STEP 0` beside z_0. Re-cropped at (66, 100) @ 51.1 mm/unit with edges at mid-pitch. Title 118 mm flush left, top-right cream | `gallery/studio/gan/current/pp_gan_iterate_v34.png` | **7.57/7** | **9/8/8** | art FAIL · **sci PASS** · **rank 1 (best)** | See the r07 detail below |

## Mandates
| id | text |
|---|---|
| A1 | not a round |
"""

CONVOLUTIONS = r"""# Ledger

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | Measured reconstruction of the reference: laminar band X → 5 whorl tiles → Y, with a footnote row (bank · cone · maps) | `gallery/studio/convolutions/current/pp_convolutions_v1.png` | — | — | unscored benchmark | Measured, not guessed. Source of the Kee |
| r02 | r01 | real-kernel: same layout with everything computed | `gallery/studio/convolutions/current/pp_convolutions_real-kernel_v9.png` | 4.71/3 | 6/6/6 | FAIL · rank 6 | Flavour `real-kernel`. Not pursued |
| r03 | r01 | sliding-window: thumbprint X, a staircase corridor, and a separate output map | `gallery/studio/convolutions/current/pp_convolutions_sliding-window_v10.png` | 5.57/4 | 8/6/5 | FAIL · rank 5 | Still a triptych, and its seams regresse |
| r04 | r03 | wavefront: ONE lattice. Swept nodes show X dots with Y rings, the unswept side keeps the distance-field rings, and the LoG head sits at the fork | `gallery/studio/convolutions/trials/pp_convolutions_iterate_v9.png` | 6.14/5 | 9/8/7 | FAIL · rank 4 | Read as a heart and left a leftover quad |
| r05 | r04 | iterate (crop-field): 37×25 lattice cropped at top and right. X is a capsule-Y whose unread arm is a stripe funnel leaving through the top-right corner. The full staircase is drawn, the head is a hatched lifted card, and the collars are \|w\| gauges. Canon Pop / Ben-Day (Lichtenstein) | `gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.png` | 6.71/6 | 9/7/7 | FAIL · rank 3 (was parent of r07) | Closed A12, A17, A18 (sci), S8, A20. 63/ |
| r06 | r04 (lineage only) | wildcard (Memphis / Sottsass *Bacterio*): 97 unit impulses as black confetti under three kernel cards (K1 gabor 30° disc, K2 gabor 120° triangle, K3 blur card). Each card shows the level 0.35 of K∗ΣX, and the solid marks > 1.25, which only a sum can reach | `gallery/studio/convolutions/trials/pp_convolutions_wildcard_v22.png` | 6.86/6 | 9/7/7 | FAIL · rank 2, not continued | Exact to 0.003. **REGRESSED S1:** the ne |
| r07 | r05 | iterate (one-X): encoding v1 applied to r05. X becomes ONE 2-pass x = 0 keyline (583 mm, ends only on the crop). Wing stripes go to Δd = 2.1 mm (10.96 → 5.18 m). Outer rings are doubled for \|bin\| ≥ 3. Dots are nib-corrected (ink area ∝ x). The last riser stops at y 24.2. Title and key sit on lattice rows. The key names every mark | `gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png` | 7.29/7 | 9/9/8 | art FAIL · sci **PASS** · **rank 1 → vote** | Closed A18, A21, A22, A23, A24, S5, S10  |

## Mandates
| id | text |
|---|---|
| A1 | not a round |
"""

MILLENNIUM_RIEMANN = r"""# Ledger

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | faithful [F]: the reference's centred architecture, corrected. X-ray mirrored top–bottom at 3.0 mm/u, σ = ½ at x = 148.5, real axis at y = 210, 20 red crosses at ±γ₁…γ₁₀, two red register ticks, ψ₁₀₀(x)−x prime footer, type in the right void between ζ's rulings | `gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5_truewidth.png` (+ `_v5.png`, `_v5.gcode`) | 7.43/6 | 8/8/7 | FAIL · rank 2 | The geometry is exact (zero sets ≤ 0.027 |
| r02 | — | abstract [A]: the LeWitt instruction drawing, flat on purpose. Upper half-plane only at 3.45 mm/u, σ = ½ at x = 180 (undrawn), real axis y = 32, t ≤ 97.35, 28 red crosses, ζ's own rulings t = kπ/ln 2 on the right carrying the wall label at x = 206 | `gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6_phys.png` (+ `_v6.png`, `_v6.gcode`) | 8.0/7 | 9/9/8 | **PASS/PASS · rank 1 → parent** | All §11 checks pass on both critics' mea |
| r03 | r02 | iterate [A] polish: r02's field byte-identical. Red drawn ONE one-way pass per arm (56 strokes, 0.21 m). Key restricted "ABOVE THE REAL LINE". `−4 −2 1` under the true feet. Label blocks centred on the measured rulings. Statement solved to end on x = 180. r01's series caption on x = 206 at the title's cap line | `gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2_phys.png` (+ `_v2.png`, `_v2.gcode`) | 8.43/8 | 9/9/9 | **PASS/PASS · best → vote** | All five r02 mandates were confirmed FIX |

## Mandates
| id | text |
|---|---|
| A1 | not a round |
"""

LEDGERS = {"ising": ISING, "gan": GAN, "convolutions": CONVOLUTIONS,
           "millennium-riemann": MILLENNIUM_RIEMANN}


@pytest.fixture
def studio(tmp_path, monkeypatch):
    """A tmp studio/ holding the four real ledgers, every module repointed at it."""
    st, gal = tmp_path / "studio", tmp_path / "gallery"
    for slug, text in LEDGERS.items():
        (st / slug / "rounds").mkdir(parents=True)
        (st / slug / "LEDGER.md").write_text(text)
    gal.mkdir()
    monkeypatch.setattr(fb, "STUDIO", st)
    monkeypatch.setattr(fb, "GALLERY", gal)
    monkeypatch.setattr(fb, "LOG", st / "feedback.jsonl")
    monkeypatch.setattr(gd, "STUDIO", st)
    monkeypatch.setattr(gd, "GALLERY", gal)
    monkeypatch.setattr(studio_sync, "STUDIO", st)
    monkeypatch.setattr(studio_sync, "GALLERY", gal)
    monkeypatch.setattr(studio_sync, "DEST", gal / "studio")
    return st


def _handoff(st: Path, slug: str, rnd: str, text: str) -> None:
    d = st / slug / "rounds" / rnd
    d.mkdir(parents=True, exist_ok=True)
    (d / "HANDOFF.md").write_text(text)


def _shape(dirs: dict) -> dict:
    return {k: (d["label"], d["rounds"]) for k, d in dirs.items()}


# ---------------------------------------------------------------------------
# parsers
# ---------------------------------------------------------------------------

def test_parse_ledger_rows():
    rows = gd.parse_ledger(ISING)
    assert [r["round"] for r in rows] == [f"r0{i}" for i in range(1, 8)]
    r6 = rows[5]
    assert r6["parent"] == "r04"                       # "r04 (nominal)"
    assert r6["render"] == "pp_ising_r06_wildcard_v11.png"
    assert r6["thesis"].startswith("WILDCARD: THE SUNBURST")
    assert r6["canon"] == ""                           # no canon column
    assert r6["art"] == "7.00 / 6" and r6["sci"] == "7 / 7 / 8"
    assert rows[0]["parent"] is None                   # "—"
    assert all(r["note"] for r in rows)                # the mandates table is not read


def test_parse_ledger_bold_round_escaped_pipes_and_parent_text():
    gan = gd.parse_ledger(GAN)
    assert gan[-1]["round"] == "r07" and gan[-1]["parent"] == "r05"   # **r07**
    assert gan[3]["parent"] == "r03"                                  # "r03 (+ r02's circle)"
    conv = gd.parse_ledger(CONVOLUTIONS)
    r5 = conv[4]
    assert "|w|" in r5["thesis"]                       # \| inside a cell is not a column break
    assert r5["render"] == "pp_convolutions_iterate_v20.png"
    riem = gd.parse_ledger(MILLENNIUM_RIEMANN)
    assert riem[0]["render"] == "pp_millennium_riemann_faithful_v5_truewidth.png"


def test_parse_ledger_canon_column_and_padding():
    text = ("## Rounds\n| round | parent | thesis | canon | render | art avg/min | sci | verdict | note |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| 4 | r2 | iterate | Art Deco | `x/pp_a_v1.png` | 7/6 | 8/8/8 | PASS | n |\n")
    (row,) = gd.parse_ledger(text)
    assert row["round"] == "r04" and row["parent"] == "r02" and row["canon"] == "Art Deco"
    assert gd.parse_ledger("# nothing here\n") == []


def test_parse_handoff():
    h = gd.parse_handoff("# r06\n- **render**: gallery/a/pp_x_v1.png\nseeds: a · b\n"
                         "canon: art_deco (STYLES.md §2)\n* order: radial\n**lineage:** Van Alen\n")
    assert h["render"] == "gallery/a/pp_x_v1.png"
    assert h["seeds"] == "a · b"
    assert h["canon"] == "art_deco (STYLES.md §2)"
    assert h["order"] == "radial"
    assert h["lineage"] == "Van Alen"
    assert h["thesis"] == "" and h["direction"] == ""


def test_canon_norm():
    assert gd.canon_norm("art_deco (STYLES.md §2)") == "deco"
    assert gd.canon_norm("science_poster") == "science-poster"
    assert gd.canon_norm("De Stijl / Broadway Boogie Woogie") == "de-stijl"
    assert gd.canon_norm("Pop / Ben-Day (Lichtenstein)") == "pop"
    assert gd.canon_norm("Memphis / Sottsass") == "memphis"
    assert gd.canon_norm("radial_viz") == "radial"
    assert gd.canon_norm("population") == ""
    assert gd.canon_norm("") == ""


# ---------------------------------------------------------------------------
# directions on the real ledgers
# ---------------------------------------------------------------------------

def test_ising_directions(studio):
    d = gd.directions("studio/ising")
    assert _shape(d) == {
        "original": ("CRITICAL", ["r01"]),
        "r02": ("COOLING STRIP", ["r02", "r04", "r05", "r07"]),   # MERGE + 2 ITERATEs
        "r03": ("COASTLINE", ["r03"]),
        "r06": ("THE SUNBURST", ["r06"]),                         # wildcard: own root
    }
    assert d["r06"]["parent_of_root"] == "r04"
    assert d["r02"]["best"]["round"] == "r07"
    assert d["r02"]["best"]["art_min"] == 7 and d["r02"]["best"]["sci"] == 8
    assert d["r02"]["slug"] == "cooling-strip" and d["r02"]["root"] == "r02"


def test_gan_directions(studio):
    d = gd.directions("studio/gan")
    assert _shape(d) == {
        "original": ("Dirac-GAN saddle", ["r01"]),
        "r02": ("escape-spiral", ["r02"]),
        "r03": ("two-players-interlaced", ["r03", "r04", "r05", "r07"]),
        "r06": ("De Stijl / Broadway Boogie Woogie", ["r06"]),
    }
    assert d["r03"]["best"]["round"] == "r07"


def test_convolutions_directions(studio):
    d = gd.directions("studio/convolutions")
    assert {k: v["rounds"] for k, v in d.items()} == {
        "original": ["r01"], "r02": ["r02"], "r03": ["r03"],
        "r04": ["r04", "r05", "r07"],          # "wavefront" is its own root, not sliding-window
        "r06": ["r06"],
    }
    assert d["r04"]["label"] == "wavefront"
    assert d["r02"]["label"] == "real-kernel" and d["r03"]["label"] == "sliding-window"
    assert d["r06"]["label"] == "Memphis / Sottsass Bacterio"


def test_millennium_riemann_directions(studio):
    d = gd.directions("studio/millennium_riemann")      # the gallery family resolves to the slug
    assert _shape(d) == {"r01": ("faithful", ["r01"]),    # variant 'faithful': not the original
                         "r02": ("abstract", ["r02", "r03"])}
    assert d["r02"]["best"]["round"] == "r03"


def test_no_ledger_is_empty(studio):
    assert gd.directions("studio/nothing-here") == {}
    assert gd.direction_of("studio/nothing-here", "pp_nothing_here_v1.png") == "original"
    assert gd.direction_of("studio/nothing-here", "pp_nothing_here_idea_v2.png") == "x-idea"


def test_canon_order_lineage_from_handoff(studio):
    _handoff(studio, "ising", "r04", "render: x\ncanon: science_poster\nlineage: Nees, Schotter\n")
    _handoff(studio, "ising", "r06", "canon: art_deco (STYLES.md §2)\n"
                                     "order: radial + nested (stepped sunburst)\n")
    d = gd.directions("studio/ising")
    assert d["r02"]["canon"] == "science_poster" and d["r02"]["canon_norm"] == "science-poster"
    assert d["r02"]["lineage"] == "Nees, Schotter"      # first round in the chain that has it
    assert d["r06"]["canon_norm"] == "deco" and d["r06"]["order"].startswith("radial")
    assert d["r03"]["canon"] == ""


# ---------------------------------------------------------------------------
# direction_of: resolution order
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("subject,name,key", [
    ("studio/ising", "pp_ising_v6.png", "original"),                  # ledger render
    ("studio/ising", "pp_ising_v5_s13.png", "original"),              # empty variant
    ("studio/ising", "pp_ising_COOLING_STRIP_v6_s3.png", "r02"),      # variant
    ("studio/ising", "pp_ising_COASTLINE_v2.gcode", "r03"),
    ("studio/ising", "pp_ising_r04_iterate_v4_s13.png", "r02"),       # rNN token
    ("studio/ising", "pp_ising_r07_iterate_v3.png", "r02"),
    ("studio/ising", "pp_ising_r06_wildcard_v10_s3.png", "r06"),
    ("studio/ising", "pp_ising_iterate_v2.png", "r02"),               # 'iterate' only in r02's chain
    ("studio/ising", "pp_ising_brand_new_v1.png", "x-brand-new"),
    ("studio/gan", "pp_gan_iterate_v16.png", "r03"),
    ("studio/gan", "pp_gan_iterate_v3.png", "r03"),
    ("studio/gan", "pp_gan_wildcard_v2.png", "r06"),
    ("studio/gan", "pp_gan_escape-spiral_v2.png", "r02"),
    ("studio/gan", "pp_gan_v1.png", "original"),
    ("studio/convolutions", "pp_convolutions_iterate_v3.png", "r04"),
    ("studio/convolutions", "pp_convolutions_wildcard_v5.png", "r06"),
    ("studio/convolutions", "pp_convolutions_sliding-window_v4.png", "r03"),
    ("studio/millennium_riemann", "pp_millennium_riemann_faithful_v3.png", "r01"),
    ("studio/millennium_riemann", "pp_millennium_riemann_iterate_v1_phys.png", "r02"),
    ("studio/millennium_riemann", "pp_millennium_riemann_abstract_v2.gcode", "r02"),
])
def test_direction_of(studio, subject, name, key):
    assert gd.direction_of(subject, name) == key


def test_variant_matching_several_roots_is_flagged(studio):
    text = ("## Rounds\n| round | parent | thesis | render | art | sci | verdict | note |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| r01 | — | first | `pp_p_v1.png` | — | — | — | — |\n"
            "| r02 | r01 | alpha: one | `pp_p_look_v2.png` | — | — | — | — |\n"
            "| r03 | r01 | beta: two | `pp_p_look_v5.png` | — | — | — | — |\n")
    (studio / "p").mkdir()
    (studio / "p" / "LEDGER.md").write_text(text)
    key, how, ambiguous = gd._resolve("studio/p", "pp_p_look_v3.png")
    assert (key, how, ambiguous) == ("r03", "variant", True)   # the latest matching row


def test_handoff_seeds_and_direction_override(studio):
    _handoff(studio, "ising", "r03", "seeds: gallery/studio/ising/trials/pp_ising_odd_v1.png · x\n")
    assert gd.direction_of("studio/ising", "pp_ising_odd_v1.png") == "r03"
    _handoff(studio, "ising", "r05", "direction: r03\n")
    d = gd.directions("studio/ising")
    assert d["r03"]["rounds"] == ["r03", "r05", "r07"]         # r07 follows its parent
    assert d["r02"]["rounds"] == ["r02", "r04"]
    assert gd.direction_of("studio/ising", "pp_ising_r05_iterate_v8.png") == "r03"
    _handoff(studio, "ising", "r04", "direction: x-side-quest\n")
    assert gd.direction_of("studio/ising", "pp_ising_r04_iterate_v2.png") == "x-side-quest"


def test_cycles_terminate(studio):
    text = ("## Rounds\n| round | parent | thesis | render | art | sci | verdict | note |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| r01 | r02 | iterate | — | — | — | — | — |\n"
            "| r02 | r01 | iterate | — | — | — | — | — |\n"
            "| r03 | r03 | — | — | — | — | — | — |\n")
    (studio / "loop").mkdir()
    (studio / "loop" / "LEDGER.md").write_text(text)
    d = gd.directions("studio/loop")
    assert sorted(r for v in d.values() for r in v["rounds"]) == ["r01", "r02", "r03"]
    assert d["r03"]["label"] == "(untitled r03)"


def test_audit_runs(studio):
    out = gd.audit(["ising"])
    assert "=== ising" in out and "THE SUNBURST" in out and "=== gan" not in out


def test_real_studio_smoke():
    real = REPO / "studio"
    if not real.is_dir() or not list(real.glob("*/LEDGER.md")):
        pytest.skip("no studio ledgers on disk")
    for led in sorted(real.glob("*/LEDGER.md")):
        ctx = gd._context(led.parent.name)
        rows = ctx["rows"]
        for r in rows:
            key = ctx["round_key"].get(r["round"])
            assert key in ctx["dirs"], (led.parent.name, r["round"])
            assert gd.KEY_RE.fullmatch(key)
        assert sorted(x for d in ctx["dirs"].values() for x in d["rounds"]) == \
            sorted(r["round"] for r in rows)
