"""Static inspection of the Power BI PBIP report definition (R12a evidence).

Lists every page and visual with its type, bound fields and any text,
so the acceptance checklist (UI03-UI07, R10) can be assessed against the
saved report definition. Read-only: nothing in the PBIP folder is changed.

Usage:  python inspect_pbip.py <path-to-Wastewater_Review.Report>
"""
import json
import re
import sys
from pathlib import Path


def fields(obj, found):
    """Collect 'Entity.Property' references anywhere in a visual definition."""
    if isinstance(obj, dict):
        if "Property" in obj and isinstance(obj.get("Expression"), dict):
            ent = obj["Expression"].get("SourceRef", {}).get("Entity", "?")
            found.add(f'{ent}.{obj["Property"]}')
        for v in obj.values():
            fields(v, found)
    elif isinstance(obj, list):
        for v in obj:
            fields(v, found)
    return found


def texts(obj, found):
    """Collect literal strings (titles, text boxes) from a visual definition."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("value", "text") and isinstance(v, str) and len(v) > 2:
                found.append(re.sub(r"^'|'$", "", v))
            texts(v, found)
    elif isinstance(obj, list):
        for v in obj:
            texts(v, found)
    return found


def main(report_dir):
    pages = Path(report_dir) / "definition" / "pages"
    order = json.loads((pages / "pages.json").read_text(encoding="utf-8")).get("pageOrder", [])
    for pid in order:
        page = json.loads((pages / pid / "page.json").read_text(encoding="utf-8"))
        print(f"\n=== {page.get('displayName')}  ({page.get('width')}x{page.get('height')})")
        for vf in sorted((pages / pid / "visuals").glob("*/visual.json")):
            v = json.loads(vf.read_text(encoding="utf-8"))
            vis = v.get("visual", {})
            vtype = vis.get("visualType", "?")
            pos = v.get("position", {})
            f = sorted(fields(vis.get("query", {}), set()))
            t = [s for s in texts(vis, []) if not s.startswith("#")]
            print(f"- {vtype:22s} y={pos.get('y', 0):>5.0f}  fields={f}")
            for s in t[:6]:
                print(f"      text: {s[:160]}")
            inter = v.get("filterConfig") or vis.get("visualContainerObjects", {})
            if "drillFilterOtherVisuals" in json.dumps(v):
                print("      note: drillFilterOtherVisuals set")


if __name__ == "__main__":
    main(sys.argv[1])
