"""Lock the shared stroke font's contract.

This file exists because the font has twice been silently reverted by agents
running `git checkout` / `git stash` on the package while it held uncommitted
work — five glyphs the first time, the per-case side bearings the second. A
revert now fails the suite loudly instead of quietly shrinking the alphabet.
"""

from __future__ import annotations

from promptplot.generative.generators import _GLYPHS, _glyph_advance, _stroke_text, _text_width


def test_alphabet_is_complete():
    for ch in "abcdefghijklmnopqrstuvwxyz":
        assert ch in _GLYPHS, f"lowercase {ch!r} missing"
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        assert ch in _GLYPHS, f"{ch!r} missing"


def test_symbols_present():
    for ch in ":/=+(),'%*-.^_|×·∂σε θ⊙∗".replace(" ", ""):
        assert ch in _GLYPHS, f"symbol {ch!r} ({hex(ord(ch))}) missing"


def test_math_and_brackets_present():
    """The ML plates set real formulae; a dropped glyph silently mangles them."""
    for ch in "ΣΠ[]{}−→←↑↓≤≥≠√∞∫":
        assert ch in _GLYPHS, f"math glyph {ch!r} ({hex(ord(ch))}) missing"


def test_every_glyph_is_drawable():
    """Each entry is a list of polylines of >=2 (x, y) points — a malformed
    entry raises deep inside a render instead of here."""
    for ch, strokes in _GLYPHS.items():
        assert isinstance(strokes, list), f"{ch!r} is not a list of strokes"
        for k, stroke in enumerate(strokes):
            assert len(stroke) >= 2, f"{ch!r} stroke {k} has < 2 points"
            for pt in stroke:
                assert len(pt) == 2, f"{ch!r} stroke {k} has a non-(x, y) point"
                assert all(isinstance(v, (int, float)) for v in pt), f"{ch!r} non-numeric"


def test_case_is_preserved():
    """`softmax` must not render as `SOFTMAX` — four plates were wrong this way."""
    assert _stroke_text("s", 0, 0, 6) != _stroke_text("S", 0, 0, 6)


def test_per_case_side_bearings():
    """Lowercase needs a tighter bearing than caps; measured 1.02 / 0.55."""
    assert _glyph_advance("o") < _glyph_advance("O")


def test_advance_cache_respects_bearing():
    """The cache must key on the bearing, not just the character."""
    a = _glyph_advance("m", 1.02, 0.55)
    b = _glyph_advance("m", 1.02, 2.0)
    assert a != b, "a tuned bearing leaked from the cache"
    assert _glyph_advance("m", 1.02, 0.55) == a, "default poisoned by a tuned call"


def test_proportional_is_opt_in():
    """Default metrics stay monospaced so existing compositions do not shift."""
    assert _text_width("illinois", 6) == len("illinois") * 5.6
    assert _text_width("illinois", 6, proportional=True) < _text_width("illinois", 6)


def test_combining_marks_do_not_advance():
    assert _glyph_advance("̃") == 0.0
