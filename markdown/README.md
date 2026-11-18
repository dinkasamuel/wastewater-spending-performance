# Wastewater spending and operational performance in England's water and sewerage companies

MSc Data Science dissertation project, UWE Bristol: Dinka Christabel Samuel (student number 25067140).

**Question:** when one of England's nine water and sewerage companies spends more than usual on running and maintaining its wastewater network (base spending), do sewer flooding, sewer collapses and pollution incidents change? The analysis compares each company with itself over time and allows for conditions that affect every company in a given year.

**Main finding:** over 2017-18 to 2024-25 (72 company-years) there is **no clear association** in either direction between spending and any of the three outcomes. A minimum-detectable-effect analysis shows how large a link would have to be before nine companies could reveal it. The results are associations, not causal effects.

## Folder structure

| Folder | Contents |
|---|---|
| `code/` | Python scripts (see the table below) |
| `data/raw/` | Ofwat source files, unchanged (see Data sources) |
| `outputs/` | Generated CSV tables, validation checks, run manifest and reproducibility result |
| `figures/` | Result charts and UML diagrams (PNG, plus SVG for the diagrams) |
| `powerbi/` | Power BI dashboard projects: **`v3/` is current**; `v2/` and `v1_2026-11-16/` are earlier versions, kept for the evaluation record |
| `docs/` | Word versions of every project document, plus the requirements register (CSV) |
| `markdown/` | Editable Markdown sources of the documents in `docs/` |

### Scripts in `code/`

| Script | What it does |
|---|---|
| `wastewater_analysis.py` | **The full analysis.** Loads and validates the data, builds the panels, then runs descriptive analysis (RQ1), association models (RQ2) and sensitivity checks (RQ3). Writes the tables and figures. Run it cell by cell (`# %%`) or as a whole |
| `methods.py` | The statistical methods: two-way fixed-effects model, CV3 jackknife, wild-cluster bootstrap (all 512 sign patterns), minimum detectable effect, Holm adjustment and self-tests |
| `check_reproducibility.py` | Runs the analysis twice in fresh processes and confirms that every output is byte-identical |
| `make_uml_figures.py` | Draws UML Figures 4.1 (project workflow) and 4.2 (requirements traceability) |
| `build_powerbi_v3.py` | Builds the current dashboard (v3) from `outputs/powerbi/*.csv`: six pages, research-question tags, alt text, portable data folder |
| `build_powerbi.py` | Builds the earlier dashboard v2 from v1 (kept for the evaluation record) |
| `inspect_pbip.py` | Lists every dashboard page and visual, with its fields and text, for evaluation |
| `md_to_docx.py` | Converts `markdown/*.md` to `docs/*.docx` |

## How to reproduce

Requires Python 3.13 and the packages pinned in `requirements.txt`. The analysis was run with Anaconda Python 3.13.9.

```bash
pip install -r requirements.txt
python code/wastewater_analysis.py
python code/check_reproducibility.py
```

- **Expected result:** all 15 validation checks pass and 20 models are fitted. `outputs/reproducibility_check.json` reports that the outputs are identical across runs.
- **Running time:** about 2 minutes, because each model enumerates all 512 bootstrap sign patterns.

**Power BI (v3):**
1. Run the analysis, which writes `outputs/powerbi/*.csv`, then `python code/build_powerbi_v3.py`.
2. Open `powerbi/v3/Wastewater_Dashboard.pbip` in Power BI Desktop.
3. Go to **Home → Transform data → Edit parameters** and set `DataFolder` to the full path of this repository's `outputs\powerbi\` folder, including the final backslash.
4. Click **Refresh**.

The six pages are: trends (RQ1), audited values (RQ1), associations (RQ2–RQ3), what can be detected (RQ2–RQ4), history and coverage (RQ1), and definitions and limits (RQ4).

## Data sources (all public, Ofwat; Open Government Licence)

| File in `data/raw/` | Publisher and use |
|---|---|
| `PR24CA06-WW1-FD.xlsx` | Ofwat, republished October 2025 for the CMA redeterminations. **Main spending source:** modelled base costs and connected properties for wastewater network plus, 2011-12 to 2024-25 actuals (later years are forecasts and are excluded) |
| `PR24-FD-CA08-Base-costs-wastewater-model-3-Network-Plus.xlsx` | Ofwat PR24 final determinations, December 2024. Used to confirm that CA06 has the same definition: identical for 2011-12 to 2023-24 (check T01b) |
| `Historical-performance-trends-for-PR24-V6.0.xlsx` | Ofwat. Outcomes: internal sewer flooding, sewer collapses, pollution incidents and treatment compliance, 2015-16 to 2024-25 |
| `WCPR_2024-25-Open-Data-Machine-Readable-Normalised-PostFDUpdate.xlsx` | Ofwat Water Company Performance Report 2024-25. Total spending (totex), properties and outcomes for 2020-21 to 2024-25 |
| `WCPR-data-report-2024-25-external-V0.2-Final.xlsx` | Ofwat companion workbook, used to cross-check every selected WCPR value |
| `WCPR-2024-25-Open-Data-DataDictionary.csv` | Field definitions for the WCPR file |
| `PR24-Cost-Assessment-Master-Dataset-Wholesale-Wastewater-Base-Costs-v4.xlsx` | Ofwat, April 2023. Earlier base-cost dataset; reference only, superseded by CA08 |
| `RAG-4.13-Table-definitions-2025-03-31.pdf` | Ofwat regulatory accounting guideline defining totex (APR table 4C) |

## Traceability

Requirements R01–R14 are linked to research questions RQ1–RQ4, to workflow actions in Figure 4.1 and to artefact locations in Figure 4.2 and `docs/Requirements_register.csv`. Code sections are tagged with the requirements and research questions they address.

## Attribution

All code was written for this project with AI assistance (Anthropic's Claude), under the author's direction and review. The statistical methods follow MacKinnon, Nielsen and Webb (2023). The AI-use disclosure is in Appendix A of the report.
