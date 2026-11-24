"""Generate the Chapter 4 UML figures as SVG.

Figure 4.1  Whole-project UML activity diagram with partitions (swimlanes).
            Each action carries an ID (A1, B1, ...) and its requirement,
            research-question and objective tags.
Figure 4.2  Requirements dependency and traceability diagram. Each
            requirement names its purpose, the research questions it serves
            and the Figure 4.1 actions that realise it.

Author: Dinka Christabel Samuel (drafted with AI assistance; see the
AI-use disclosure in Appendix A). Pure standard-library Python: no
dependencies. Run from the project folder:  python code/make_uml_figures.py
The SVGs are written to figures/. PNG copies are rendered with headless Google Chrome (or Microsoft Edge):
  chrome --headless=new --force-device-scale-factor=2 --window-size=1340,<height>
         --screenshot=<file>.png <file>.svg   (height 2080 for Figure 4.1, 1578 for Figure 4.2)
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "figures"
FONT = "Segoe UI, Arial, sans-serif"
INK = "#1f2933"
ACCENT = "#1f5f8b"   # requirement / RQ tags
LINE = "#3e4c59"
FILL = "#f4f7fa"
LANE_FILL = ["#ffffff", "#fbfcfd"]


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.parts = w, h, []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=17, weight="normal", fill=INK, anchor="middle",
             style="normal", rotate=None):
        tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
                 f'font-weight="{weight}" font-style="{style}" fill="{fill}" '
                 f'text-anchor="{anchor}" dominant-baseline="middle"{tr}>{escape(s)}</text>')

    def path(self, pts, dashed=False, arrow=True, width=1.8, dotted=False):
        d = " ".join(("M" if i == 0 else "L") + f"{x},{y}" for i, (x, y) in enumerate(pts))
        dash = ' stroke-dasharray="8,6"' if dashed else (' stroke-dasharray="2,5"' if dotted else "")
        mk = ' marker-end="url(#arrow)"' if arrow else ""
        self.add(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{width}"{dash}{mk}/>')

    def save(self, name, crop_top=0):
        """Write the SVG. crop_top removes empty space at the top: the figure title
        lives in the report caption, not inside the image."""
        h = self.h - crop_top
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{h}" '
                f'viewBox="0 {crop_top} {self.w} {h}">'
                '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9.5" refY="5" '
                'markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10" fill="none" stroke="{LINE}" stroke-width="1.6"/>'
                '</marker></defs>'
                f'<rect y="{crop_top}" width="{self.w}" height="{h}" fill="#ffffff"/>')
        (OUT / name).write_text(head + "".join(self.parts) + "</svg>", encoding="utf-8")


# ---------------------------------------------------------------- Figure 4.1
def figure_4_1():
    W, H = 1340, 2140
    s = SVG(W, H)
    # partitions: (label, x0, x1)
    lanes = [("Researcher", 50, 330), ("Python pipeline (notebook + src)", 330, 850),
             ("Power BI artefact", 850, 1100), ("Supervisor", 1100, 1340)]
    cx = {"R": 190, "P": 590, "PL": 465, "PR": 715, "B": 975, "S": 1220}
    BW = {"R": 240, "P": 280, "PL": 230, "PR": 230, "B": 230, "S": 190}
    BH = 76

    phase_rows = [3, 6, 8, 15.2]
    def y(r):
        return 230 + (r - 1) * 100 + 40 * sum(1 for p in phase_rows if r >= p)

    top, bottom = 70, H - 20
    for i, (lab, x0, x1) in enumerate(lanes):
        s.add(f'<rect x="{x0}" y="{top}" width="{x1-x0}" height="{bottom-top}" '
              f'fill="{LANE_FILL[i % 2]}" stroke="{LINE}" stroke-width="1.2"/>')
        s.add(f'<rect x="{x0}" y="{top}" width="{x1-x0}" height="44" fill="#e4ebf1" '
              f'stroke="{LINE}" stroke-width="1.2"/>')
        s.text((x0 + x1) / 2, top + 22, lab, size=18, weight="bold")
    s.add(f'<rect x="0" y="{top}" width="50" height="{bottom-top}" fill="#eef2f5" '
          f'stroke="{LINE}" stroke-width="1.2"/>')

    # phase bands (strip on the left + dashed separators)
    bounds = [top + 44] + [y(p) - 70 for p in phase_rows] + [bottom]
    names = ["Scope & research (Ch 1–2)", "Feasibility (Ch 3)", "Design (Ch 4)",
             "Implementation (Ch 5)", "Results & evaluation (Ch 6–7)"]
    for i, nm in enumerate(names):
        a, b = bounds[i], bounds[i + 1]
        if i > 0:
            s.add(f'<line x1="0" y1="{a}" x2="{W}" y2="{a}" stroke="#9aa5b1" '
                  f'stroke-width="1.4" stroke-dasharray="10,6"/>')
        s.text(25, (a + b) / 2, nm, size=16, weight="bold", rotate=-90)

    def action(key, lane, r, title, desc, tag, dashed=False):
        x, w = cx[lane], BW[lane]
        yy = y(r)
        dash = ' stroke-dasharray="8,6"' if dashed else ""
        s.add(f'<rect x="{x-w/2}" y="{yy-BH/2}" width="{w}" height="{BH}" rx="16" '
              f'fill="{FILL}" stroke="{LINE}" stroke-width="1.8"{dash}/>')
        s.text(x, yy - 22, f"{key}  {title}", size=17, weight="bold")
        s.text(x, yy, desc, size=15)
        s.text(x, yy + 22, tag, size=14, weight="bold", fill=ACCENT)
        return x, yy, w

    def decision(lane, r, l1, l2, w=210, h=70):
        x, yy = cx[lane], y(r)
        s.add(f'<polygon points="{x},{yy-h/2} {x+w/2},{yy} {x},{yy+h/2} {x-w/2},{yy}" '
              f'fill="#fff8e6" stroke="{LINE}" stroke-width="1.8"/>')
        s.text(x, yy - 10, l1, size=14, weight="bold")
        s.text(x, yy + 10, l2, size=14, weight="bold")

    def bar(r, x0=420, x1=760):
        s.add(f'<rect x="{x0}" y="{y(r)-4}" width="{x1-x0}" height="8" fill="{INK}"/>')

    def label(x, yy, t, anchor="start"):
        s.text(x, yy, t, size=14, style="italic", anchor=anchor)

    # ---- nodes
    s.add(f'<circle cx="{cx["R"]}" cy="{y(1)-70}" r="11" fill="{INK}"/>')
    action("A1", "R", 1, "Define scope", "aim, objectives, RQ1–RQ4", "Obj 1–6 · RQ1–RQ4")
    action("S1", "S", 1, "Agree scope", "England, 9 WaSCs", "supervision")
    action("A2", "R", 2, "Review literature", "identify gaps G1–G3", "G1–G3")
    action("B1", "P", 3, "Audit sources", "coverage, units, definitions", "R01")
    decision("R", 4, "Pre-2020 totex", "joinable?")
    action("B3", "R", 5, "Adopt base costs", "balanced 2017-18 to 2024-25", "R03 R04 · 18 Nov")
    action("C1", "R", 6, "Derive requirements", "R01–R14, MoSCoW", "Figure 4.2")
    action("S2", "S", 6, "Feedback", "traceability, UML links", "3 Oct 2026")
    action("C2", "R", 7, "Design artefact", "components, data, views", "R01–R14 mapped")
    # UML note for R14
    nx, ny, nw, nh = cx["P"], y(7), 300, 66
    s.add(f'<path d="M{nx-nw/2},{ny-nh/2} L{nx+nw/2-16},{ny-nh/2} L{nx+nw/2},{ny-nh/2+16} '
          f'L{nx+nw/2},{ny+nh/2} L{nx-nw/2},{ny+nh/2} Z" fill="#fffdf2" stroke="{LINE}" stroke-width="1.4"/>')
    s.text(nx, ny - 12, "R14 Won't: no prediction and", size=15)
    s.text(nx, ny + 12, "no composite company ranking", size=15)
    action("D1", "P", 8, "Extract sources", "cell references + SHA-256", "R02")
    action("D2", "P", 9, "Build panel", "2022-23 prices, £/property, periods", "R01 R03 R04 R05 · Obj 1")
    decision("P", 10, "Validation", "checks pass?")
    action("D4", "R", 10, "Record and correct", "failure logged, fix applied", "R03")
    bar(10.8)
    action("E1", "PL", 11.6, "Descriptive trends", "companies × years", "R06 · RQ1 · Obj 2")
    action("E2", "PR", 11.6, "Adjusted models", "company + year effects, CV3", "R07 · RQ2 · Obj 3")
    action("E3", "PR", 12.6, "Sensitivity", "scale, omission, timing", "R05 R08 · RQ3 · Obj 4")
    bar(13.4)
    action("E4", "P", 14.2, "Export and rerun", "fact tables, fresh kernel", "R11 · Obj 6")
    action("F1", "B", 14.2, "Power BI report", "6 pages, RQ-tagged", "R06 R09 R10 · RQ4 · Obj 5")
    action("G1", "R", 15.2, "Evaluate", "data, analysis, artefact", "R12a R12b · RQ4 · Obj 6")
    decision("S", 16.2, "Changes", "needed?", w=180)
    action("G3", "R", 17.2, "Report and reflect", "answer RQ1–RQ4", "Ch 6–8")
    ex, ey = cx["R"], y(18) - 20
    s.add(f'<circle cx="{ex}" cy="{ey}" r="13" fill="none" stroke="{INK}" stroke-width="2"/>'
          f'<circle cx="{ex}" cy="{ey}" r="8" fill="{INK}"/>')

    # ---- flows
    R, P, B, S_ = cx["R"], cx["P"], cx["B"], cx["S"]
    h2 = BH / 2
    s.path([(R, y(1) - 59), (R, y(1) - h2)])
    s.path([(R + 120, y(1)), (S_ - 95, y(1))])
    s.path([(S_, y(1) + h2), (S_, y(2)), (R + 120, y(2))])
    s.path([(R, y(2) + h2), (R, y(3)), (P - 140, y(3))])
    s.path([(P, y(3) + h2), (P, y(3) + 50), (R, y(3) + 50), (R, y(4) - 35)])
    s.path([(R, y(4) + 35), (R, y(5) - h2)]); label(R + 8, y(4) + 50, "[no]")
    s.path([(R + 105, y(4)), (322, y(4)), (322, y(6) - 52), (262, y(6) - 52), (262, y(6) - h2)])
    label(R + 112, y(4) - 14, "[yes]")
    s.path([(R, y(5) + h2), (R, y(6) - h2)])
    s.path([(S_ - 95, y(6)), (R + 120, y(6))], dashed=True)
    label(700, y(6) - 14, "object flow: supervisory feedback", anchor="middle")
    s.path([(R, y(6) + h2), (R, y(7) - h2)])
    s.path([(nx - 150, y(7)), (R + 120, y(7))], arrow=False, dotted=True, width=1.6)
    s.path([(R, y(7) + h2), (R, y(8)), (P - 140, y(8))])
    s.path([(P, y(8) + h2), (P, y(9) - h2)])
    s.path([(P, y(9) + h2), (P, y(10) - 35)])
    s.path([(P - 105, y(10)), (R + 120, y(10))]); label(P - 160, y(10) - 14, "[no]")
    s.path([(R, y(10) - h2), (R, y(9)), (P - 140, y(9))])
    s.path([(P, y(10) + 35), (P, y(10.8) - 4)]); label(P + 8, y(10) + 48, "[yes]")
    s.path([(cx["PL"], y(10.8) + 4), (cx["PL"], y(11.6) - h2)])
    s.path([(cx["PR"], y(10.8) + 4), (cx["PR"], y(11.6) - h2)])
    s.path([(cx["PR"], y(11.6) + h2), (cx["PR"], y(12.6) - h2)])
    s.path([(cx["PL"], y(11.6) + h2), (cx["PL"], y(13.4) - 4)])
    s.path([(cx["PR"], y(12.6) + h2), (cx["PR"], y(13.4) - 4)])
    s.path([(P, y(13.4) + 4), (P, y(14.2) - h2)])
    s.path([(P + 140, y(14.2)), (B - 115, y(14.2))])
    s.path([(B, y(14.2) + h2), (B, y(15.2) - 56), (R, y(15.2) - 56), (R, y(15.2) - h2)])
    s.path([(R + 120, y(15.2)), (S_, y(15.2)), (S_, y(16.2) - 35)])
    s.path([(S_, y(16.2) + 35), (S_, y(17.2)), (R + 120, y(17.2))]); label(S_ + 8, y(16.2) + 50, "[no]")
    s.path([(S_ + 90, y(16.2)), (1328, y(16.2)), (1328, y(6)), (S_ + 95, y(6))])
    label(1322, y(7) + 10, "[yes] change request", anchor="end")
    s.path([(R, y(17.2) + h2), (R, ey - 14)])

    # legend
    lx, ly = 380, y(17.2) + 40
    for i, t in enumerate([
            "Tags: R = requirement (Figure 4.2); RQ = research question;",
            "Obj = objective; G = research gap. Diamond = decision;",
            "bars = fork/join; dashed = object flow; folded box = note.",
            "Action IDs (A1…G3) are cited in Figure 4.2 and Appendix B."]):
        s.text(lx, ly + i * 20, t, size=14, anchor="start")
    s.save("fig4_1_project_activity.svg", crop_top=60)


# ---------------------------------------------------------------- Figure 4.2
REQS = {
    # id: (col, layer, priority, name, purpose, rqs, realised)
    "R01": (2, 0, "Must", "Define scope and metric boundaries", "Fixes what is measured", "RQ1–RQ3", "B1, D2"),
    "R02": (2, 1, "Must", "Preserve sources and provenance", "Every value is traceable", "RQ1–RQ4", "D1"),
    "R03": (2, 2, "Must", "Build validated company-year panel", "One unique row per company-year", "RQ1–RQ3", "B3, D2, D4"),
    "R04": (1, 3, "Must", "Consistent prices and intensity", "Spending is comparable", "RQ1–RQ3", "D2"),
    "R05": (3, 3, "Must", "Retain actual measurement periods", "Timing comparisons are honest", "RQ2–RQ3", "D2, E3"),
    "R06": (1, 4, "Must", "Separate outcomes, units, direction", "No hidden trade-offs", "RQ1, RQ4", "E1, F1"),
    "R07": (2, 4, "Must", "Proportionate association models", "Answers RQ2 with uncertainty", "RQ2", "E2"),
    "R09": (1, 5, "Must", "Interactive company/year views", "User-led comparison", "RQ4", "F1"),
    "R08": (2, 5, "Must", "Sensitivity analysis", "Measure, timing, company checks", "RQ3", "E3"),
    "R10": (2, 6, "Must", "Expose definitions and limits", "Prevents misreading", "RQ1–RQ4", "F1"),
    "R11": (3, 6, "Must", "Reproducible fresh-kernel run", "Independent verification", "RQ1–RQ4", "E4"),
    "R12a": (1, 7, "Must", "Researcher-led evaluation", "Tasks, heuristics, accessibility", "RQ4", "G1"),
    "R13": (1, 8, "Could", "Exportable comparison view", "Reuse with context kept", "RQ4", "F1 (optional)"),
    "R12b": (2, 8, "Should", "Small user evaluation", "Only if ethics approved by 4 Dec", "RQ4", "G1"),
    "R14": (3, 0, "Won't", "No prediction or company ranking", "Outside scope; could mislead", "—", "excluded by design"),
}


def figure_4_2():
    W, H = 1340, 1640
    s = SVG(W, H)
    COL = {1: 230, 2: 670, 3: 1110}
    BW, BH = 400, 122
    def Y(layer):
        return 170 + layer * 165

    def box(rid):
        c, L, pr, name, why, rqs, real = REQS[rid]
        x, yy = COL[c], Y(L)
        dash = ' stroke-dasharray="8,6"' if pr == "Won't" else ""
        fill = "#fbfbfb" if pr != "Must" else FILL
        s.add(f'<rect x="{x-BW/2}" y="{yy-BH/2}" width="{BW}" height="{BH}" fill="{fill}" '
              f'stroke="{LINE}" stroke-width="1.8"{dash}/>')
        s.add(f'<line x1="{x-BW/2}" y1="{yy-BH/2+30}" x2="{x+BW/2}" y2="{yy-BH/2+30}" '
              f'stroke="{LINE}" stroke-width="1"/>')
        s.text(x - BW / 2 + 12, yy - BH / 2 + 15, f"«requirement»  {rid}", size=15,
               weight="bold", anchor="start")
        s.text(x + BW / 2 - 12, yy - BH / 2 + 15, f"[{pr}]", size=15, weight="bold",
               anchor="end")
        s.text(x, yy - 14, name, size=17, weight="bold")
        s.text(x, yy + 12, f"Purpose: {why}", size=15)
        tag = "Not implemented: excluded by design" if pr == "Won't" else f"{rqs}  ·  realised in {real}"
        s.text(x, yy + 38, tag, size=15, weight="bold", fill=ACCENT)

    for rid in REQS:
        box(rid)

    def top(rid, dx=0):
        c, L, *_ = REQS[rid]
        return COL[c] + dx, Y(L) - BH / 2

    def bot(rid, dx=0):
        c, L, *_ = REQS[rid]
        return COL[c] + dx, Y(L) + BH / 2

    def mid(l1, off=0):
        return (Y(l1) + BH / 2 + Y(l1 + 1) - BH / 2) / 2 + off

    def straight(a, b):
        s.path([bot(a), top(b)])

    straight("R01", "R02")
    straight("R02", "R03")
    # bus R03 -> R04, R05
    m = mid(2)
    s.path([bot("R03"), (COL[2], m)], arrow=False)
    s.path([(COL[1], m), (COL[3], m)], arrow=False)
    s.path([(COL[1], m), top("R04")]); s.path([(COL[3], m), top("R05")])
    # bus {R04, R05} -> {R06, R07}
    m = mid(3)
    s.path([bot("R04"), (COL[1], m)], arrow=False)
    s.path([bot("R05"), (COL[3], m)], arrow=False)
    s.path([(COL[1], m), (COL[3], m)], arrow=False)
    s.path([(COL[1], m), top("R06")]); s.path([(COL[2], m), top("R07")])
    straight("R06", "R09")
    straight("R07", "R08")
    # R06 -> R10 via channel between col 1 and col 2
    x0 = bot("R06", 100)[0]
    s.path([bot("R06", 100), (x0, mid(4)), (450, mid(4)), (450, mid(5)),
            (COL[2] - 60, mid(5)), top("R10", -60)])
    s.path([bot("R08"), top("R10")])
    s.path([bot("R08", 70), (COL[2] + 70, mid(5)), (COL[3], mid(5)), top("R11")])
    # R09 -> R12 passes the empty col-1 cell of layer 6
    s.path([bot("R09"), top("R12a")])
    s.path([bot("R10"), (COL[2], mid(6)), (COL[1] + 60, mid(6)), top("R12a", 60)])
    straight("R12a", "R13")
    s.path([bot("R12a", 100), (COL[1] + 100, mid(7)), (COL[2], mid(7)), top("R12b")])

    # sources box (col 1, layers 0-2) with «derive» arrow into R01
    sx, sy0, sy1 = COL[1], Y(0) - BH / 2, Y(2) + BH / 2
    s.add(f'<rect x="{sx-BW/2}" y="{sy0}" width="{BW}" height="{sy1-sy0}" fill="#ffffff" '
          f'stroke="{LINE}" stroke-width="1.6" stroke-dasharray="3,4"/>')
    s.text(sx, sy0 + 26, "Requirement sources", size=18, weight="bold")
    lines = [
        ("Research questions RQ1–RQ4 (Ch 1)", INK),
        ("RQ1 variation across companies and years", ACCENT),
        ("RQ2 adjusted associations", ACCENT),
        ("RQ3 sensitivity of associations", ACCENT),
        ("RQ4 communication through Power BI", ACCENT),
        ("Research gaps G1–G3 (Ch 2)", INK),
        ("Feasibility audit and base-cost decision (Ch 3)", INK),
        ("Supervisor feedback, 3 Oct 2026", INK),
        ("Logbook review of priorities", INK),
    ]
    for i, (t, col) in enumerate(lines):
        s.text(sx - BW / 2 + 18, sy0 + 66 + i * 34, t, size=15, anchor="start", fill=col,
               weight="bold" if col == ACCENT else "normal")
    s.path([(sx + BW / 2, Y(0)), (COL[2] - BW / 2, Y(0))], dashed=True)
    s.text((sx + BW / 2 + COL[2] - BW / 2) / 2, Y(0) - BH / 2 - 16, "«derive»", size=14, style="italic")

    # legend (col 3, layers 7-8)
    lx, ly = COL[3] - BW / 2, Y(7) - BH / 2
    s.add(f'<rect x="{lx}" y="{ly}" width="{BW}" height="{Y(8)+BH/2-ly}" fill="#ffffff" '
          f'stroke="{LINE}" stroke-width="1.2"/>')
    s.text(lx + 16, ly + 26, "How to read", size=17, weight="bold", anchor="start")
    legend = [
        "Arrow A → B: B depends on A, so A is",
        "satisfied first. Joined arrows: every lower",
        "box depends on every upper box.",
        "Transitive links omitted (full list: App. B).",
        "Must / Should / Could / Won't = MoSCoW;",
        "dashed box = excluded by design.",
        "'Realised in' = action IDs in Figure 4.1.",
    ]
    for i, t in enumerate(legend):
        s.text(lx + 16, ly + 60 + i * 26, t, size=15, anchor="start")
    s.save("fig4_2_requirements_traceability.svg", crop_top=62)


if __name__ == "__main__":
    figure_4_1()
    figure_4_2()
    print("SVGs written to", OUT)
