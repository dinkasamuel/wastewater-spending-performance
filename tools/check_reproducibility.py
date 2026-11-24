"""Reproducibility check (requirement R11).

Runs the master notebook twice, each time in a fresh kernel, and confirms that every
result file (CSV and PNG) is byte-identical across the two runs, using the SHA-256
hashes the notebook records in 3_results/tables/run_manifest.json.
The verdict is written to 3_results/tables/reproducibility_check.json.

Usage (from the project folder):   python tools/check_reproducibility.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_analysis import execute  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "3_results" / "tables" / "run_manifest.json"


def run_once():
    execute(save=False)
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["outputs_sha256"]


first, second = run_once(), run_once()
differences = sorted(k for k in first.keys() | second.keys() if first.get(k) != second.get(k))
result = {"files_compared": len(first), "identical": not differences, "differences": differences}
(MANIFEST.parent / "reproducibility_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
sys.exit(0 if not differences else 1)
