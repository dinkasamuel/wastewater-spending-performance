# Decision log

This log records decisions that change scope, requirements or method. It supports the "evidence of planning and management" criterion; earlier decisions are recorded in `Project_Review_Version_2026-11-16/docs/decision_log.csv`.

## D-2026-11-18 Requirements realism review

**Trigger:** a review of whether each requirement can be met by 7 January 2027, given what has been implemented so far.

**Findings:**
- R01–R08 and R11 are implemented and automatically checked.
- R09 and R10 are built, but their acceptance tasks (UI01–UI10) are not yet recorded.
- R12, which required evaluation with users, depends on UWE ethics approval and on recruiting participants before the supervisor's draft cut-off (about 24 December).
- Risk register item K07 already flagged that RQ4 could be left partly unanswered.

**Decisions:**
1. **R12 split into two requirements.**
   - R12a (Must) is a researcher-led evaluation: UI01–UI10, a structured heuristic review and accessibility checks.
   - R12b (Should) is a small user study with 3–5 informed non-specialists. It runs only if ethics approval is obtained by 4 December 2026; if it is not, the reason is recorded and the study omitted.
2. **R07 acceptance test made measurable.** Every estimate must report its sample size, number of clusters, specification, CV3 interval and restricted bootstrap p-value. The outputs must contain no causal wording.
3. **R10 acceptance test reworded so the researcher can check it directly.** Each page shows the source, unit, price basis and period; definitions are reachable in one click; every estimate is shown with its interval.
4. **R13 dependency changed.** R13 now depends on R12a and remains optional.

**Affected items:**
- `docs/Requirements_register.csv`
- Figures 4.1 and 4.2
- Chapter 4, Sections 4.1, 4.2 and 4.5

**Actions:**
- [ ] Confirm the UWE ethics route and turnaround for a low-risk dashboard user study.
- [ ] Ask the supervisor whether R12a is acceptable as the minimum evaluation.
- [ ] Complete UI01–UI10 and record the results.

## D-2026-11-18b Ethics coverage for the user study

**Finding:** the student's existing ethics declaration covers the use of public Ofwat data only. The planned R12b user study involves human participants, so it is **not covered**.

**Decision:**
- No participant is contacted until the supervisor has completed a new or updated UWE Student Ethical Review Record for the study, with a low-risk outcome.
- The draft pack is in `markdown/Ethics_*.md` (Word copies in `docs/`). The student will raise the request with the supervisor directly.
- If the study is not approved by 4 December 2026, it is not run. RQ4 then relies on the researcher-led evaluation (R12a), and the limitation is discussed in Chapter 7.

**Actions:**
- [ ] Student raises the study with the supervisor and shares the pack (target: this week).
- [ ] Record the date of the supervisor's decision and its outcome here.

## D-2026-11-18c Main spending measure and analysis window (option A)

**Decision (student-approved):**
- **Explanatory variable:** Ofwat's *modelled base costs, wastewater network plus*, from PR24 final-determination model CA08 (December 2024), in GBP at 2022-23 prices, divided by connected properties.
- **Main analysis:** a balanced panel for 2017-18 to 2023-24 (9 companies × 7 years = 63 company-years).
- **Outcomes:** PR24 historical performance trends V6.0, a single release for all years.

**Evidence:**
- **One definition for every year.** CA08 restates base costs on a single definition for 2011-12 to 2023-24.
- **Forecasts excluded.** The file's 2024-25 to 2029-30 values are forecasts: CA08's 2024-25 property counts differ from the actual WCPR counts, while 2023-24 matches exactly. The forecast years are therefore excluded (check T08).
- **Properties agree.** CA08 property counts equal the WCPR figures for 7 of 9 companies. Severn Trent is about +1.9% higher, because the CA08 series (SVH) includes Hafren Dyfrdwy, whose base costs are about 1% of the combined total. South West Water differs by up to −2.0%, in 2020-21 and 2021-22 only.
- **The v4 dataset is not used for the main analysis.** CA08 and the older v4 dataset differ by more than a price conversion (ratios 1.14–1.40 by company), so they are different definitions and are never mixed.
- **Common window.** Outcomes are complete for all nine companies from 2017-18, which is why the main panel starts then.
- **The code matches the earlier verified pipeline.** The previous five-year total-spending design is reproduced exactly (check T09).

**Sensitivity analyses kept:**
- the unbalanced panel;
- total spending plus size;
- one-year and two-year lags;
- base versus total spending on the same 2020-23 rows;
- leaving out each company in turn;
- the previous design.

**Open item:** extending the analysis to 2024-25 requires rebuilding Ofwat's base-cost definition from each company's 2024-25 annual report tables and validating that rebuild on 2022-23 and 2023-24. The files have not been downloaded yet; they await the student's approval.

**Affected items:**
- Chapters 1–4: aim, RQ2 wording, scope and feasibility text.
- The requirements register and Figure 4.2, which need their wording updated.
- The Power BI dashboard, which moves to version 3.

## D-2026-11-18d Extension to 2024-25

**Source:** Ofwat's PR24CA06 "WW1" dataset, republished in October 2025 for the CMA redeterminations (9.3 MB). It was downloaded with the student's approval on 18 November 2026.

**Evidence:**
- **Same definition.** Modelled base costs for 2011-12 to 2023-24 equal the December 2024 file (CA08) exactly for every company-year (check T01b).
- **Actual 2024-25 figures.** The 2024-25 connected-property counts equal the actual WCPR 2024-25 counts for 8 of 9 companies; Severn Trent differs by +0.5%, the known Hafren Dyfrdwy boundary. The file's inputs are labelled "JULY2025", the month companies submitted their 2024-25 annual reports.

**Decision:**
- The main analysis window becomes **2017-18 to 2024-25** (balanced; 9 × 8 = 72 company-years).
- The base-versus-total spending comparison now covers 2020-21 to 2024-25 (45 rows).
- The 27 company annual-report files are no longer needed.

**Result:** all 15 checks pass, two fresh runs give identical outputs, and the main conclusions are unchanged: no clear association for any outcome.

## D-2026-11-18e Power BI dashboard version 3

**Decision:** replace v2 with a new dashboard (v3) generated by `code/build_powerbi_v3.py` from the analysis outputs.

**What changes:**
- **Data:** base spending over the balanced 2017-18 to 2024-25 panel.
- **Portable data location:** a single Power Query parameter, `DataFolder`, so markers set one path and refresh. This fixes review item A2.
- **Traceability tags:** every page header names the research questions, objectives and requirements it answers (supervisor feedback, 3 October). This fixes review item A1 for the dashboard.
- **New page 4, "What can be detected":** shows the minimum detectable effects.
- **No relabelling inside the dashboard:** plain-language labels and units come from the analysis tables, so the dashboard displays results without recalculating or relabelling them.
- **Kept from v2:** alt text, a unique tab order and series labels on every line chart.

**Checks:**
- The build checks that every bound field exists in the model and that every data visual has a title and alt text.
- Rebuilding gives identical files.

**Not yet verified:** opening and refreshing in Power BI Desktop. This is covered by live checks L0–L14 (`PowerBI_live_check_sheet`).

## D-2026-11-24 Simplified project layout; the notebook is the master copy

**Trigger:** the student found the project confusing. The analysis existed both as a script and as a generated notebook, helper scripts were mixed in with the analysis, three dashboard versions sat side by side, and the tags used several styles.

**Decision (student-approved):**

**One master notebook.**
- `2_analysis/analysis.ipynb` is the single source of the analysis.
- The old script (`code/wastewater_analysis.py`) and the notebook generator were retired.

**One tag format.** Every notebook step heading uses `[RQ · Objective · Requirement]`, and each result is followed by a "What this shows" note.

**Numbered folders.**

| New folder | Was |
|---|---|
| `1_data/` | `data/raw/` |
| `2_analysis/` | `code/` (analysis) |
| `3_results/tables/` | `outputs/` |
| `3_results/figures/` | `figures/` |
| `3_results/dashboard_tables/` | `outputs/powerbi/` |
| `4_dashboard/` | `powerbi/v3/` |
| `5_report/` | report chapters, from `docs/` and `markdown/` |
| `6_project_records/` | working records, from `docs/` and `markdown/` |
| `tools/` | helper scripts, from `code/` |

**Old dashboards.** Dashboard v1 and v2 were removed from the working folder. They remain in the git history, so the evaluation record is intact.

**Earlier entries.** Earlier entries in this log and in the evaluation log use the old paths; this table maps them to the new layout.

**Verification:**
- **Results unchanged.** All 20 result tables and the 3 charts produced by the notebook are byte-identical to those produced by the script before the change.
- **Checks and models.** All 15 checks pass and 20 models are fitted.
- **Reproducible.** Two fresh runs of the notebook are byte-identical (25 of 25 files).
- **Dashboard rebuilt.** The dashboard was rebuilt with `DataFolder` pointing to `3_results\dashboard_tables\`; its static checks pass.

**Follow-up:**
- The saved `.pbix` still holds the old data path. It needs one refresh in Power BI Desktop after setting `DataFolder`, then a save.

## D-2026-11-24b Master dataset and data dictionary

**Decision (student-approved):** the data are consolidated into one file, and every column is documented.

**The master dataset.**
- File: `3_results/tables/master_dataset.csv`.
- Contents: one row per company and year, 2015-16 to 2024-25 (90 rows), with plain column names. It holds:
  - base spending (£m and per property), including the previous year and two years earlier;
  - connected properties;
  - total spending, for 2020-21 onward;
  - the four outcomes;
  - an `in_main_analysis` flag.
- The notebook writes this file and then reads only it for every model. The 72-row model sample is simply the flagged rows.

**The data dictionary.**
- File: `3_results/tables/data_dictionary.csv`.
- It defines all 195 columns of the 19 tables the notebook writes: what each column means, its unit and its source (Ofwat file and item code, or the formula).
- The definitions are kept in `2_analysis/column_definitions.csv`.

**New checks:**
- **T07a:** the master dataset has 90 unique company-years.
- **T13:** every column of every output table is defined. If a column is ever added without a definition, the run stops, so the dictionary cannot go out of date.

**Verification:** every result table and chart is byte-identical to the previous run. All 17 checks pass.
