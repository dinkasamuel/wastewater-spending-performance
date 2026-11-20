"""Build Power BI dashboard version 3 (PBIP project) from the analysis outputs.

What v3 adds over v2 (requirements R06, R09, R10, R12a; research question RQ4):
  - data: base spending, balanced panel 2017-18 to 2024-25, read from outputs/powerbi/*.csv;
  - portability: one Power Query parameter, DataFolder, holds the data location, so a
    marker sets a single path (Transform data > Edit parameters) and refreshes;
  - traceability: every page header names the research question, objective and
    requirements it answers (supervisor feedback, 3 Oct 2026);
  - a "what can be detected" page showing the minimum detectable effects;
  - accessibility: alt text on every visual, unique keyboard tab order, plain-language
    labels and units, and series labels on line charts so colour is never the only cue.

The dashboard only displays values computed by code/wastewater_analysis.py; it does not
refit any model. Identifiers are derived from names, so rebuilding gives identical files.

Usage (from the project folder, after running the analysis):
    python code/build_powerbi_v3.py
Then open powerbi/v3/Wastewater_Dashboard.pbip in Power BI Desktop.
"""
import csv
import hashlib
import json
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "powerbi"
OUT = ROOT / "powerbi" / "v3"
NAME = "Wastewater_Dashboard"
THEME_SRC = ROOT / "powerbi" / "v2" / "Wastewater_Review.Report" / "StaticResources"
DEFAULT_FOLDER = str(DATA) + "\\"          # author's path; markers change the parameter
NAVY, GREY = "#17333B", "#36535C"
# Explicit, fixed colour per company on every line chart (theme order), so overriding one colour
# cannot shift the others. United Utilities' theme colour #D9B300 is 2.0:1 on white and fails
# WCAG 1.4.11, so it is replaced by a darker gold #9A7B00 (4.0:1; see check_contrast.py).
COMPANY_COLOURS = {"ANH": "#118DFF", "NES": "#12239E", "SRN": "#E66C37", "SVE": "#6B007B", "SWB": "#E044A7",
                   "TMS": "#744EC2", "UUW": "#9A7B00", "WSX": "#D64550", "YKY": "#197278"}
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric"


def uid(*parts):
    """Stable UUID from a name, so repeated builds produce identical files."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "wastewater-v3/" + "/".join(parts)))


def vid(*parts):
    """Stable 20-character visual/page identifier."""
    return hashlib.md5("/".join(parts).encode()).hexdigest()[:20]


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(content, indent=2, ensure_ascii=False) if isinstance(content, (dict, list)) else content
    path.write_text(text, encoding="utf-8")


# ============================================================ semantic model (TMDL)
MEASURES = {
    "pbi_panel": [
        ("Base spending per property", "AVERAGE(pbi_panel[base_spend_per_property_gbp])", "0.00"),
        ("Flooding rate", "AVERAGE(pbi_panel[sewer_flooding_rate])", "0.00"),
        ("Collapse rate", "AVERAGE(pbi_panel[sewer_collapse_rate])", "0.00"),
        ("Pollution rate", "AVERAGE(pbi_panel[pollution_rate])", "0.00"),
    ],
    "pbi_outcomes_long": [
        ("Selected outcome value",
         "IF(HASONEVALUE(pbi_outcomes_long[outcome]), AVERAGE(pbi_outcomes_long[value]), BLANK())", "0.00"),
        ("Outcome chart title",
         'IF(HASONEVALUE(pbi_outcomes_long[outcome]), SELECTEDVALUE(pbi_outcomes_long[outcome]) & " | " & '
         'SELECTEDVALUE(pbi_outcomes_long[unit]) & " | blank = not available", '
         '"Select exactly one outcome to show its values and unit")', None),
    ],
}


def column_types(table):
    """Infer TMDL/M types from the CSV: integer, decimal or text (blank cells allowed)."""
    with open(DATA / f"{table}.csv", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    types = {}
    for i, col in enumerate(header):
        values = [r[i] for r in body if r[i] != ""]
        def ok(cast):
            try:
                [cast(v) for v in values]
                return bool(values)
            except ValueError:
                return False
        if col in ("year_start", "company_years", "companies", "companies_with_data") and ok(int):
            types[col] = ("int64", "Int64.Type")
        elif ok(float) and col not in ("reporting_year",):
            types[col] = ("double", "type number")
        else:
            types[col] = ("string", "type text")
    return header, types


FORMATS = {"properties": "#,0", "base_spend_per_property_gbp": "#,0.00", "base_spend_gbp_m": "#,0.0",
           "sewer_flooding_rate": "0.00", "sewer_collapse_rate": "0.00", "pollution_rate": "0.00",
           "treatment_compliance_pct": "0.00", "value": "0.00", "average_rate": "0.00",
           "detectable_pct_of_average": "0", "p_wild_bootstrap": "0.000", "p_holm_main": "0.000"}


def table_tmdl(table):
    header, types = column_types(table)
    lines = [f"table {table}", f"\tlineageTag: {uid(table)}", ""]
    for name, expr, fmt in MEASURES.get(table, []):
        lines.append(f"\tmeasure '{name}' = {expr}")
        if fmt:
            lines.append(f"\t\tformatString: {fmt}")
        lines += [f"\t\tlineageTag: {uid(table, 'measure', name)}", ""]
    for col in header:
        dtype = types[col][0]
        lines += [f"\tcolumn {col}", f"\t\tdataType: {dtype}"]
        if dtype == "double":
            lines.append(f"\t\tformatString: {FORMATS.get(col, '0.000')}")
        lines += [f"\t\tlineageTag: {uid(table, col)}", "\t\tsummarizeBy: none",
                  f"\t\tsourceColumn: {col}", "", "\t\tannotation SummarizationSetBy = User", ""]
    typed = ", ".join(f'{{"{c}", {types[c][1]}}}' for c in header)
    lines += [
        f"\tpartition {table} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "{table}.csv"),'
        f'[Delimiter=",", Columns={len(header)}, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        "\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
        '\t\t\t\t    Blanks = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),',
        f'\t\t\t\t    Typed = Table.TransformColumnTypes(Blanks, {{{typed}}}, "en-GB")',
        "\t\t\t\tin", "\t\t\t\t    Typed", "", "\tannotation PBI_ResultType = Table", ""]
    return "\n".join(lines), set(header) | {m[0] for m in MEASURES.get(table, [])}


TABLES = ["pbi_panel", "pbi_outcomes_long", "pbi_models", "pbi_detectability", "pbi_coverage", "pbi_dictionary"]


def build_model():
    sm = OUT / f"{NAME}.SemanticModel"
    fields = {}
    for t in TABLES:
        text, names = table_tmdl(t)
        write(sm / "definition" / "tables" / f"{t}.tmdl", text)
        fields[t] = names
    write(sm / "definition" / "expressions.tmdl", "\n".join([
        f'expression DataFolder = "{DEFAULT_FOLDER}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]',
        f"\tlineageTag: {uid('DataFolder')}", "", "\tannotation PBI_ResultType = Text", ""]))
    write(sm / "definition" / "model.tmdl", "\n".join([
        "model Model", "\tculture: en-GB", "\tdefaultPowerBIDataSourceVersion: powerBI_V3",
        "\tsourceQueryCulture: en-GB", "\tdataAccessOptions", "\t\tlegacyRedirects", "\t\treturnErrorValuesAsNull", "",
        "annotation __PBI_TimeIntelligenceEnabled = 0", "",
        "annotation PBI_QueryOrder = " + json.dumps(["DataFolder"] + TABLES), "",
        "annotation PBI_ProTooling = [\"DevMode\"]", ""] + [f"ref table {t}" for t in TABLES] + [""]))
    write(sm / "definition" / "database.tmdl", "database\n\tcompatibilityLevel: 1606\n")
    write(sm / "definition.pbism", {"version": "4.2", "settings": {}})
    write(sm / ".platform", {"$schema": f"{SCHEMA}/gitIntegration/platformProperties/2.0.0/schema.json",
                             "metadata": {"type": "SemanticModel", "displayName": NAME},
                             "config": {"version": "2.0", "logicalId": uid("semanticmodel")}})
    return fields


# ============================================================ report (PBIR JSON)
def lit(value):
    return {"expr": {"Literal": {"Value": value}}}


def text_lit(s):
    return lit("'" + s.replace("'", "''") + "'")


def field(table, prop, measure=False, display=None):
    kind = "Measure" if measure else "Column"
    p = {"field": {kind: {"Expression": {"SourceRef": {"Entity": table}}, "Property": prop}},
         "queryRef": f"{table}.{prop}", "nativeQueryRef": prop}
    if display:
        p["displayName"] = display
    return p


def container(page, key, x, y, w, h, tab, visual):
    return {"$schema": f"{SCHEMA}/item/report/definition/visualContainer/2.14.0/schema.json",
            "name": vid(page, key), "position": {"x": x, "y": y, "z": tab, "width": w, "height": h, "tabOrder": tab},
            "visual": visual}


def decorate(visual, title=None, alt=None):
    vco = visual.setdefault("visualContainerObjects", {})
    if title is not None:
        vco["title"] = [{"properties": {"show": lit("true"), "text": title if isinstance(title, dict) else text_lit(title),
                                        "fontSize": lit("12D")}}]
    if alt:
        vco["general"] = [{"properties": {"altText": text_lit(alt)}}]
    visual["drillFilterOtherVisuals"] = True
    return visual


def textbox(lines):
    """lines: list of (text, size_px, bold, colour)."""
    paragraphs = [{"textRuns": [{"value": t, "textStyle": {"fontFamily": "Segoe UI", "fontSize": f"{s}px",
                                                           **({"fontWeight": "bold"} if b else {}), "color": c}}]}
                  for t, s, b, c in lines]
    return {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": paragraphs}}]},
            "drillFilterOtherVisuals": True}


def header(title, tags, context):
    return textbox([(title, 24, True, NAVY), (tags, 15, True, "#1F5F8B"), (context, 14, False, GREY)])


def slicer(table, column, display):
    return decorate({"visualType": "slicer",
                     "query": {"queryState": {"Values": {"projections": [field(table, column, display=display) | {"active": True}]}}},
                     "objects": {"data": [{"properties": {"mode": text_lit("Basic")}}]}},
                    alt=f"Slicer to filter this page by {display.lower()}.")


def table_visual(table, columns, title, alt, sort_by=None):
    query = {"queryState": {"Values": {"projections": [field(table, c, display=d) for c, d in columns]}}}
    if sort_by:
        query["sortDefinition"] = {"sort": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": table}},
                                                                  "Property": sort_by}}, "direction": "Ascending"}]}
    style = [{"properties": {"wordWrap": lit("true"), "fontSize": lit("11D")}}]
    return decorate({"visualType": "tableEx", "query": query,
                     "objects": {"values": style, "columnHeaders": style}}, title=title, alt=alt)


def line_chart(table, measure, title, alt, series="company_code", series_name="Company"):
    sort = {"sort": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": "reporting_year"}},
                      "direction": "Ascending"}]}
    visual = {"visualType": "lineChart",
              "query": {"queryState": {
                  "Category": {"projections": [field(table, "reporting_year", display="Reporting year") | {"active": True}]},
                  "Series": {"projections": [field(table, series, display=series_name)]},
                  "Y": {"projections": [field(table, measure, measure=True)]}},
                  "sortDefinition": sort},
              "objects": {"seriesLabels": [{"properties": {"show": lit("true")}}],
                          "dataPoint": [{
                              "properties": {"fill": {"solid": {"color": text_lit(colour)}}},
                              "selector": {"data": [{"scopeId": {"Comparison": {
                                  "ComparisonKind": 0,
                                  "Left": {"Column": {"Expression": {"SourceRef": {"Entity": table}},
                                                      "Property": series}},
                                  "Right": {"Literal": {"Value": f"'{code}'"}}}}}]}}
                              for code, colour in COMPANY_COLOURS.items()],
                          "lineStyles": [{"properties": {"lineChartType": text_lit("linear"),
                                                         "showMarker": lit("true")}}]}}
    visual = decorate(visual, title=title, alt=alt)
    visual["visualContainerObjects"]["subTitle"] = [{"properties": {"show": lit("false")}}]
    return visual


PAGES = []      # (page_id, display_name, [(key, x, y, w, h, visual)])


def page(name, items):
    PAGES.append((vid("page", name), name, items))


SRC_NOTE = "Source: Ofwat PR24 base-cost data (CA06, Oct 2025) and PR24 historical performance trends V6.0 (Jan 2026)."
page("1 Trends", [
    ("header", 20, 10, 1240, 92, header(
        "How spending and outcomes changed, 2017-18 to 2024-25",
        "Answers RQ1  ·  Objective 2  ·  Requirements R06, R09",
        "Base spending per connected property in 2022-23 prices; outcomes in their own units. Flooding, collapses and "
        "pollution: lower is better. Pollution is measured by calendar year. " + SRC_NOTE)),
    ("company", 20, 112, 170, 290, slicer("pbi_panel", "company_label", "Company")),
    ("year", 20, 412, 170, 290, slicer("pbi_panel", "reporting_year", "Reporting year")),
    ("spend", 205, 112, 525, 290, line_chart("pbi_panel", "Base spending per property",
        "Base spending per property | GBP, 2022-23 prices",
        "Line chart of base spending per connected property for each company, 2017-18 to 2024-25, GBP at 2022-23 prices.")),
    ("flood", 740, 112, 520, 290, line_chart("pbi_panel", "Flooding rate",
        "Internal sewer flooding | per 10,000 connections | lower is better",
        "Line chart of internal sewer flooding incidents per 10,000 connections for each company. Lower is better.")),
    ("collapse", 205, 412, 525, 290, line_chart("pbi_panel", "Collapse rate",
        "Sewer collapses | per 1,000 km of sewer | lower is better",
        "Line chart of sewer collapses per 1,000 km of sewer for each company. Lower is better.")),
    ("pollution", 740, 412, 520, 290, line_chart("pbi_panel", "Pollution rate",
        "Pollution incidents | per 10,000 km of sewer | calendar year | lower is better",
        "Line chart of pollution incidents per 10,000 km of sewer by calendar year for each company. Lower is better.")),
])
page("2 Values", [
    ("header", 20, 10, 1240, 92, header(
        "Audited values: one row per company and reporting year",
        "Answers RQ1  ·  Objective 1  ·  Requirements R03, R04, R09",
        "Values are exactly those used in the analysis (72 company-years). Rates are never summed. " + SRC_NOTE)),
    ("company", 20, 112, 170, 290, slicer("pbi_panel", "company_label", "Company")),
    ("year", 20, 412, 170, 290, slicer("pbi_panel", "reporting_year", "Reporting year")),
    ("table", 205, 112, 1055, 590, table_visual("pbi_panel", [
        ("company_label", "Company"), ("reporting_year", "Reporting year"),
        ("base_spend_per_property_gbp", "Base spending per property (GBP, 2022-23 prices)"),
        ("base_spend_gbp_m", "Base spending (GBP m, 2022-23 prices)"),
        ("properties", "Connected properties"),
        ("sewer_flooding_rate", "Internal flooding (per 10,000 connections)"),
        ("sewer_collapse_rate", "Sewer collapses (per 1,000 km)"),
        ("pollution_rate", "Pollution (per 10,000 km, calendar year)"),
        ("treatment_compliance_pct", "Treatment compliance (%, calendar year, descriptive)")],
        "Company-year values used in the analysis",
        "Table of the 72 company-years in the analysis with base spending, connected properties and four outcomes in their own units.")),
])
page("3 Associations", [
    ("header", 20, 10, 1240, 92, header(
        "Is more spending associated with fewer problems?",
        "Answers RQ2 (main models) and RQ3 (sensitivity)  ·  Objectives 3-4  ·  Requirements R07, R08, R10",
        "Difference in each outcome, in its own unit, for 10% more base spending per property, comparing each company "
        "with itself and allowing for shared yearly conditions. 95% ranges use nine company clusters (CV3).")),
    ("outcome", 20, 112, 200, 200, slicer("pbi_models", "outcome", "Outcome")),
    ("role", 20, 322, 200, 200, slicer("pbi_models", "role", "Type of result")),
    ("table", 235, 112, 1025, 420, table_visual("pbi_models", [
        ("outcome", "Outcome"), ("specification", "Specification"), ("role", "Type"), ("years", "Years"),
        ("company_years", "Company-years"), ("companies", "Companies"),
        ("difference_per_10pct", "Difference for +10% spending"), ("ci95_low", "95% range: low"),
        ("ci95_high", "95% range: high"), ("range_includes_zero", "Range includes zero?"),
        ("p_wild_bootstrap", "Wild-bootstrap p-value"),
        ("detectable_difference_80pct", "Smallest detectable difference")],
        "Model results, main models first (stored values; filters do not refit any model)",
        "Table of model results: difference in each outcome for 10 percent more spending, 95 percent range, p-value and smallest detectable difference.",
        sort_by="role")),
    ("note", 235, 542, 1025, 160, textbox([
        ("How to read this page", 15, True, NAVY),
        ("A range that includes zero means the data cannot tell whether the link is positive, negative or absent. "
         "It is not proof of no link.", 13, False, GREY),
        ("These are associations, not causal effects: spending can respond to failures as well as prevent them.", 13, False, GREY),
        ("Main models: no clear association for flooding, collapses or pollution over 2017-18 to 2024-25.", 13, True, GREY)])),
])
page("4 What can be detected", [
    ("header", 20, 10, 1240, 92, header(
        "How large would a link have to be for nine companies to reveal it?",
        "Answers RQ2-RQ4  ·  Objectives 3-5  ·  Requirements R07, R10",
        "Smallest difference per 10% more spending that the main model would detect with 80% probability "
        "(minimum detectable effect).")),
    ("table", 20, 112, 1240, 185, table_visual("pbi_detectability", [
        ("outcome", "Outcome"), ("unit", "Unit"), ("average_rate", "Average rate"),
        ("difference_per_10pct", "Estimated difference"), ("ci95_low", "95% range: low"), ("ci95_high", "95% range: high"),
        ("detectable_difference_80pct", "Smallest detectable difference"),
        ("detectable_pct_of_average", "As % of average rate")],
        "Main models: estimate and detectable size",
        "Table of the three main models showing the estimated difference, its 95 percent range and the smallest difference the data could reliably detect.")),
    ("plain", 20, 305, 1240, 190, table_visual("pbi_detectability", [
        ("outcome", "Outcome"), ("plain_message", "What this means in plain words")],
        "In plain words",
        "Table giving a plain-language sentence for each main model about the size of link the data could detect.")),
    ("note", 20, 505, 1240, 197, textbox([
        ("Why this matters", 15, True, NAVY),
        ("With only nine companies, any real link smaller than about a fifth of the average rate per 10% more spending "
         "would usually go unnoticed.", 13, False, GREY),
        ("So 'no clear link' here means 'no large link', not 'spending makes no difference'.", 13, True, GREY),
        ("Comparing more years or more companies would be needed to detect smaller links.", 13, False, GREY)])),
])
page("5 History and coverage", [
    ("header", 20, 10, 1240, 92, header(
        "Outcome history 2015-16 to 2024-25 and data coverage",
        "Answers RQ1  ·  Objective 1  ·  Requirements R05, R06",
        "Select exactly one outcome. Missing values stay blank and are never shown as zero. The main analysis uses "
        "2017-18 to 2024-25, the years in which every company reports every outcome.")),
    ("outcome", 20, 112, 200, 200, slicer("pbi_outcomes_long", "outcome", "Outcome")),
    ("company", 20, 322, 200, 380, slicer("pbi_outcomes_long", "company_label", "Company")),
    ("chart", 235, 112, 600, 330, line_chart("pbi_outcomes_long", "Selected outcome value",
        {"expr": {"Measure": {"Expression": {"SourceRef": {"Entity": "pbi_outcomes_long"}},
                              "Property": "Outcome chart title"}}},
        "Line chart of the selected outcome for each company, 2015-16 to 2024-25. Missing years are left blank.")),
    ("coverage", 845, 112, 415, 330, table_visual("pbi_coverage", [
        ("outcome", "Outcome"), ("reporting_year", "Year"), ("companies_with_data", "Companies (of 9)")],
        "Data coverage by outcome and year",
        "Table showing how many of the nine companies have data for each outcome in each year.")),
    ("table", 235, 452, 1025, 250, table_visual("pbi_outcomes_long", [
        ("company_label", "Company"), ("reporting_year", "Reporting year"), ("outcome", "Outcome"), ("unit", "Unit"),
        ("period_basis", "Period basis"), ("value", "Value"), ("available", "Available?"),
        ("in_main_window", "In main analysis?")],
        "Outcome values with period and availability",
        "Table of outcome values with unit, period basis, availability and whether the year is in the main analysis.")),
])
page("6 Definitions and limits", [
    ("header", 20, 10, 1240, 92, header(
        "Definitions, sources and limits",
        "Answers RQ4  ·  Objective 5  ·  Requirements R02, R10",
        "Everything shown in this dashboard comes from public Ofwat data processed by the project's Python code; "
        "the dashboard displays results and never recalculates them.")),
    ("table", 20, 108, 1240, 272, table_visual("pbi_dictionary", [
        ("measure", "Measure"), ("unit", "Unit"), ("better_direction", "Better direction"), ("period", "Period"),
        ("role", "Role")],
        "What each measure means",
        "Table defining each measure: unit, direction of better performance, period and role in the analysis.")),
    ("sources", 20, 386, 1240, 252, table_visual("pbi_dictionary", [
        ("measure", "Measure"), ("source", "Source")],
        "Where each measure comes from",
        "Table giving the Ofwat source for each measure.")),
    ("note", 20, 644, 1240, 72, textbox([
        ("Limits: associations, not causes; nine companies limit precision (page 4). Base spending excludes enhancement; "
         "totex includes it and is consistent only from 2020-21.", 13, False, GREY),
        ("Compliance is descriptive only. No ranking or forecast (R14). Severn Trent spending includes Hafren Dyfrdwy (about 1%).",
         13, False, GREY)])),
])


def build_report():
    rp = OUT / f"{NAME}.Report"
    write(rp / "definition.pbir", {"version": "4.0", "datasetReference": {"byPath": {"path": f"../{NAME}.SemanticModel"}}})
    write(rp / ".platform", {"$schema": f"{SCHEMA}/gitIntegration/platformProperties/2.0.0/schema.json",
                             "metadata": {"type": "Report", "displayName": NAME},
                             "config": {"version": "2.0", "logicalId": uid("report")}})
    shutil.copytree(THEME_SRC, rp / "StaticResources", dirs_exist_ok=True)
    report = json.loads((ROOT / "powerbi/v2/Wastewater_Review.Report/definition/report.json").read_text(encoding="utf-8"))
    write(rp / "definition" / "report.json", report)
    write(rp / "definition" / "version.json", {"$schema": f"{SCHEMA}/item/report/definition/versionMetadata/1.0.0/schema.json",
                                               "version": "2.0.0"})
    write(rp / "definition" / "pages" / "pages.json", {
        "$schema": f"{SCHEMA}/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [p[0] for p in PAGES], "activePageName": PAGES[0][0]})
    used = []
    for pid, pname, items in PAGES:
        write(rp / "definition" / "pages" / pid / "page.json", {
            "$schema": f"{SCHEMA}/item/report/definition/page/2.1.0/schema.json",
            "name": pid, "displayName": pname, "displayOption": "FitToPage", "height": 720, "width": 1280})
        for i, (key, x, y, w, h, visual) in enumerate(items):
            # Power BI visits the highest tabOrder first (verified in Desktop's Selection pane,
            # 18 Nov 2026), so reading order top-to-bottom gets descending numbers.
            c = container(pname, key, x, y, w, h, len(items) - 1 - i, visual)
            write(rp / "definition" / "pages" / pid / "visuals" / c["name"] / "visual.json", c)
            used.append((pname, key, visual))
    return used


def static_checks(fields, used):
    """Every bound field exists; every non-text visual has alt text and a title; tab order is unique."""
    problems = []
    for pname, key, visual in used:
        for role in visual.get("query", {}).get("queryState", {}).values():
            for p in role["projections"]:
                kind = "Measure" if "Measure" in p["field"] else "Column"
                ent = p["field"][kind]["Expression"]["SourceRef"]["Entity"]
                prop = p["field"][kind]["Property"]
                if prop not in fields.get(ent, set()):
                    problems.append(f"{pname}/{key}: unknown field {ent}.{prop}")
        if visual["visualType"] != "textbox":
            vco = visual.get("visualContainerObjects", {})
            if "general" not in vco:
                problems.append(f"{pname}/{key}: no alt text")
            if "title" not in vco and visual["visualType"] != "slicer":
                problems.append(f"{pname}/{key}: no title")
    return problems


if __name__ == "__main__":
    if OUT.exists():                       # clear old files; empty folders locked by Windows may remain
        for f in sorted(OUT.rglob("*"), reverse=True):
            if f.is_file() and f.suffix != ".pbix":     # keep the saved .pbix copy
                f.unlink()
            else:
                try:
                    f.rmdir()
                except OSError:
                    pass
    fields = build_model()
    used = build_report()
    write(OUT / f"{NAME}.pbip", {"version": "1.0", "artifacts": [{"report": {"path": f"{NAME}.Report"}}],
                                 "settings": {"enableAutoRecovery": True}})
    problems = static_checks(fields, used)
    visuals = [u for u in used if u[2]["visualType"] != "textbox"]
    print(f"Built {OUT.relative_to(ROOT)}: {len(PAGES)} pages, {len(used)} visuals ({len(visuals)} data visuals)")
    print("Static checks:", "all passed" if not problems else problems)
    raise SystemExit(1 if problems else 0)
