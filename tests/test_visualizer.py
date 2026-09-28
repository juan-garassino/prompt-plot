"""Tests for promptplot/visualizer.py — GCodeVisualizer."""

import pytest
from pathlib import Path

from promptplot.models import GCodeCommand, GCodeProgram
from promptplot.config import PromptPlotConfig

try:
    from promptplot.visualizer import GCodeVisualizer
    import matplotlib
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not MATPLOTLIB_AVAILABLE, reason="matplotlib not installed"
)


@pytest.fixture
def config():
    return PromptPlotConfig()


@pytest.fixture
def visualizer(config):
    return GCodeVisualizer(config)


@pytest.fixture
def simple_program():
    return GCodeProgram(commands=[
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=10, y=10),
        GCodeCommand(command="M3", s=1000),
        GCodeCommand(command="G1", x=50, y=50, f=2000),
        GCodeCommand(command="G1", x=80, y=80, f=2000),
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=0, y=0),
    ])


@pytest.fixture
def oob_program():
    """Program with out-of-bounds segments."""
    return GCodeProgram(commands=[
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=10, y=10),
        GCodeCommand(command="M3", s=1000),
        GCodeCommand(command="G1", x=500, y=500, f=2000),
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=0, y=0),
    ])


@pytest.fixture
def empty_program():
    return GCodeProgram(commands=[GCodeCommand(command="M5")])


class TestGCodeVisualizer:
    def test_construction(self, config):
        viz = GCodeVisualizer(config)
        assert viz.config is config

    def test_preview_creates_file(self, visualizer, simple_program, tmp_path):
        output = str(tmp_path / "test_preview.png")
        visualizer.preview(simple_program, output)
        assert Path(output).exists()
        assert Path(output).stat().st_size > 0

    def test_preview_empty_program(self, visualizer, empty_program, tmp_path):
        output = str(tmp_path / "empty_preview.png")
        visualizer.preview(empty_program, output)
        assert Path(output).exists()

    def test_preview_oob_program(self, visualizer, oob_program, tmp_path):
        output = str(tmp_path / "oob_preview.png")
        visualizer.preview(oob_program, output)
        assert Path(output).exists()

    def test_get_stats(self, visualizer, simple_program):
        stats = visualizer.get_stats(simple_program)
        assert "drawing_distance" in stats
        assert "travel_distance" in stats
        assert "pen_cycles" in stats
        assert "total_commands" in stats
        assert stats["drawing_distance"] > 0
        assert stats["pen_cycles"] >= 1

    def test_get_stats_empty(self, visualizer, empty_program):
        stats = visualizer.get_stats(empty_program)
        assert stats["drawing_distance"] == 0
        assert stats["pen_cycles"] == 0

    def test_stats_drawing_segments(self, visualizer, simple_program):
        stats = visualizer.get_stats(simple_program)
        assert stats["drawing_segments"] == 2  # Two G1 commands while pen is down

    def test_construction_without_config(self):
        viz = GCodeVisualizer()
        assert viz.config is None

    def test_analyze_regions_returns_report(self, visualizer, simple_program):
        report = visualizer.analyze_regions(simple_program, creative_mode="figurative")
        assert "global" in report
        assert "regions" in report
        assert len(report["regions"]) > 0

    def test_save_analysis_artifacts(self, visualizer, simple_program, tmp_path):
        artifacts = visualizer.save_analysis_artifacts(
            simple_program,
            str(tmp_path / "analysis"),
            creative_mode="abstract",
        )
        assert Path(artifacts["preview_path"]).exists()
        assert Path(artifacts["overlay_path"]).exists()
        assert Path(artifacts["heatmap_path"]).exists()
        assert Path(artifacts["json_path"]).exists()
        assert artifacts["analysis"]["creative_mode"] == "abstract"


class _RecordingVisualizer(GCodeVisualizer if MATPLOTLIB_AVAILABLE else object):
    """Records which renderer each frame went through instead of drawing."""

    def __init__(self, config=None):
        super().__init__(config)
        self.calls = []

    def _render(self, lines, stats, output_path, title=None):
        self.calls.append(("mono", len(lines), stats["total_commands"], output_path))
        Path(output_path).write_bytes(b"png")

    def _render_color_layers(self, lines, stats, output_path, palette, pen_widths=None, title=None):
        self.calls.append(("color", len(lines), stats["total_commands"], output_path))
        Path(output_path).write_bytes(b"png")


@pytest.fixture
def two_color_program():
    return GCodeProgram(commands=[
        GCodeCommand(command="M3", s=1000, color=0),
        GCodeCommand(command="G1", x=10, y=10, color=0),
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=20, y=20),
        GCodeCommand(command="M3", s=1000, color=1),
        GCodeCommand(command="G1", x=40, y=40, color=1),
        GCodeCommand(command="M5"),
    ])


class TestPreviewFrames:
    def test_writes_requested_frames(self, visualizer, simple_program, tmp_path):
        paths = visualizer.preview_frames(simple_program, str(tmp_path / "f"), frames=3)
        assert [Path(p).name for p in paths] == ["frame_001.png", "frame_002.png", "frame_003.png"]
        assert all(Path(p).stat().st_size > 0 for p in paths)

    def test_frames_are_cumulative_and_end_on_full_program(self, config, simple_program, tmp_path):
        viz = _RecordingVisualizer(config)
        viz.preview_frames(simple_program, str(tmp_path), frames=3)
        counts = [c[2] for c in viz.calls]
        assert counts == sorted(counts)
        assert counts[-1] == len(simple_program.commands)

    def test_frames_capped_at_command_count(self, config, simple_program, tmp_path):
        viz = _RecordingVisualizer(config)
        paths = viz.preview_frames(simple_program, str(tmp_path), frames=500)
        assert len(paths) == len(simple_program.commands)
        assert [c[2] for c in viz.calls] == list(range(1, len(simple_program.commands) + 1))

    def test_render_mode_fixed_by_full_program(self, config, two_color_program, tmp_path):
        # early frames only hold colour 0, but every frame must match the final render
        viz = _RecordingVisualizer(config)
        viz.preview_frames(two_color_program, str(tmp_path), frames=len(two_color_program.commands))
        assert {c[0] for c in viz.calls} == {"color"}

    def test_rejects_non_positive_frames(self, visualizer, simple_program, tmp_path):
        with pytest.raises(ValueError):
            visualizer.preview_frames(simple_program, str(tmp_path), frames=0)
