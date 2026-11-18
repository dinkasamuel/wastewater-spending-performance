"""Build Power BI report version 2 from the frozen 16 Nov review version.

Fixes the problems recorded in evaluation/R12a_evaluation_log.md:
  1. plain-language column and slicer labels (removes causal 'effect' label)  [R07, R06]
  2. alt text on every non-text visual                                        [R12a / UI08]
  3. unique keyboard tab order per page (top-to-bottom, left-to-right)       [R12a / UI08]
  4. unit shown for the historical outcome (column + dynamic chart title)    [R10]
  5. source and period context on pages 2 and 3; clusters column on page 3   [R10, R07]
  6. series labels on company line charts so colour is not the only signal   [R12a / UI08]

The v1 source is read only; output goes to powerbi/v2/.
Data paths inside the model still point at the 16 Nov data folder (read only).

Usage (from the project folder):  python code/build_powerbi.py
"""
import json
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "powerbi" / "v1_2026-11-16"
OUT = ROOT / "powerbi" / "v2"
NAME = "Wastewater_Review"

# ------------------------------------------------------------------ labels
DISPLAY = {
    "company_code": "Company",
    "reporting_year": "Reporting year",
    "expenditure_real_m": "Real spending (GBP m, 2017/18 prices)",
    "properties_thousands": "Connected properties (thousands)",
    "expenditure_real_per_property": "Real spending per property (GBP, 2017/18 prices)",
    "sewer_flooding_rate": "Internal flooding (per 10,000 connections)",
    "pollution_rate": "Pollution (per 10,000 km, calendar year)",
    "sewer_collapse_rate": "Sewer collapses (per 1,000 km)",
    "treatment_compliance_pct": "Treatment compliance (%, calendar year, descriptive)",
    # page 3
    "Outcome name": "Outcome",
    "Unit": "Unit",
    "Model specification": "Specification",
    "outcome_release": "Outcome source",
    "n": "Company-years",
    "companies": "Companies (clusters)",
    "effect_10pct": "Rate difference for +10% spending",
    "lower_10pct": "95% interval: lower",
    "upper_10pct": "95% interval: upper",
    "wcr11_p_zero": "Wild-bootstrap p-value",
    # page 4
    "period_basis": "Period basis",
    "period_start": "Measured from",
    "period_end": "Measured to",
    "value": "Value (blank = not available)",
    "source_cell": "Source cell",
    # page 5
    "metric": "Metric",
    "unit": "Unit",
    "better_direction": "Better direction",
    "analytical_role": "Role in analysis",
    "source_item": "Ofwat source item",
}

OUTCOME_SWITCH = ('SWITCH({col}, "sewer_flooding_rate", "Internal sewer flooding", '
                  '"sewer_collapse_rate", "Sewer collapses", "pollution_rate", "Pollution incidents", '
                  '"treatment_compliance_pct", "Treatment works compliance", {col})')
SPEC_SWITCH = ('SWITCH(model_results[specification], '
               '"main", "Main: same year", '
               '"total_plus_size", "Total spending plus size", '
               '"preceding_financial_year", "Spending in preceding financial year", '
               '"same_year_on_lag_sample", "Same year on lag sample (comparison)", '
               '"calendar_same_label", "Same label (calendar outcome)", '
               '"calendar_2021_onward", "Calendar 2021 onward", '
               '"calendar_lag_1", "Lag 1 (overlaps outcome year)", '
               '"calendar_same_label_on_lag_1_sample", "Same label on lag-1 sample", '
               '"calendar_lag_2", "Lag 2 (wholly precedes)", '
               '"calendar_same_label_on_lag_2_sample", "Same label on lag-2 sample", '
               '"outcome_release_sensitivity", "PR24 outcome release", '
               'model_results[specification])')


def calc_column(name, expr, dtype="string"):
    return (f"\tcolumn '{name}' = {expr}\n"
            f"\t\tdataType: {dtype}\n"
            f"\t\tlineageTag: {uuid.uuid4()}\n"
            f"\t\tsummarizeBy: none\n\n")


def measure(name, expr):
    return (f"\tmeasure '{name}' = {expr}\n"
            f"\t\tlineageTag: {uuid.uuid4()}\n\n")


def add_to_table(tmdl_path, block, before="\tpartition "):
    text = tmdl_path.read_text(encoding="utf-8")
    i = text.index(before)
    tmdl_path.write_text(text[:i] + block + text[i:], encoding="utf-8")


# ------------------------------------------------------------------ helpers
def lit(s):
    return {"expr": {"Literal": {"Value": "'" + s.replace("'", "''") + "'"}}}


def column_field(entity, prop):
    return {"field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
            "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}


def projections(visual):
    for role in visual["visual"].get("query", {}).get("queryState", {}).values():
        yield from role.get("projections", [])


def prop_of(p):
    f = p["field"]
    key = "Column" if "Column" in f else "Measure"
    return f[key]["Property"]


def swap_field(p, entity, new_prop):
    p["field"]["Column"]["Property"] = new_prop
    p["queryRef"] = f"{entity}.{new_prop}"
    p["nativeQueryRef"] = new_prop


def set_alt(v, text):
    vco = v["visual"].setdefault("visualContainerObjects", {})
    vco["general"] = [{"properties": {"altText": lit(text)}}]


def set_paragraph(v, index, text):
    paras = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"]
    paras[index]["textRuns"][0]["value"] = text


ALT = {
    ("1 Company trends", "Real expenditure per property"):
        "Line chart of real wastewater network-plus spending per connected property, GBP at 2017/18 prices, one line per company, 2020/21 to 2024/25.",
    ("1 Company trends", "Flooding rate"):
        "Line chart of internal sewer flooding incidents per 10,000 connections, one line per company. Lower is better.",
    ("1 Company trends", "Collapse rate"):
        "Line chart of sewer collapses per 1,000 km of sewer, one line per company. Lower is better.",
    ("1 Company trends", "Pollution rate"):
        "Line chart of pollution incidents per 10,000 km of sewer by calendar year, one line per company. Lower is better.",
    ("2 Audited values", "tableEx"):
        "Table of audited values: one row per company and reporting year, with spending, properties and the four outcomes in their own units.",
    ("3 Adjusted findings", "tableEx"):
        "Table of adjusted associations: rate difference for 10 percent higher spending with 95 percent interval, sample size, clusters and bootstrap p-value for each model.",
    ("4 Historical outcomes", "lineChart"):
        "Line chart of the selected historical outcome by company, 2015/16 to 2024/25. Missing years are left blank.",
    ("4 Historical outcomes", "tableEx"):
        "Table of historical outcome values with measurement period start and end dates and source cell. Blank values are not available.",
    ("5 Definitions and limits", "tableEx"):
        "Table of metric definitions: unit, period basis, direction of better performance, role in the analysis and Ofwat source item.",
}


def alt_for(page, v):
    vt = v["visual"]["visualType"]
    props = [prop_of(p) for p in projections(v)]
    if vt == "slicer":
        label = DISPLAY.get(props[0], props[0]) if props else "value"
        return f"Slicer to filter this page by {label.lower()}."
    for key in ([(page, p) for p in props] + [(page, vt)]):
        if key in ALT:
            return ALT[key]
    return None


# ------------------------------------------------------------------ build
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copy2(SRC / f"{NAME}.pbip", OUT / f"{NAME}.pbip")
    for part in ("Report", "SemanticModel"):
        shutil.copytree(SRC / f"{NAME}.{part}", OUT / f"{NAME}.{part}",
                        ignore=shutil.ignore_patterns("cache.abf"))

    tables = OUT / f"{NAME}.SemanticModel" / "definition" / "tables"
    add_to_table(tables / "model_results.tmdl",
                 calc_column("Outcome name", OUTCOME_SWITCH.format(col="model_results[outcome]"))
                 + calc_column("Unit", "LOOKUPVALUE(metric_dictionary[unit], metric_dictionary[metric], model_results[outcome])")
                 + calc_column("Model specification", SPEC_SWITCH))
    add_to_table(tables / "historical_outcomes.tmdl",
                 calc_column("Outcome name", OUTCOME_SWITCH.format(col="historical_outcomes[metric]"))
                 + calc_column("Unit", "LOOKUPVALUE(metric_dictionary[unit], metric_dictionary[metric], historical_outcomes[metric])"))
    add_to_table(tables / "historical_outcomes.tmdl",
                 measure("Historical chart title",
                         'IF(HASONEVALUE(historical_outcomes[metric]), '
                         'SELECTEDVALUE(historical_outcomes[Outcome name]) & " | " & '
                         'SELECTEDVALUE(historical_outcomes[Unit]) & " | blank = not available", '
                         '"Select exactly one outcome to show its rate and unit")'),
                 before="\tcolumn ")

    pages = OUT / f"{NAME}.Report" / "definition" / "pages"
    log = []
    for pdir in sorted(p for p in pages.iterdir() if p.is_dir()):
        page = json.loads((pdir / "page.json").read_text(encoding="utf-8"))["displayName"]
        visuals = []
        for vf in (pdir / "visuals").glob("*/visual.json"):
            visuals.append((vf, json.loads(vf.read_text(encoding="utf-8"))))

        # 3. unique tab order: top-to-bottom, then left-to-right
        visuals.sort(key=lambda t: (round(t[1]["position"]["y"] / 40), t[1]["position"]["x"]))
        for i, (_, v) in enumerate(visuals):
            v["position"]["tabOrder"] = i

        for vf, v in visuals:
            vt = v["visual"]["visualType"]

            if page == "3 Adjusted findings" and vt in ("tableEx", "slicer"):
                for p in projections(v):
                    if prop_of(p) == "outcome":
                        swap_field(p, "model_results", "Outcome name")
                    elif prop_of(p) == "specification":
                        swap_field(p, "model_results", "Model specification")
                if vt == "tableEx":
                    proj = v["visual"]["query"]["queryState"]["Values"]["projections"]
                    proj.insert(1, column_field("model_results", "Unit"))
                    idx = next(i for i, p in enumerate(proj) if prop_of(p) == "n")
                    proj.insert(idx + 1, column_field("model_results", "companies"))

            if page == "4 Historical outcomes":
                for p in projections(v):
                    if prop_of(p) == "metric":
                        swap_field(p, "historical_outcomes", "Outcome name")
                if vt == "tableEx":
                    proj = v["visual"]["query"]["queryState"]["Values"]["projections"]
                    idx = next(i for i, p in enumerate(proj) if prop_of(p) == "Outcome name")
                    proj.insert(idx + 1, column_field("historical_outcomes", "Unit"))
                if vt == "lineChart":
                    title = v["visual"]["visualContainerObjects"]["title"][0]["properties"]
                    title["text"] = {"expr": {"Measure": {
                        "Expression": {"SourceRef": {"Entity": "historical_outcomes"}},
                        "Property": "Historical chart title"}}}

            if page == "5 Definitions and limits" and vt == "tableEx":
                proj = v["visual"]["query"]["queryState"]["Values"]["projections"]
                proj.append(column_field("metric_dictionary", "source_item"))

            # 1. plain-language labels on every bound column
            for p in projections(v):
                name = prop_of(p)
                if name in DISPLAY and "Column" in p["field"]:
                    p["displayName"] = DISPLAY[name]

            # 6. series labels on company line charts
            if vt == "lineChart":
                v["visual"].setdefault("objects", {})["seriesLabels"] = [
                    {"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]

            # 5. context text
            if vt == "textbox":
                first = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"]
                if first.startswith("Audited values"):
                    set_paragraph(v, 1, "Source: Ofwat WCPR 2024-25 data. One company per reporting year; "
                                        "pollution and compliance use the calendar year in which the label starts.")
                    set_paragraph(v, 2, "Real spending: GBP million, 2017/18 prices. Properties: thousands. "
                                        "Compliance: percent, descriptive only. Rates are not summed.")
                if first.startswith("Adjusted associations"):
                    set_paragraph(v, 1, "Source: WCPR panel, 2020/21-2024/25. Difference in each outcome's own unit "
                                        "for 10% higher real spending per property; approximate 95% CV3 intervals.")

            # 2. alt text
            if vt != "textbox":
                text = alt_for(page, v)
                if text:
                    set_alt(v, text)
                log.append((page, vt, v["position"]["tabOrder"], bool(text)))

            vf.write_text(json.dumps(v, indent=2, ensure_ascii=False), encoding="utf-8")

    missing = [r for r in log if not r[3]]
    print(f"Built {OUT}")
    print(f"non-text visuals: {len(log)}; without alt text: {len(missing)} {missing}")


if __name__ == "__main__":
    build()
