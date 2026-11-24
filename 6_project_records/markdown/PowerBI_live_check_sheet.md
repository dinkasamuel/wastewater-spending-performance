# Live check sheet: Power BI dashboard version 3

**File:** `4_dashboard\Wastewater_Dashboard.pbip`. Open it in Power BI Desktop.
**Built by:** `tools/build_dashboard.py` from the tables in `3_results\dashboard_tables\`.

Record each result as PASS or FAIL, with a short note. If something fails, take a screenshot and save it in `6_project_records\screenshots\`. These checks provide evidence for requirements R06, R09, R10 and R12a.

| # | Task | What to do | Expected | Result | Note |
|---|---|---|---|---|---|
| L0 | Open, set the data folder, refresh | Open the .pbip. Go to Home → Transform data → **Edit parameters** and check that `DataFolder` points to your `3_results\dashboard_tables\` folder, ending with `\`. Then click **Refresh** | No errors. In Data view the row counts are: pbi_panel 72, pbi_outcomes_long 360, pbi_models 20, pbi_detectability 3, pbi_coverage 40, pbi_dictionary 6 | | |
| L1 (UI01) | One audited row | Page 2: select Anglian Water and 2020-21 | Base spending per property 121.23; base spending £m 345.80; properties 2,852,389; flooding 1.33; collapses 6.04; pollution 27.47; compliance 99.29 | | |
| L2 (UI02) | All 72 rows | Page 2: clear the slicers. On the table, choose "…" → Export data → CSV, saved as `3_results\tables\v3_page2_export.csv` | Saved. Claude compares all 72 rows against `pbi_panel.csv` | | |
| L3 (UI03) | Unit shown | Page 5: select only Pollution incidents | The chart title reads "Pollution incidents \| incidents per 10,000 km of sewer \| blank = not available" | | |
| L4 (UI04) | Missing stays blank | Page 5: Pollution incidents, Anglian Water | 2015-16 and 2016-17 are blank in the table ("No (missing in source)"), and no point is drawn at zero | | |
| L5 (UI06) | Two outcomes selected | Page 5: Ctrl-click two outcomes | The chart is empty, and the title says "Select exactly one outcome…" | | |
| L6 (UI05) | Stored results only | Page 3: choose Type = Main model | 3 rows (one per outcome), each with 72 company-years and 9 companies. Changing a slicer only filters rows | | |
| L7 | Plain labels | Look at the column headers on every page | No underscores or raw field names | | |
| L8 | Second cue besides colour | Page 1 | Company names appear at the line ends (series labels). If not, note it | | |
| L9 (UI08) | Keyboard | Page 1: press Ctrl+F6 to reach the canvas, then Tab repeatedly | Focus moves header → slicers → charts in reading order | | |
| L10 (UI08) | Alt text | Select any chart → Format → General → Alt text | Alt text present | | |
| L11 (UI08) | Legibility | View each page at 100% on your screen | Titles and table text readable without zooming in | | |
| L12 | Traceability tags | Read each page header | Every page names the research question(s), objective(s) and requirements it answers | | |
| L13 (UI07) | Definitions | Page 6 | Unit, direction, period, source and notes for every measure; limits listed | | |
| L14 (UI10) | Save and reopen | File → Save as `4_dashboard\Wastewater_Dashboard.pbix`. Close it, then reopen the .pbix | Opens on page 1 with all six pages present | | |

When finished, tell me. I'll compare the exported CSV and record the results in the evaluation log.
