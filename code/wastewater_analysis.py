"""Wastewater base spending and operational performance: full reproducible analysis.

Research questions (Chapter 1)
    RQ1  How do spending and outcomes vary across the nine companies and over time?
    RQ2  What associations exist between spending and each outcome, after allowing for
         company scale, permanent company differences and shared yearly conditions?
    RQ3  How sensitive are these associations to the spending measure, influential
         companies and timing?
    (RQ4, communication through Power BI, is evaluated separately.)

Run from the project folder:   python code/wastewater_analysis.py
Inputs : data/raw/   (unchanged Ofwat files; SHA-256 recorded before and after the run)
Outputs: outputs/ (CSV + run_manifest.json) and figures/ (PNG)

The file is split into "# %%" cells, so it can be run cell by cell in VS Code or Spyder.
Each cell that produces a result is followed by an INSIGHT comment. The insights were
written from the run of 18 Nov 2026 and must be re-checked if any input file changes.

Author: Dinka Christabel Samuel, MSc Data Science, UWE Bristol.
Written with AI assistance (see the AI-use disclosure in Appendix A).
"""

# %% 0. Setup ---------------------------------------------------------------------------
import hashlib
import json
import math
import platform
import sys
from datetime import date
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # draw to files, no screen needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
import methods as m                        # statistical functions (code/methods.py)

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT, FIG = ROOT / "data" / "raw", ROOT / "outputs", ROOT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

FILES = {
    "base_costs": RAW / "PR24CA06-WW1-FD.xlsx",
    "base_costs_dec2024": RAW / "PR24-FD-CA08-Base-costs-wastewater-model-3-Network-Plus.xlsx",
    "wcpr": RAW / "WCPR_2024-25-Open-Data-Machine-Readable-Normalised-PostFDUpdate.xlsx",
    "wcpr_companion": RAW / "WCPR-data-report-2024-25-external-V0.2-Final.xlsx",
    "pr24_outcomes": RAW / "Historical-performance-trends-for-PR24-V6.0.xlsx",
}

# The nine water and sewerage companies serving England (Environment Agency, 2025a).
COMPANIES = {"ANH": "Anglian Water", "NES": "Northumbrian Water", "SVE": "Severn Trent Water",
             "SRN": "Southern Water", "SWB": "South West Water", "TMS": "Thames Water",
             "UUW": "United Utilities", "WSX": "Wessex Water", "YKY": "Yorkshire Water"}
# Ofwat cost-assessment codes -> WCPR codes. SVH = Severn Trent England + Hafren Dyfrdwy
# (Wales), the only Severn Trent series with properties for every year; see BOUNDARY note.
COST_CODE = {"NWT": "UUW", "SVH": "SVE"}
OUTCOMES = {"sewer_flooding_rate": "incidents per 10,000 connections",
            "sewer_collapse_rate": "collapses per 1,000 km of sewer",
            "pollution_rate": "incidents per 10,000 km of sewer (calendar year)",
            "treatment_compliance_pct": "% of works compliant (calendar year)"}
MODELLED = ["sewer_flooding_rate", "sewer_collapse_rate", "pollution_rate"]   # compliance: descriptive only
BALANCED_YEARS = range(2017, 2025)       # 2017/18-2024/25: every company has every outcome
LAST_ACTUAL_COST_YEAR = 2024             # 2025/26 onwards in the Ofwat file are forecasts

CHECKS = []


def label(year):
    """2017 -> '2017-18' (Ofwat reporting-year label)."""
    return f"{year}-{str(year + 1)[-2:]}"


def check(test_id, passed, detail):
    """Record every validation result; stop the run on the first failure (R03, R11)."""
    CHECKS.append({"test_id": test_id, "passed": bool(passed), "detail": detail})
    if not passed:
        pd.DataFrame(CHECKS).to_csv(OUT / "validation_checks.csv", index=False)
        raise AssertionError(f"{test_id}: {detail}")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


input_hashes_before = {k: sha256(p) for k, p in FILES.items()}
check("T00_methods", m.self_tests(), "Known slope, demeaning, 512-draw bootstrap and Holm self-tests pass")
print("Setup complete; method self-tests passed.")


# %% 1. Base spending (Ofwat PR24 datasets CA06 and CA08) -- R01, R02, R04 ------------
# Main source: CA06 'WW1' dataset republished by Ofwat in October 2025 for the CMA appeals.
# Sheet 'F_Outputs_prep' holds, per company and year, modelled base costs for wastewater
# network plus (GBP million, 2022-23 prices) and connected properties (number). It
# contains the actual 2024-25 figures that companies reported in July 2025.
wb = load_workbook(FILES["base_costs"], read_only=True, data_only=True)
rows = list(wb["F_Outputs_prep"].iter_rows(values_only=True))
wb.close()
names = list(rows[1])                                   # second row holds readable names
base = pd.DataFrame([r for r in rows[2:] if r[1]], columns=names)[
    ["companycode", "financial year", "modelledbase_wwnp", "properties"]]
base.columns = ["cost_code", "reporting_year", "base_cost_m_2223", "properties"]
base[["base_cost_m_2223", "properties"]] = base[["base_cost_m_2223", "properties"]].astype(float)

# Validation source: CA08 (December 2024 final determinations). Its actual years must
# equal CA06 exactly; otherwise the two files would not share one definition.
wb = load_workbook(FILES["base_costs_dec2024"], read_only=True, data_only=True)
rows = list(wb["Costs"].iter_rows(values_only=True))
wb.close()
h = next(i for i, r in enumerate(rows) if r[0] == "Codecombine")
ca08 = pd.DataFrame([(r[1], r[2], r[5]) for r in rows[h + 1:] if r[1]],
                    columns=["cost_code", "reporting_year", "ca08_m"])
both = base.merge(ca08, on=["cost_code", "reporting_year"])
both = both[both.reporting_year.str[:4].astype(int).between(2011, 2023)]
check("T01b_same_definition", np.allclose(both.base_cost_m_2223, both.ca08_m.astype(float), atol=1e-9),
      f"CA06 equals CA08 for all {len(both)} company-years 2011-12 to 2023-24 (one definition)")

base["company_code"] = base.cost_code.replace(COST_CODE)
base["year_start"] = base.reporting_year.str[:4].astype(int)
base = base[base.company_code.isin(COMPANIES) & (base.cost_code != "SVE")]   # use SVH for Severn Trent
base["is_forecast"] = base.year_start > LAST_ACTUAL_COST_YEAR
actual = base[~base.is_forecast & base.year_start.ge(2011)].copy()
actual["base_cost_per_property"] = actual.base_cost_m_2223 * 1e6 / actual.properties   # GBP, 2022-23 prices

check("T01_base_grid", len(actual) == 9 * 14 and not actual.duplicated(["company_code", "year_start"]).any(),
      f"{len(actual)} company-years = 9 companies x 14 actual years (2011-12 to 2024-25)")
check("T02_base_positive", (actual[["base_cost_m_2223", "properties"]] > 0).all().all(),
      "All actual base costs and property counts are positive (needed for logs)")
actual.to_csv(OUT / "base_costs_actual.csv", index=False)
print(actual.groupby("year_start").base_cost_per_property.agg(["mean", "min", "max"]).round(1))

# INSIGHT: Ofwat's CA06 dataset gives one consistent definition of base spending for all
# nine companies from 2011-12 to 2024-25 (126 company-years, no gaps). For 2011-12 to
# 2023-24 it is identical to the December 2024 file (CA08), and it adds the actual 2024-25
# figures. Values from 2025-26 onwards are Ofwat forecasts and are deliberately excluded.


# %% 2. WCPR 2024-25 baseline: total spending, properties, outcomes -- R02, R03 ---------
WCPR_ITEMS = {"B0143TAWWNP 17-18prices": "totex_m_1718", "BN2710": "properties_thousands",
              "APR3B_01": "sewer_flooding_rate", "APR3B_02": "pollution_rate",
              "APR3B_03": "sewer_collapse_rate", "APR3B_04": "treatment_compliance_pct"}
raw = pd.read_excel(FILES["wcpr"], sheet_name="in")
raw = raw[raw.COMPANY_ABBREVIATION.isin(COMPANIES)
          & raw.YEAR.isin([label(y) for y in range(2020, 2025)])
          & raw.UNIQUE_ITEM_REFERENCE.isin(WCPR_ITEMS)].copy()
raw["value"] = pd.to_numeric(raw.VALUE, errors="coerce")
check("T03_wcpr_grid", len(raw) == 9 * 5 * len(WCPR_ITEMS) and raw.value.notna().all(),
      f"{len(raw)} WCPR values = 9 companies x 5 years x {len(WCPR_ITEMS)} items, none missing")

# Cross-check every selected value against Ofwat's companion workbook.
grid = pd.read_excel(FILES["wcpr_companion"], sheet_name="Data", header=None)
h = next(i for i, r in grid.head(50).iterrows()
         if {"Company abb", "Unique Item Ref", "Year", "Value"} <= set(r.dropna().astype(str)))
companion = grid.iloc[h + 1:].set_axis(grid.iloc[h].tolist(), axis=1)
companion = companion.rename(columns={"Company abb": "COMPANY_ABBREVIATION", "Year": "YEAR",
                                      "Unique Item Ref": "UNIQUE_ITEM_REFERENCE"})
keys = ["COMPANY_ABBREVIATION", "YEAR", "UNIQUE_ITEM_REFERENCE"]
both = raw.merge(companion[keys + ["Value"]], on=keys, how="left", validate="one_to_one")
check("T04_companion", np.allclose(both.value, pd.to_numeric(both.Value), rtol=1e-9, atol=1e-7),
      "Every selected WCPR value equals the companion workbook value")

wcpr = (raw.assign(item=raw.UNIQUE_ITEM_REFERENCE.map(WCPR_ITEMS))
        .pivot(index=["COMPANY_ABBREVIATION", "YEAR"], columns="item", values="value")
        .reset_index().rename(columns={"COMPANY_ABBREVIATION": "company_code", "YEAR": "reporting_year"}))
wcpr["year_start"] = wcpr.reporting_year.str[:4].astype(int)
wcpr["totex_per_property"] = wcpr.totex_m_1718 * 1000 / wcpr.properties_thousands   # GBP, 2017-18 prices
wcpr.to_csv(OUT / "wcpr_baseline_2020_2025.csv", index=False)

# Do Ofwat's two sources agree on connected properties? (scale measure, R04)
cross = actual.merge(wcpr[["company_code", "year_start", "properties_thousands"]],
                     on=["company_code", "year_start"])
cross["difference_pct"] = 100 * (cross.properties - cross.properties_thousands * 1000) / (cross.properties_thousands * 1000)
cross[["company_code", "reporting_year", "properties", "properties_thousands", "difference_pct"]].to_csv(
    OUT / "property_crosscheck.csv", index=False)
exact = cross.groupby("company_code").difference_pct.apply(lambda s: s.abs().max() < 1e-6)
check("T05_properties", exact.sum() >= 7 and set(exact[~exact].index) <= {"SVE", "SWB"},
      f"Properties identical for {int(exact.sum())} of 9 companies; differences only for {sorted(exact[~exact].index)}")
print(cross.groupby("company_code").difference_pct.agg(["min", "max"]).round(2))

# INSIGHT: The cost file and the performance report agree exactly on connected properties
# for seven companies in 2020-21 to 2024-25. Severn Trent is +0.5% to +1.9% higher because
# the cost series includes Hafren Dyfrdwy (Wales); South West Water differs by up to about
# -2% in 2020-21 and 2021-22 only. Both are boundary differences, documented as limits.


# %% 3. PR24 historical outcomes, 2015-16 to 2024-25 -- R01, R05 ----------------------
PR24_CODES = {"OUT5_01_PR24_OFWAT": "sewer_flooding_rate", "OUT5_05_PR24_OFWAT": "pollution_rate",
              "OUT5_11_PR24_OFWAT": "sewer_collapse_rate", "OUT4_19_PR24_OFWAT": "treatment_compliance_pct"}
wb = load_workbook(FILES["pr24_outcomes"], read_only=True, data_only=True)
rows = wb["Final data post overrides"].iter_rows(max_col=80, values_only=True)
for _ in range(4):
    head = next(rows)
year_col = {y: head.index(label(y)) for y in range(2015, 2025)}
records = []
for row in rows:
    if row[1] in COMPANIES and row[3] == "England" and str(row[4]).strip() == "Company" and row[5] in PR24_CODES:
        metric = PR24_CODES[row[5]]
        for y, col in year_col.items():
            v = row[col]
            ok = isinstance(v, (int, float)) and math.isfinite(v)
            records.append({"company_code": row[1], "year_start": y, "metric": metric,
                            "value": (v * 100 if metric == "treatment_compliance_pct" else v) if ok else np.nan,
                            "period_basis": "calendar" if row[15] == "Calendar year" else "financial"})
wb.close()
outcomes_long = pd.DataFrame(records)
check("T06_pr24_grid", len(outcomes_long) == 9 * 10 * 4 and not outcomes_long.duplicated(
    ["company_code", "year_start", "metric"]).any(), "Unique 9 companies x 10 years x 4 outcomes grid")
outcomes_long.to_csv(OUT / "pr24_outcomes_long.csv", index=False)

coverage = outcomes_long.pivot_table(index="metric", columns="year_start", values="value",
                                     aggfunc=lambda s: s.notna().sum())
coverage.to_csv(OUT / "outcome_coverage.csv")
print(coverage)

# INSIGHT: Outcome records are complete for all nine companies from 2017-18 (flooding from
# 2016-17). Earlier years are patchy (e.g. collapses 2 of 9 in 2015-16), so the main
# analysis uses the balanced window 2017-18 to 2024-25; missing values are never filled in.


# %% 4. Build the analysis panels -- R03, R04, R05 --------------------------------------
outcomes_wide = outcomes_long.pivot(index=["company_code", "year_start"], columns="metric",
                                    values="value").reset_index()
panel = outcomes_wide.merge(actual[["company_code", "year_start", "base_cost_m_2223", "properties",
                                    "base_cost_per_property"]], on=["company_code", "year_start"],
                            how="left", validate="one_to_one")
panel["reporting_year"] = panel.year_start.map(label)
panel["log_spend_pp"] = np.log(panel.base_cost_per_property)
panel["log_spend_total"] = np.log(panel.base_cost_m_2223)
panel["log_properties"] = np.log(panel.properties)

# Lagged spending: last year's (lag 1) and the year before (lag 2). Base spending exists
# back to 2011-12, so lags do not shorten the outcome window.
for lag in (1, 2):
    prior = actual[["company_code", "year_start", "base_cost_per_property"]].copy()
    prior["year_start"] += lag
    panel = panel.merge(prior.rename(columns={"base_cost_per_property": f"spend_pp_lag{lag}"}),
                        on=["company_code", "year_start"], how="left", validate="one_to_one")
    panel[f"log_spend_pp_lag{lag}"] = np.log(panel[f"spend_pp_lag{lag}"])
panel["company_name"] = panel.company_code.map(COMPANIES)

balanced = panel[panel.year_start.isin(BALANCED_YEARS)].copy()
check("T07_balanced", len(balanced) == 72 and balanced[MODELLED + ["log_spend_pp", "log_spend_pp_lag1",
                                                                    "log_spend_pp_lag2"]].notna().all().all(),
      "Balanced panel: 9 companies x 8 years = 72 rows, no missing outcomes or spending")
check("T08_no_forecasts", panel.loc[panel.base_cost_m_2223.notna(), "year_start"].max() <= LAST_ACTUAL_COST_YEAR,
      "No forecast spending year enters any panel")
panel.to_csv(OUT / "panel_all_years.csv", index=False)
balanced.to_csv(OUT / "panel_main_balanced.csv", index=False)
print(balanced[["base_cost_per_property"] + MODELLED].describe().round(2))

# INSIGHT: The main panel has 72 company-years (9 x 8), 60% more than the previous
# five-year design (45). Spending per property and every modelled outcome are present
# in every row, so all three outcomes are analysed on exactly the same sample.


# %% 5. RQ1 -- How do spending and outcomes vary? -------------------------------------
summary = (panel[panel.year_start.between(2015, 2024)]
           .groupby("year_start")[["base_cost_per_property"] + list(OUTCOMES)]
           .mean().round(3))
summary.to_csv(OUT / "rq1_yearly_company_means.csv")
first, last = balanced[balanced.year_start == 2017], balanced[balanced.year_start == 2024]
change = (last.set_index("company_code")[["base_cost_per_property"] + MODELLED]
          - first.set_index("company_code")[["base_cost_per_property"] + MODELLED])
change.round(3).to_csv(OUT / "rq1_change_2017_to_2024.csv")
print(summary)
print("\nCompanies with lower rate in 2024-25 than 2017-18:",
      {o: int((change[o] < 0).sum()) for o in MODELLED})
print("Companies spending more per property in 2024-25 than 2017-18:", int((change.base_cost_per_property > 0).sum()))

# INSIGHT (RQ1, run of 18 Nov 2026):
# - Spending: the average company's base spending per property was flat from 2017-18 to
#   2020-21 (GBP 132-136), then rose to GBP 172 in 2024-25, about 27% above 2017-18 in
#   real terms. All nine companies spent more per property in 2024-25 than in 2017-18.
#   The largest rises were South West Water (+GBP 99), Southern Water (+GBP 57) and
#   Thames Water (+GBP 54).
# - Outcomes:
#   - Internal flooding fell on average (2.76 -> 1.67 per 10,000 connections), with 7 of 9
#     companies lower.
#   - Collapses also fell (11.9 -> 6.6 per 1,000 km), with 7 of 9 lower.
#   - Pollution rose (33.5 -> 53.4 per 10,000 km, the highest year in the window); only
#     Severn Trent and Yorkshire Water ended lower.
# - Spending rising while flooding and collapses fall is a sector-wide pattern over time.
#   On its own it is not evidence of a link, because both may follow shared trends. RQ2
#   therefore compares each company with itself and removes shared year effects.


# %% 6. RQ2 + RQ3 -- association models ------------------------------------------------
results, omissions = [], []


def add(data, outcome, predictors, spec, source="PR24 V6.0", measure="base spending per property"):
    row, omit = m.run_model(data.dropna(subset=[outcome] + predictors), outcome, predictors, spec, source, measure)
    results.append(row)
    omissions.extend(omit)


unbalanced = panel[panel.year_start.between(2015, LAST_ACTUAL_COST_YEAR)]
for outcome in MODELLED:
    add(balanced, outcome, ["log_spend_pp"], "main: same year, balanced 2017-24")
    if unbalanced[outcome].notna().sum() > len(balanced):     # only when extra years exist
        add(unbalanced, outcome, ["log_spend_pp"], "unbalanced: all available years")
    add(balanced, outcome, ["log_spend_total", "log_properties"], "total spending + size")
    add(balanced, outcome, ["log_spend_pp_lag1"], "spending one year earlier")
    if outcome == "pollution_rate":     # calendar outcome: lag 2 is the only fully preceding year
        add(balanced, outcome, ["log_spend_pp_lag2"], "spending two years earlier")

# Spending measure comparison on identical rows: base vs total spending, 2020-21 to 2024-25.
same = balanced[balanced.year_start >= 2020].merge(
    wcpr[["company_code", "year_start", "totex_per_property"]], on=["company_code", "year_start"])
same["log_totex_pp"] = np.log(same.totex_per_property)
for outcome in MODELLED:
    add(same, outcome, ["log_spend_pp"], "base spending, 2020-24")
    add(same, outcome, ["log_totex_pp"], "total spending, 2020-24", measure="total spending per property")

# Previous design (16 Nov 2026), reproduced as a check: WCPR totex and WCPR outcomes, 2020-24.
wcpr_model = wcpr.assign(log_totex_pp=np.log(wcpr.totex_per_property))
for outcome in ["sewer_flooding_rate", "sewer_collapse_rate"]:
    add(wcpr_model, outcome, ["log_totex_pp"], "previous design: WCPR totex 2020-24",
        source="WCPR 2024-25", measure="total spending per property")

results = pd.DataFrame(results)
main = results.specification.str.startswith("main") & results.outcome.isin(["sewer_flooding_rate", "sewer_collapse_rate"])
results["p_wild_holm"] = np.nan
results.loc[main, "p_wild_holm"] = m.holm(results.loc[main, "p_wild_bootstrap"])
results["mde_pct_of_mean"] = 100 * results.mde_10pct_80power / results.outcome_mean

previous = results[results.specification.str.startswith("previous")].set_index("outcome").diff_per_10pct
check("T09_reproduce_previous", np.isclose(previous["sewer_flooding_rate"], 0.0134, atol=5e-5)
      and np.isclose(previous["sewer_collapse_rate"], 0.3111, atol=5e-5),
      f"Previous main estimates reproduced: flooding {previous['sewer_flooding_rate']:.4f}, collapses {previous['sewer_collapse_rate']:.4f}")
check("T10_bootstrap", results.bootstrap_draws.eq(512).all(), "All 512 sign patterns used in every model")

# Independent check of the two main slopes by balanced two-way demeaning (no dummies).
for outcome in ["sewer_flooding_rate", "sewer_collapse_rate"]:
    def demean(col):
        a = balanced.pivot(index="company_code", columns="year_start", values=col).to_numpy()
        return a - a.mean(0) - a.mean(1)[:, None] + a.mean()
    x, y = demean("log_spend_pp"), demean(outcome)
    dummy = results.loc[main & results.outcome.eq(outcome), "slope_log"].iloc[0]
    check(f"T11_demean_{outcome}", np.isclose(np.sum(x * y) / np.sum(x * x), dummy, atol=1e-9),
          "Demeaned slope equals dummy-variable slope")

results.to_csv(OUT / "model_results.csv", index=False)
pd.DataFrame(omissions).to_csv(OUT / "company_omission_results.csv", index=False)
show = ["outcome", "specification", "n", "diff_per_10pct", "ci_low_10pct", "ci_high_10pct",
        "p_wild_bootstrap", "mde_10pct_80power", "mde_pct_of_mean"]
with pd.option_context("display.width", 200, "display.max_columns", 20):
    print(results[show].round(3).to_string(index=False))

# INSIGHT (RQ2, main models, run of 18 Nov 2026). Values are differences in each
# outcome's own unit for 10% more base spending per property, with 95% CV3 ranges:
# - Flooding    +0.06  [-0.29, +0.41]   bootstrap p = 0.68
# - Collapses   -0.22  [-1.58, +1.14]   bootstrap p = 0.72
# - Pollution   +0.84  [-4.97, +6.66]   bootstrap p = 0.78
# Every range includes zero, and the Holm-adjusted p-values for the two main outcomes are
# both 1.00. Over eight years the data show no clear association in either direction.
#
# INSIGHT (RQ3, sensitivity):
# - The design can detect only large links. With 80% power it would detect a difference
#   of 0.49 for flooding (22% of the average rate), 1.9 for collapses (21%) and 8.1 for
#   pollution (21%) per 10% more spending. "No clear link" therefore means that any real
#   link is smaller than about a fifth of the average rate per 10% more spending, or
#   cannot be detected with nine companies.
# - No single company drives the main results. The leave-one-company-out ranges are
#   flooding -0.05 to +0.14, collapses -0.53 to +0.26 and pollution -1.34 to +2.12.
#   The pollution range crosses zero only when Southern Water is left out.
# - The unbalanced panel and the "total spending + size" version give the same picture.
# - Timing: spending one year earlier gives flooding -0.12 and collapses -0.12, both
#   unclear. For pollution, last year's spending gives -2.12 [-4.83, +0.59]. Its bootstrap
#   p-value is 0.02 and all nine leave-one-out fits are negative, but the CV3 range
#   includes zero, the two methods disagree, and it is one of 20 specifications. Spending
#   two years earlier (wholly before the calendar-year outcome) gives -0.07. This is a
#   timing pattern worth discussing, not a finding.
# - Base versus total spending on the same 45 rows (2020-24): no measure shows a clear
#   link with any outcome. The previous five-year design is reproduced exactly (flooding
#   0.013, collapses 0.311), which confirms that this code matches the verified 16 Nov
#   pipeline.


# %% 7. Figures for the report and dashboard -- R06 -----------------------------------
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.bbox": "tight"})
colours = plt.get_cmap("tab10").colors

# 7a. Data coverage: which company-years exist for each outcome.
fig, ax = plt.subplots(figsize=(10, 3.2))
ax.imshow(coverage.to_numpy(float), vmin=0, vmax=9, cmap="Blues", aspect="auto")
ax.set_xticks(range(coverage.shape[1]), [label(y) for y in coverage.columns], rotation=35, ha="right")
ax.set_yticks(range(coverage.shape[0]), [c.replace("_", " ") for c in coverage.index])
for i in range(coverage.shape[0]):
    for j in range(coverage.shape[1]):
        v = int(coverage.iloc[i, j])
        ax.text(j, i, v, ha="center", va="center", color="white" if v > 5 else "black")
ax.add_patch(plt.Rectangle((1.5, -0.5), 8, coverage.shape[0], fill=False, lw=2, ec="#d62728"))
ax.set_title("Companies with data (of 9), PR24 outcomes. Red box: balanced main window 2017-18 to 2024-25")
fig.savefig(FIG / "fig_outcome_coverage.png")
plt.close(fig)

# 7b. Trends by company: base spending per property and the three modelled outcomes.
markers = ["o", "s", "^", "D", "v", "P", "X", "*", "h"]      # shape as well as colour (accessibility)
fig, axes = plt.subplots(2, 2, figsize=(12, 8.5), sharex=True)
series = [("base_cost_per_property", "Base spending per property (GBP, 2022-23 prices)")] + \
         [(o, f"{o.replace('_', ' ').capitalize()}\n({OUTCOMES[o]})") for o in MODELLED]
for ax, (col, title) in zip(axes.flat, series):
    for i, c in enumerate(COMPANIES):
        s = balanced[balanced.company_code == c]
        ax.plot(s.year_start, s[col], marker=markers[i], ms=4, lw=1.3, color=colours[i],
                label=f"{c} {COMPANIES[c]}")
    ax.set_title(title, fontsize=10)
    ax.set_xticks(list(BALANCED_YEARS), [label(y) for y in BALANCED_YEARS], rotation=35, ha="right")
    ax.grid(alpha=0.2)
handles, names = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, names, loc="lower center", ncol=5, fontsize=8, frameon=False, bbox_to_anchor=(0.5, -0.04))
fig.suptitle("RQ1: company trajectories, 2017-18 to 2024-25")
fig.savefig(FIG / "fig_company_trends.png")
plt.close(fig)

# 7c. Forest plot: every estimate with its 95% interval and the minimum detectable effect.
fig, axes = plt.subplots(3, 1, figsize=(10, 13))
for ax, outcome in zip(axes, MODELLED):
    r = results[results.outcome == outcome].reset_index(drop=True)
    pos = np.arange(len(r))[::-1]
    ax.errorbar(r.diff_per_10pct, pos, xerr=[r.diff_per_10pct - r.ci_low_10pct,
                                             r.ci_high_10pct - r.diff_per_10pct],
                fmt="o", color="#1f5f8b", capsize=3)
    mde = r.loc[0, "mde_10pct_80power"]
    ax.axvspan(-mde, mde, color="#f2c14e", alpha=0.25,
               label="Range the main model cannot reliably detect (80% power)")
    ax.axvline(0, color="grey", ls="--", lw=1)
    ax.set_yticks(pos, r.specification, fontsize=9)
    ax.set_title(f"{outcome.replace('_', ' ').capitalize()} ({OUTCOMES[outcome]})", fontsize=10, loc="left")
    ax.set_xlabel("Difference in outcome for 10% more spending per property")
handles, names = axes[0].get_legend_handles_labels()
fig.legend(handles, names, loc="lower center", fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.suptitle("RQ2-RQ3: associations with 95% CV3 intervals (nine company clusters)\n"
             "Associations, not causal effects", fontsize=11)
fig.tight_layout(rect=(0, 0.02, 1, 0.97))
fig.savefig(FIG / "fig_association_estimates.png")
plt.close(fig)
print("Figures written to", FIG)


# %% 8. Tables for the Power BI dashboard -- R06, R09, R10 (RQ4) ------------------------
# Small, clearly named CSV files with plain-language labels and units already attached,
# so the dashboard never has to recalculate or relabel anything (it only displays).
PBI = OUT / "powerbi"
PBI.mkdir(exist_ok=True)
LABEL = {"sewer_flooding_rate": "Internal sewer flooding", "sewer_collapse_rate": "Sewer collapses",
         "pollution_rate": "Pollution incidents", "treatment_compliance_pct": "Treatment works compliance"}
UNIT = {"sewer_flooding_rate": "incidents per 10,000 connections",
        "sewer_collapse_rate": "collapses per 1,000 km of sewer",
        "pollution_rate": "incidents per 10,000 km of sewer",
        "treatment_compliance_pct": "% of works compliant"}

(balanced[["company_code", "company_name", "reporting_year", "year_start", "base_cost_per_property",
           "base_cost_m_2223", "properties"] + list(OUTCOMES)]
 .rename(columns={"base_cost_per_property": "base_spend_per_property_gbp",
                  "base_cost_m_2223": "base_spend_gbp_m"})
 .to_csv(PBI / "pbi_panel.csv", index=False))

long = outcomes_long.assign(
    company_name=outcomes_long.company_code.map(COMPANIES),
    reporting_year=outcomes_long.year_start.map(label),
    outcome=outcomes_long.metric.map(LABEL), unit=outcomes_long.metric.map(UNIT),
    available=np.where(outcomes_long.value.notna(), "Yes", "No (missing in source)"),
    in_main_window=np.where(outcomes_long.year_start.isin(BALANCED_YEARS), "Yes", "No"))
long[["company_code", "company_name", "reporting_year", "year_start", "outcome", "unit",
      "period_basis", "value", "available", "in_main_window"]].to_csv(PBI / "pbi_outcomes_long.csv", index=False)


def role(spec):
    if spec.startswith("main"):
        return "1 Main model"
    if spec.startswith("previous"):
        return "4 Reproduction check"
    if "2020-24" in spec:
        return "3 Base vs total spending"
    return "2 Sensitivity"


models = pd.DataFrame({
    "outcome": results.outcome.map(LABEL), "unit": results.outcome.map(UNIT),
    "specification": results.specification, "role": results.specification.map(role),
    "answers": np.where(results.specification.str.startswith("main"), "RQ2", "RQ3"),
    "spending_measure": results.spending_measure, "outcome_source": results.outcome_source,
    "years": results.first_year.map(label) + " to " + results.last_year.map(label),
    "company_years": results.n, "companies": results.companies,
    "difference_per_10pct": results.diff_per_10pct.round(3),
    "ci95_low": results.ci_low_10pct.round(3), "ci95_high": results.ci_high_10pct.round(3),
    "range_includes_zero": np.where((results.ci_low_10pct < 0) & (results.ci_high_10pct > 0), "Yes", "No"),
    "p_wild_bootstrap": results.p_wild_bootstrap.round(3), "p_holm_main": results.p_wild_holm.round(3),
    "detectable_difference_80pct": results.mde_10pct_80power.round(3),
    "detectable_pct_of_average": results.mde_pct_of_mean.round(1)})
models.to_csv(PBI / "pbi_models.csv", index=False)

main_rows = results[results.specification.str.startswith("main")]
detect = pd.DataFrame({
    "outcome": main_rows.outcome.map(LABEL), "unit": main_rows.outcome.map(UNIT),
    "average_rate": main_rows.outcome_mean.round(2),
    "difference_per_10pct": main_rows.diff_per_10pct.round(2),
    "ci95_low": main_rows.ci_low_10pct.round(2), "ci95_high": main_rows.ci_high_10pct.round(2),
    "detectable_difference_80pct": main_rows.mde_10pct_80power.round(2),
    "detectable_pct_of_average": main_rows.mde_pct_of_mean.round(0)})
detect["plain_message"] = [
    f"No clear link. Only a difference of about {d:.2f} ({p:.0f}% of the average rate) "
    f"per 10% more spending could be reliably detected."
    for d, p in zip(detect.detectable_difference_80pct, detect.detectable_pct_of_average)]
detect.to_csv(PBI / "pbi_detectability.csv", index=False)

(coverage.stack().rename("companies_with_data").reset_index()
 .assign(outcome=lambda d: d.metric.map(LABEL), reporting_year=lambda d: d.year_start.map(label))
 [["outcome", "reporting_year", "companies_with_data"]].to_csv(PBI / "pbi_coverage.csv", index=False))

pd.DataFrame([
    ["Base spending per property", "GBP per connected property, 2022-23 prices", "No automatic direction",
     "Financial year (April-March)", "Explanatory variable",
     "Ofwat PR24CA06 dataset (Oct 2025): modelled base costs, wastewater network plus",
     "Operating and maintaining existing assets; excludes enhancement and bioresources. Severn Trent includes Hafren Dyfrdwy (~1% of costs)."],
    ["Total spending per property (totex)", "GBP per connected property, 2017-18 prices", "No automatic direction",
     "Financial year", "Comparison only (2020-21 to 2024-25)", "Ofwat WCPR 2024-25, item B0143TAWWNP",
     "Includes enhancement; not available on a consistent basis before 2020-21."],
    [LABEL["sewer_flooding_rate"], UNIT["sewer_flooding_rate"], "Lower is better", "Financial year",
     "Modelled outcome", "Ofwat historical performance trends for PR24 V6.0", ""],
    [LABEL["sewer_collapse_rate"], UNIT["sewer_collapse_rate"], "Lower is better", "Financial year",
     "Modelled outcome", "Ofwat historical performance trends for PR24 V6.0", ""],
    [LABEL["pollution_rate"], UNIT["pollution_rate"], "Lower is better", "Calendar year (label 2024-25 = 2024)",
     "Modelled outcome", "Ofwat historical performance trends for PR24 V6.0", ""],
    [LABEL["treatment_compliance_pct"], UNIT["treatment_compliance_pct"], "Higher is better",
     "Calendar year", "Descriptive only", "Ofwat historical performance trends for PR24 V6.0",
     "Boundary wider than network-plus spending, so not modelled."],
], columns=["measure", "unit", "better_direction", "period", "role", "source", "notes"]
).to_csv(PBI / "pbi_dictionary.csv", index=False)
print("Power BI tables written:", sorted(p.name for p in PBI.glob("*.csv")))


# %% 9. Validation record and run manifest -- R02, R11 ---------------------------------
check("T12_inputs_unchanged", all(sha256(p) == input_hashes_before[k] for k, p in FILES.items()),
      "Raw input files unchanged by the run")
pd.DataFrame(CHECKS).to_csv(OUT / "validation_checks.csv", index=False)
outputs = sorted(p for folder in (OUT, FIG) for p in folder.rglob("*")
                 if p.is_file() and p.suffix in {".csv", ".png"})
manifest = {
    "python": platform.python_version(),
    "packages": {p: version(p) for p in ["numpy", "pandas", "scipy", "openpyxl", "matplotlib"]},
    "inputs_sha256": {p.name: sha256(p) for p in FILES.values()},
    "main_window": "2017-18 to 2024-25 (balanced, 72 company-years)",
    "spending_measure": "Ofwat modelled base costs, wastewater network plus, GBP 2022-23 prices, per connected property",
    "models": len(results), "checks_passed": len(CHECKS),
    "outputs_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p) for p in outputs},
}
(OUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"All {len(CHECKS)} checks passed; {len(results)} models; manifest written.")
