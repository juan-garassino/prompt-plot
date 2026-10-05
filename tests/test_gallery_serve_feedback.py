"""POST /feedback and GET /feedback.json on the gallery server, both scopes.

A real ThreadingHTTPServer on port 0 (the pattern of
tests/test_plotjob.py::test_server_routes), every path repointed at tmp.
"""

from __future__ import annotations

import json
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gallery_directions as gd  # noqa: E402
import gallery_feedback as fb  # noqa: E402
import gallery_serve  # noqa: E402


@pytest.fixture
def server(tmp_path, monkeypatch):
    from http.server import ThreadingHTTPServer

    st, gal = tmp_path / "studio", tmp_path / "gallery"
    (st / "ising").mkdir(parents=True)
    (gal / "studio" / "ising" / "current").mkdir(parents=True)
    (gal / "viewer.html").write_text("<html></html>")
    for mod, name, val in ((fb, "STUDIO", st), (fb, "GALLERY", gal), (fb, "REPO", tmp_path),
                           (fb, "LOG", st / "feedback.jsonl"), (gd, "STUDIO", st),
                           (gd, "GALLERY", gal), (gallery_serve, "GALLERY", gal)):
        monkeypatch.setattr(mod, name, val)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), gallery_serve.Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"

    def call(route: str, body: dict | None = None, raw: bytes | None = None):
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        req = urllib.request.Request(base + route, data=data,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            with e:
                return e.code, json.loads(e.read())

    try:
        yield call, st
    finally:
        srv.shutdown()
        srv.server_close()


RENDER = {"target": "studio/ising/current/pp_ising_v6.png", "subject": "studio/ising",
          "verdict": "archive", "note": "not now"}
DIRECTION = {"scope": "direction", "subject": "studio/ising", "direction": "r02",
             "label": "COOLING STRIP", "root": "r02",
             "target": "studio/ising/@direction/r02", "verdict": "works"}


def test_post_both_scopes_and_read_back(server):
    call, st = server
    code, out = call("/feedback", RENDER)
    assert code == 200 and out["entry"]["scope"] == "render"
    code, out = call("/feedback", DIRECTION)
    assert code == 200 and out["entry"]["direction"] == "r02"
    assert out["stats"]["directions"] == 1
    code, out = call("/feedback.json")
    assert code == 200
    recs = out["records"]
    assert recs["studio/ising/current/pp_ising_v6.png"]["verdict"] == "archive"
    assert recs["studio/ising/@direction/r02"]["scope"] == "direction"
    assert (st / "DIRECTIONS.md").exists() and (st / "ising" / "FEEDBACK.md").exists()


@pytest.mark.parametrize("body", [
    {**RENDER, "verdict": "works"},
    {**DIRECTION, "verdict": "keep"},
    {**DIRECTION, "target": "studio/ising/@direction/r03"},
    {**DIRECTION, "direction": "Cooling"},
    {**RENDER, "target": "studio/ising/@direction/r02"},
    {**RENDER, "target": "../../etc/passwd"},
    {**RENDER, "scope": "nope"},
])
def test_post_rejections(server, body):
    call, st = server
    code, out = call("/feedback", body)
    assert code == 400 and out["error"]
    assert not (st / "feedback.jsonl").exists()


def test_post_bad_bodies(server):
    call, _st = server
    assert call("/feedback", raw=b"not json")[0] == 400
    assert call("/nowhere", {})[0] == 404


def test_rapid_posts_are_serialised(server):
    call, st = server
    results = []

    def post(w: int) -> None:
        # 4 workers x 3 posts: concurrent, but inside socketserver's listen backlog of 5
        for j in range(3):
            i = w * 3 + j
            v = ("keep", "rework", "archive", "cut", "promote")[i % 5]
            try:
                results.append(call("/feedback", {
                    **RENDER, "verdict": v,
                    "target": f"studio/ising/current/pp_ising_v{i}.png"})[0])
            except Exception as e:  # surface it in the assertion, not as a thread warning
                results.append(repr(e))

    threads = [threading.Thread(target=post, args=(w,)) for w in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results == [200] * 12
    lines = (st / "feedback.jsonl").read_text().splitlines()
    assert len(lines) == 12 and all(json.loads(x)["scope"] == "render" for x in lines)
    assert gallery_serve.FEEDBACK_LOCK.acquire(blocking=False)
    gallery_serve.FEEDBACK_LOCK.release()
