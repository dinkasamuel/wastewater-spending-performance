# 5 Implementation

This chapter describes how the design was built. Action identifiers (D1, E2 …) refer to Figure 4.1, and requirement identifiers (R01 …) to Figure 4.2. All code, data and outputs are in the project repository (Appendix H).

## 5.1 Environment and structure

The analysis uses Python 3.13.9 with pandas 2.3.3, NumPy 2.3.5, SciPy 1.16.3, openpyxl 3.1.5 and Matplotlib 3.10.6.

The repository has six numbered folders, in the order the work flows: unchanged Ofwat sources (`1_data/`), the analysis (`2_analysis/`), results (`3_results/`), the dashboard (`4_dashboard/`), the report (`5_report/`) and project records (`6_project_records/`). Helper scripts sit in `tools/`.

The whole analysis is one Jupyter notebook (`2_analysis/analysis.ipynb`), run from top to bottom. Statistical methods sit in a separate module (`methods.py`), so the notebook reads as ten numbered steps. Each step heading carries one tag in the same format, `[RQ · Objective · Requirement]`, and each result is followed by a short "What this shows" note written from the run.

## 5.2 Data pipeline (D1–D2; R01–R05)

The pipeline reads three Ofwat workbooks directly:

| Source | Use |
|---|---|
| PR24 base-cost dataset CA06, October 2025 (Ofwat, 2025e) | Base spending and connected properties, 2011-12 to 2024-25 |
| PR24 historical performance trends V6.0 (Ofwat, 2026) | Outcomes, 2015-16 to 2024-25 |
| WCPR 2024-25 (Ofwat, 2025b) | Total spending, for comparison and reproduction |

Spending is converted to pounds per connected property at 2022-23 prices. Forecast years (2025-26 onwards) are removed. Severn Trent appears in the cost data as its combined England and Wales series, the only one with properties for every year; the Welsh element is about 1% of its costs.

The main panel keeps the 72 company-years (2017-18 to 2024-25) in which every company reports every outcome. Missing values are never filled in.

Fifteen automatic checks stop the run on any failure (R03). Among them:
- the October 2025 cost file equals the December 2024 file for all 117 shared company-years, confirming one definition;
- all 270 selected WCPR values equal Ofwat's companion workbook;
- the input files are unchanged by the run.

## 5.3 Statistical models (E1–E3; R07–R08)

**Model.** Each outcome is regressed on the logarithm of base spending per property, with an indicator for every company and every year (two-way fixed effects). The company indicators absorb permanent differences such as size and geography. The year indicators absorb shared conditions such as weather. The spending coefficient is therefore estimated only from change *within* each company. It is reported as the difference in the outcome, in its own unit, associated with 10% more spending: the coefficient multiplied by ln(1.1).

**Uncertainty.** With only nine companies, inference follows MacKinnon, Nielsen and Webb (2023):
- **CV3 jackknife:** the model is refitted leaving out each company in turn, giving 95% intervals on the t distribution with 8 degrees of freedom.
- **Restricted wild-cluster bootstrap:** tests whether the spending coefficient could be zero by enumerating all 2⁹ = 512 sign patterns, so the p-value contains no random element.
- **Holm adjustment** (Holm, 1979) is applied to the two main outcomes, flooding and collapses.

**Detectable effect.** For each model, the minimum detectable effect (Bloom, 1995) gives the smallest association the design would detect with 80% power.

**Specifications.** Twenty models were fitted:
- three main models, one per outcome (RQ2);
- seventeen sensitivity checks (RQ3):
  - an unbalanced panel;
  - total spending with size entered separately;
  - lagged spending, including a two-year lag for calendar-year pollution;
  - base against total spending on identical 2020-24 rows;
  - the earlier five-year design reproduced.

**Verification.** Before use on real data, self-tests recover a known slope from artificial data. Every slope is re-derived by partialling out the other variables, and the main slopes are confirmed by an independent calculation. The earlier design's published estimates are reproduced exactly.

## 5.4 Reproducibility and notebook (E4; R11)

**Run manifest.** Each run records package versions and SHA-256 hashes of every input and output.

**Repeat runs.** Two fresh runs of the notebook gave byte-identical results for all 25 output files.

**One master notebook.** The notebook is the single source of the analysis. A small helper (`tools/run_analysis.py`) executes it from a fresh kernel and saves it, so every number shown in it comes from a complete run. It executed without errors.

**Traceability.** The supervisor asked for each answer to be traceable to the artefact:
- every step heading names the research question, objective and requirements it answers, for example `[RQ2 + RQ3 · Obj 3, 4 · R07 R08]`;
- a "What this shows" note follows each result.

## 5.5 Dashboard (F1; R06, R09, R10)

**Tables.** The analysis writes six small, labelled tables for the dashboard.

**Build.** A build script generates the Power BI project: six pages and 21 data visuals, each with a title and alt text. Every bound field is checked against the model.

**Display only.** The dashboard displays results and never refits a model.

**Portability.** A `DataFolder` parameter makes the project portable, and a saved `.pbix` copy opens with its data embedded.

**Traceability.** Each page header names the research question, objective and requirements it answers.

Live testing of the dashboard is reported in Chapter 7.
