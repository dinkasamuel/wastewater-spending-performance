"""Colour-contrast check for the Power BI dashboard (requirement R12a, WCAG 2.1).

Computes the WCAG contrast ratio of every text colour and every company line colour
used in dashboard v3 against the backgrounds they appear on:
  - text: at least 4.5:1 (WCAG 1.4.3, normal text);
  - lines and markers (graphical objects): at least 3:1 (WCAG 1.4.11).
Colours are read from the build script and the report theme. Writes
outputs/contrast_check.csv.

Usage (from the project folder):   python code/check_contrast.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = next((ROOT / "powerbi" / "v3").rglob("BaseThemes/*.json"))
OUT = ROOT / "outputs" / "contrast_check.csv"


def luminance(hex_colour):
    """Relative luminance (WCAG 2.1 definition)."""
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(fg, bg):
    hi, lo = sorted([luminance(fg), luminance(bg)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


theme = json.loads(THEME.read_text(encoding="utf-8"))
import re                                    # colours actually applied per company (build script)
_src = (ROOT / "code" / "build_powerbi_v3.py").read_text(encoding="utf-8")
theme["dataColors"] = re.findall(r'"[A-Z]{3}": "(#[0-9A-F]{6})"', _src.split("COMPANY_COLOURS = ")[1].split("}")[0])
page_bg = theme["visualStyles"]["page"]["*"]["background"][0]["color"]["solid"]["color"]
items = [("Header title (navy)", "#17333B", "#FFFFFF", "text", 4.5),
         ("Header tags (blue)", "#1F5F8B", "#FFFFFF", "text", 4.5),
         ("Header context (grey)", "#36535C", "#FFFFFF", "text", 4.5),
         ("Table and axis text (theme foreground)", theme["foreground"], "#FFFFFF", "text", 4.5),
         ("Secondary text (theme)", theme["foregroundNeutralSecondary"], "#FFFFFF", "text", 4.5)]
companies = ["ANH", "NES", "SRN", "SVE", "SWB", "TMS", "UUW", "WSX", "YKY"]   # legend order
items += [(f"Line colour {i + 1} ({c})", col, "#FFFFFF", "graphic", 3.0)
          for i, (c, col) in enumerate(zip(companies, theme["dataColors"]))]

rows = []
for name, fg, bg, kind, need in items:
    r = ratio(fg, bg)
    rows.append({"element": name, "colour": fg, "background": bg, "type": kind,
                 "ratio": round(r, 2), "required": need, "passes": r >= need})
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['element']:42s} {r['colour']}  {r['ratio']:5.2f}:1  need {r['required']}  {'PASS' if r['passes'] else 'FAIL'}")
print("page background", page_bg)
