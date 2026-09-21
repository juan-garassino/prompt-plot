"""ATTENTION AS TOPOGRAPHY — the exploded-axonometric DAG.

A thin wrapper so the package piece is regenerable through the same harness as
every studio plate, and so its GCode carries the standard provenance header.
The composition itself lives in promptplot/generative/pieces/ml.py.
"""

from __future__ import annotations

from promptplot.generative.pieces.ml import bauhaus_relevance


def attention_dag(rng, bounds, colors: int = 4):
    return bauhaus_relevance(rng, bounds, colors=colors)
