"""The public bucket's bootstrap record: scripts/prints_cors.json + setup_prints_bucket.sh.

The bucket gs://garassino-ai-prints already exists; these files are how it was
made and how to rebuild it. Nothing here calls gcloud — the script is only
syntax-checked with ``bash -n``.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_bucket_files_are_shaped_right():
    cors = json.loads((REPO / "scripts" / "prints_cors.json").read_text())
    assert cors == [{
        "origin": ["https://artificial-artifacts.com", "https://www.artificial-artifacts.com",
                   "https://artificial-artifacts.web.app",
                   "https://artificial-artifacts-staging.web.app",
                   "http://localhost:8081", "http://127.0.0.1:8081"],
        "method": ["GET"], "responseHeader": ["Content-Type"], "maxAgeSeconds": 3600}]
    script = REPO / "scripts" / "setup_prints_bucket.sh"
    bash = shutil.which("bash")
    assert bash and subprocess.run([bash, "-n", str(script)]).returncode == 0
    text = script.read_text()
    assert "set -euo pipefail" in text and "prints_cors.json" in text
    assert "allUsers" in text and "roles/storage.objectViewer" in text
