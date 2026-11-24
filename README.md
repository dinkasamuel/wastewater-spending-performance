# Wastewater spending and operational performance in England's water and sewerage companies

MSc Data Science dissertation project, UWE Bristol: Dinka Christabel Samuel (student number 25067140).

**Question:** when one of England's nine water and sewerage companies spends more than usual on running and maintaining its wastewater network (base spending), do sewer flooding, sewer collapses and pollution incidents change?

**Answer (2017-18 to 2024-25, 72 company-years):** there is **no clear association** in either direction for any of the three outcomes. With nine companies, only links of roughly a fifth of each outcome's average rate per 10% more spending could be reliably detected. These are associations, not causal effects.

## Folders (in the order the work flows)

| Folder | What is in it |
|---|---|
| `1_data/` | Ofwat source files, never edited |
| `2_analysis/` | **`analysis.ipynb`**: the whole analysis in one notebook, plus `methods.py` (statistical functions) |
| `3_results/` | `tables/` (CSV results and checks), `figures/` (charts and UML diagrams), `dashboard_tables/` (data for Power BI) |
| `4_dashboard/` | **`Wastewater_Dashboard.pbip`**: the Power BI dashboard (also saved as `.pbix`) |
| `5_report/` | Report chapters, appendices and references (Word), with their Markdown sources in `5_report/markdown/` |
| `6_project_records/` | Ethics pack, decision log, evaluation log, live-check sheet, plans and reviews |
| `tools/` | Helpers you rarely need (see below) |

## How to run it

Requires Python 3.13 with the packages in `requirements.txt`; the reported run used Anaconda Python 3.13.9.

1. **Analysis:** open `2_analysis/analysis.ipynb` in Jupyter and choose *Kernel → Restart & Run All*. Or, from the project folder:
   ```bash
   python tools/run_analysis.py
   ```
   It takes about one minute. Every step should finish without errors, ending with "All 15 checks passed; 20 models".
2. **Check that it reproduces** (optional): this runs the notebook twice and confirms the results are byte-identical.
   ```bash
   python tools/check_reproducibility.py
   ```
3. **Dashboard:** open `4_dashboard/Wastewater_Dashboard.pbip` in Power BI Desktop. Go to *Home → Transform data → Edit parameters* and set `DataFolder` to the full path of this project's `3_results\dashboard_tables\` folder, ending with a backslash. Then click *Refresh*.

## How to read the notebook

The notebook has ten numbered steps. Each heading ends with one tag that shows what the step answers:

> `Step 6 · Is spending associated with outcomes?  [RQ2 + RQ3 · Obj 3, 4 · R07 R08]`

- **RQ** = research question (RQ1–RQ4, Chapter 1).
- **Obj** = objective (1–6, Chapter 1).
- **R** = requirement (R01–R14, Appendix B and Figure 4.2).

Each result is followed by a **What this shows** note in plain English.

The six dashboard pages carry the same tags in their headers.

## Tools

| Tool | Use |
|---|---|
| `run_analysis.py` | Runs the notebook from a fresh kernel and saves it |
| `check_reproducibility.py` | Runs the notebook twice and compares every output |
| `build_dashboard.py` | Rebuilds the Power BI dashboard from `3_results/dashboard_tables/` |
| `check_contrast.py` | Checks dashboard colours against WCAG 2.1 contrast rules |
| `inspect_dashboard.py` | Lists every dashboard page and visual, for evaluation |
| `make_uml_figures.py` | Redraws UML Figures 4.1 and 4.2 |
| `md_to_docx.py` | Turns the Markdown sources into the Word documents |

## Data sources (public, Ofwat; Open Government Licence)

| File in `1_data/` | Use |
|---|---|
| `PR24CA06-WW1-FD.xlsx` | **Main spending source:** modelled base costs and connected properties, wastewater network plus, 2011-12 to 2024-25 actuals (Ofwat, October 2025) |
| `PR24-FD-CA08-Base-costs-wastewater-model-3-Network-Plus.xlsx` | Confirms the main source uses the same definition (December 2024) |
| `Historical-performance-trends-for-PR24-V6.0.xlsx` | Outcomes: flooding, collapses, pollution, treatment compliance, 2015-16 to 2024-25 |
| `WCPR_2024-25-Open-Data-Machine-Readable-Normalised-PostFDUpdate.xlsx` | Total spending (totex) and outcomes 2020-21 to 2024-25, used as a comparison |
| `WCPR-data-report-2024-25-external-V0.2-Final.xlsx` | Cross-check of every WCPR value used |
| `WCPR-2024-25-Open-Data-DataDictionary.csv` | WCPR field definitions |
| `PR24-Cost-Assessment-Master-Dataset-Wholesale-Wastewater-Base-Costs-v4.xlsx` | Earlier base-cost dataset (reference only) |
| `RAG-4.13-Table-definitions-2025-03-31.pdf` | Ofwat definition of totex (table 4C) |

## Attribution

The statistical methods follow MacKinnon, Nielsen and Webb (2023). Use of generative AI is declared in Appendix A (`5_report/`).
