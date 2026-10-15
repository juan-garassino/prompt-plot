"""Gate on the offline eval harness (evals/): no case may lose or add ink,
break pen safety or leak a pen-down into another colour layer."""

from evals.run_evals import run_all, summarize


def test_eval_harness_safety_and_fidelity():
    rows = run_all()
    errors = [r for r in rows if "error" in r]
    assert not errors, errors
    s = summarize(rows)
    assert s["safety_violations"] == 0
    assert s["missing_mm"] == 0
    assert s["spurious_mm"] == 0
    assert s["layer_leaks"] == 0
    assert s["mixed_layers"] == 0
    assert s["extra_color_switches"] == 0


def test_optimizer_does_not_increase_travel_on_single_colour_generators():
    """Stroke ordering keeps the input order when it cannot do better, so on
    single-colour cases the only extra travel allowed is the final return home."""
    for r in run_all():
        if r["case"] in ("gen_maze", "gen_flow_field"):
            assert r["travel"] <= r["travel_in"] + 400, r  # 400 mm > A4 diagonal home trip
