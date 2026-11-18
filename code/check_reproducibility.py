"""Reproducibility check (requirement R11).

Runs wastewater_analysis.py twice in fresh Python processes and confirms that every
output file (CSV and PNG) is byte-identical across the two runs, using the SHA-256 hashes
recorded in outputs/run_manifest.json. The result is written to
outputs/reproducibility_check.json.

Usage (from the project folder):   python code/check_reproducibility.py
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "code" / "wastewater_analysis.py"
MANIFEST = ROOT / "outputs" / "run_manifest.json"


def run_once():
    """Run the analysis in a new process and return its output hashes."""
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["outputs_sha256"]


first, second = run_once(), run_once()
differences = sorted(k for k in first.keys() | second.keys() if first.get(k) != second.get(k))
result = {"files_compared": len(first), "identical": not differences, "differences": differences}
(ROOT / "outputs" / "reproducibility_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
sys.exit(0 if not differences else 1)
