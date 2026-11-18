# Live check sheet: Power BI report version 2

**File:** `powerbi\v2\Wastewater_Review.pbip`. Open it in Power BI Desktop.

Record each result as PASS or FAIL, with a short note. If something fails, take a screenshot and save it in `outputs\screenshots\`.

| # | Task | What to do | Expected | Result | Note |
|---|---|---|---|---|---|
| L0 | Open and refresh | Open the .pbip, then Home → Refresh | No error messages. Row counts in the Data view: baseline 45, model results 17, historical 360, dictionary 10 | | |
| L1 (UI01) | One audited row | Page 2: select ANH and 2020-21 | Real spending 341.51; properties 2,852.39; per property 119.73; flooding 1.33; pollution 27.65; collapses 6.34; compliance 99.29 | | |
| L2 (UI02) | All 45 rows | Page 2: clear the filters. On the table, open "…" → Export data → CSV, and save it as `evaluation\v2_page2_export.csv` | Saved (I will compare all 45 rows against the panel) | | |
| L3 (UI03) | Historical unit | Page 4: select Pollution incidents | Chart title reads "Pollution incidents \| incidents per 10,000 km \| blank = not available"; the table's Unit column matches | | |
| L4 (UI04) | Missing stays blank | Page 4: Pollution, ANH, 2015-16 | Value blank in the table; no point plotted at zero | | |
| L5 (UI06) | Two outcomes selected | Page 4: Ctrl-click two outcomes | Chart blank; title says "Select exactly one outcome…" | | |
| L6 (UI05) | Model rows fixed | Page 3: change the slicers | Only stored rows are filtered; the labels read in plain English; "Companies (clusters)" shows 9 for the main models | | |
| L7 | Plain labels | Look at the headers on pages 2–5 | No underscores or raw names such as effect_10pct | | |
| L8 | Series labels | Page 1 | Company codes appear at the line ends (if not, note it: the setting may be unsupported) | | |
| L9 (UI08) | Keyboard | Page 1: press Ctrl+F6 to reach the canvas, then Tab repeatedly | Focus moves title → slicers → charts → notes in a sensible order | | |
| L10 (UI08) | Alt text | Select a chart; Format → General → Alt text | Alt text present | | |
| L11 (UI08) | Legibility | View at 100% zoom on your screen | Titles and table text readable without zooming in | | |
| L12 (UI10) | Save and reopen | File → Save as `powerbi\v2\Wastewater_Review_v2.pbix`; close; reopen the .pbix | Opens on page 1 with filters cleared and all five pages present | | |

When finished, tell me and I'll compare the exported CSV and update the evaluation log.
