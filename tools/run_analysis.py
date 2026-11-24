"""Run the master notebook 2_analysis/analysis.ipynb from top to bottom and save it.

This is the same as opening the notebook and choosing Kernel > Restart & Run All:
every output shown in the saved notebook comes from this fresh run.

Usage (from the project folder):   python tools/run_analysis.py
"""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "2_analysis" / "analysis.ipynb"


def execute(save=True):
    """Execute the notebook in a fresh kernel, running from 2_analysis/."""
    nb = nbformat.read(NOTEBOOK, as_version=4)
    NotebookClient(nb, timeout=1800, kernel_name="python3",
                   resources={"metadata": {"path": str(NOTEBOOK.parent)}}).execute()
    if save:
        nbformat.write(nb, NOTEBOOK)
    return nb


if __name__ == "__main__":
    execute()
    print("Notebook executed and saved:", NOTEBOOK.relative_to(ROOT))
