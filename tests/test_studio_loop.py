"""Studio design loop: stub-provider round-trip (no keys, no network).

House stub style (no Mock/MagicMock): a fake provider with a scripted reply
queue, recording calls on self.calls.
"""

import json

import pytest

from promptplot.studio.loop import run_design_loop


class _StubProvider:
    provider_name = "stub"

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    async def acomplete(self, prompt):
        self.calls.append(("text", prompt[:80]))
        return self.replies.pop(0)

    async def acomplete_multimodal(self, prompt, image_paths=None):
        self.calls.append(("vision", [str(p) for p in (image_paths or [])]))
        return self.replies.pop(0)


DESIGN = json.dumps(
    {
        "concept": "truchet as a calm field",
        "payload": {"panels": [{"generator": "truchet", "seed": 8, "params": {}}], "title": "T"},
    }
)
CRITIQUE = json.dumps(
    {
        "scores": {
            "hierarchy": 8, "grid_alignment": 9, "tension_asymmetry": 8,
            "negative_space": 8, "pen_craft": 9, "concept_legibility": 8,
            "depth_dimensionality": 8,
        },
        "verdict": "pass",
        "top_fixes": [],
        "one_line": "clean",
    }
)
SYNTH = json.dumps({"done": True, "instruction": ""})


async def test_params_mode_one_round(tmp_path):
    provider = _StubProvider([DESIGN, CRITIQUE, SYNTH])
    res = await run_design_loop(
        "cnn", provider, mode="params", rounds=3, out_dir=tmp_path / "cnn"
    )
    assert len(res.rounds) == 1  # passed + done on round 1
    r = res.rounds[0]
    assert r.verdict == "pass"
    assert r.render_path is not None and r.render_path.exists()
    assert (tmp_path / "cnn" / "rounds" / "r01" / "payload.json").exists()
    assert (tmp_path / "cnn" / "rounds" / "r01" / "critique.json").exists()
    assert (tmp_path / "cnn" / "final" / "PROPOSAL.md").exists()
    # vision critic got the render
    kinds = [k for k, _ in provider.calls]
    assert kinds == ["text", "vision", "text"]


async def test_bad_designer_json_recovers(tmp_path):
    provider = _StubProvider(["not json at all", DESIGN, CRITIQUE, SYNTH])
    res = await run_design_loop(
        "cnn", provider, mode="params", rounds=2, out_dir=tmp_path / "cnn2"
    )
    assert len(res.rounds) == 2
    assert res.rounds[0].verdict == "fail"
    assert res.rounds[1].verdict == "pass"


async def test_render_failure_feeds_back(tmp_path):
    bad = json.dumps({"concept": "x", "payload": {"panels": [{"generator": "no_such_piece", "seed": 1}]}})
    provider = _StubProvider([bad, DESIGN, CRITIQUE, SYNTH])
    res = await run_design_loop(
        "cnn", provider, mode="params", rounds=2, out_dir=tmp_path / "cnn3"
    )
    assert res.rounds[0].verdict == "fail"
    assert "render failed" in res.rounds[0].instruction
    assert res.rounds[1].verdict == "pass"


# --- the reconstruction seat: reference image in, Scene JSON out -------------

SCENE = json.dumps(
    {
        "concept": "a plate with a square on it",
        "payload": {
            "canvas": [100, 100],
            "paper": "a4",
            "orientation": "portrait",
            "inks": {"black": "#111111", "red": "#cb292a"},
            "widths_mm": [0.1, 0.5],
            "stages": ["main"],
            "occlusion": "cover",
            "title": "PLATE",
            "objects": [
                {
                    "name": "back plate",
                    "material": "cubist_plane",
                    "cover": [[0, 0], [100, 0], [100, 100], [0, 100]],
                    "marks": [
                        {"role": "contour", "points": [[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]]},
                        {"role": "hatch", "points": [[0, 50], [100, 50]]},
                    ],
                },
                {
                    "name": "front square",
                    "material": "cubist_plane",
                    "cover": [[30, 30], [70, 30], [70, 70], [30, 70]],
                    "ink": "red",
                    "width_mm": 0.5,
                    "marks": [{"role": "contour", "points": [[30, 30], [70, 30], [70, 70], [30, 70], [30, 30]]}],
                },
            ],
        },
    }
)


async def test_reference_image_reaches_designer_and_critic(tmp_path):
    ref = tmp_path / "reference.png"
    ref.write_bytes(b"fakepng")  # the stub never decodes it
    provider = _StubProvider([DESIGN, CRITIQUE, SYNTH])
    res = await run_design_loop(
        "cnn", provider, mode="params", rounds=1, out_dir=tmp_path / "ref", reference=ref
    )
    kinds = [k for k, _ in provider.calls]
    # designer now SEES the reference; critic gets reference + render
    assert kinds == ["vision", "vision", "text"]
    assert provider.calls[0][1] == [str(ref)]
    assert provider.calls[1][1][0] == str(ref)
    assert provider.calls[1][1][1].endswith("render.png")
    proposal = (tmp_path / "ref" / "final" / "PROPOSAL.md").read_text()
    assert "Reference:" in proposal
    assert res.rounds[0].verdict == "pass"


async def test_reference_is_found_by_convention(tmp_path):
    out = tmp_path / "conv"
    (out / "ref").mkdir(parents=True)
    (out / "ref" / "reference.png").write_bytes(b"fakepng")
    provider = _StubProvider([DESIGN, CRITIQUE, SYNTH])
    await run_design_loop("cnn", provider, mode="params", rounds=1, out_dir=out)
    assert [k for k, _ in provider.calls] == ["vision", "vision", "text"]


async def test_scene_mode_compiles_and_writes_artifacts(tmp_path):
    provider = _StubProvider([SCENE, CRITIQUE, SYNTH])
    res = await run_design_loop(
        "cnn", provider, mode="scene", rounds=1, out_dir=tmp_path / "scene"
    )
    r = res.rounds[0]
    assert r.verdict == "pass"
    rdir = tmp_path / "scene" / "rounds" / "r01"
    assert (rdir / "scene.json").exists()
    assert (rdir / "pen_plan.json").exists()
    assert r.render_path is not None and r.render_path.exists()
    plan = json.loads((rdir / "pen_plan.json").read_text())
    passes = [p for p in plan if "pen" in p]
    assert [(p["ink"], p["width_mm"]) for p in passes] == [("black", 0.1), ("red", 0.5)]
    # the designer prompt in scene mode inlines the playbook
    designer_prompt = provider.calls[0][1]
    assert designer_prompt.startswith("You are a DESIGNER")


async def test_scene_mode_invalid_scene_feeds_back(tmp_path):
    bad = json.dumps({"concept": "x", "payload": {"canvas": [10, 10], "objects": [{"name": "o", "ink": "chartreuse"}]}})
    provider = _StubProvider([bad, SCENE, CRITIQUE, SYNTH])
    res = await run_design_loop(
        "cnn", provider, mode="scene", rounds=2, out_dir=tmp_path / "scene2"
    )
    assert res.rounds[0].verdict == "fail"
    assert "render failed" in res.rounds[0].instruction
    assert res.rounds[1].verdict == "pass"
