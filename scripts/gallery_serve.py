"""Serve the gallery so the viewer can SAVE feedback to disk.

A `file://` page cannot write anywhere — which is why the viewer's judgements
used to die in `localStorage`. This is the smallest thing that fixes it: the
stdlib HTTP server, bound to loopback, serving `gallery/` and accepting one
POST.

Stdlib only and no package import, matching `gallery_index.py` — the project
env does not reliably resolve, so these tools must run from any interpreter.

    python scripts/gallery_serve.py
    -> http://localhost:8731/viewer.html
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gallery_feedback as fb  # noqa: E402
from gallery_plotter import PlotterBridge  # noqa: E402

logger = logging.getLogger(__name__)
REPO = Path(__file__).resolve().parent.parent
GALLERY = REPO / "gallery"
MAX_BODY = 256 * 1024
BRIDGE: PlotterBridge | None = None  # set in main()
# One writer at a time: the viewer's 1-5 / W-M-D keys can fire POSTs faster than
# write_views regenerates the markdown, and two interleaved rewrites race.
FEEDBACK_LOCK = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(GALLERY), **kw)

    def log_message(self, fmt, *args):  # quieter than the default access log
        if "POST" in (str(args[0]) if args else ""):  # log_error passes an HTTPStatus
            logger.info("%s", args[0])

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        route = self.path.split("?")[0]
        if route == "/feedback.json":
            try:
                self._json(200, {"records": fb.latest_by_target()})
            except Exception as e:  # never take the server down over a bad line
                logger.exception("feedback read failed")
                self._json(500, {"error": str(e)})
            return
        if route == "/plotter/state":
            self._json(200, BRIDGE.state())
            return
        if route == "/plotter/jobs":
            try:
                self._json(200, BRIDGE.jobs())
            except Exception as e:
                self._json(500, {"error": str(e)})
            return
        if route == "/plotter/layers":
            qs = parse_qs(urlparse(self.path).query)
            try:
                self._json(200, BRIDGE.layers((qs.get("target") or [""])[0]))
            except Exception as e:
                self._json(400, {"error": str(e)})
            return
        super().do_GET()

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BODY:
            raise ValueError(f"body must be 1..{MAX_BODY} bytes, got {n}")
        return json.loads(self.rfile.read(n))

    def do_POST(self):  # noqa: N802
        route = self.path.split("?")[0]
        if route == "/plotter/job":
            try:
                self._json(200, BRIDGE.start(self._body()))
            except Exception as e:
                logger.warning("plot refused: %s", e)
                self._json(400, {"error": str(e)})
            return
        if route == "/plotter/stop":
            self._json(200, BRIDGE.stop())
            return
        if route in ("/plotter/continue", "/plotter/pause", "/plotter/resume"):
            try:
                if route == "/plotter/continue":
                    has_body = int(self.headers.get("Content-Length") or 0) > 0
                    out = BRIDGE.continue_(self._body() if has_body else None)
                elif route == "/plotter/pause":
                    out = BRIDGE.pause()
                else:
                    out = BRIDGE.resume(self._body())
                self._json(200, out)
            except Exception as e:
                logger.warning("%s refused: %s", route, e)
                self._json(400, {"error": str(e)})
            return
        if route != "/feedback":
            self._json(404, {"error": "no such endpoint"})
            return
        try:
            record = self._body()
            # The target is a path this process will write about; keep it inside
            # the gallery so a crafted request cannot reach the rest of the disk.
            target = str(record.get("target", ""))
            resolved = (GALLERY / target).resolve()
            if not resolved.is_relative_to(GALLERY.resolve()):
                raise ValueError(f"target escapes the gallery: {target!r}")
            with FEEDBACK_LOCK:
                entry = fb.append(record)
                stats = fb.write_views()
            logger.info("%s %s %s -> %s", entry["scope"], entry["verdict"].upper(),
                        entry["target"], entry["piece"] or "no source on disk")
            self._json(200, {"ok": True, "entry": entry, "stats": stats})
        except Exception as e:
            logger.warning("rejected: %s", e)
            self._json(400, {"error": str(e)})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8731)
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--allow-plot", action="store_true",
                    help="let the viewer drive the plotter (off by default: this "
                         "turns a browser button into machine movement)")
    ap.add_argument("--serial-port", default=None, help="plotter serial port")
    ap.add_argument("--paper", default="a4:landscape", help="size:orientation or WxH")
    ap.add_argument("--margin", type=float, default=15.0)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    global BRIDGE
    BRIDGE = PlotterBridge(GALLERY, allow=args.allow_plot, port=args.serial_port,
                           paper=args.paper, margin=args.margin)

    if not (GALLERY / "viewer.html").exists():
        logger.error("no gallery/viewer.html — run: python scripts/gallery_index.py")
        return 1

    url = f"http://localhost:{args.port}/viewer.html"
    # Loopback only: this process writes files, so it must not be reachable
    # from the network.
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    logger.info("gallery on %s", url)
    logger.info("directions board on %s", url.rsplit("/", 1)[0] + "/board.html")
    logger.info("feedback -> studio/feedback.jsonl, studio/<slug>/FEEDBACK.md, "
                "studio/DIRECTIONS.md, studio/QUEUE.md")
    if args.allow_plot:
        logger.info("PLOTTING ENABLED — port %s, paper %s, margin %g",
                    args.serial_port or "(config default)", args.paper, args.margin)
        logger.info("the frame trace is enforced: no layer streams until one runs here")
    else:
        logger.info("plotting disabled (pass --allow-plot to drive the machine)")
    logger.info("ctrl-c to stop")
    if not args.no_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        logger.info("\nstopped")
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
