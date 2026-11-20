# R12a evaluation log: Power BI artefact

**Artefact checked:** `powerbi/v1_2026-11-16/Wastewater_Review.pbip`, the saved report definition and semantic model, together with the CSV files it loads.
**Evaluator:** researcher. This is a self-evaluation, not an independent user study.
**Date:** 18 November 2026.
**Method:** static inspection of the PBIP definition with `inspect_pbip.py` and checks of the source data. No file in the review package was changed.

Status codes:
- **PASS:** the evidence meets the acceptance test.
- **PARTIAL:** the evidence meets part of the test.
- **FAIL:** the evidence contradicts the test.
- **LIVE:** the check needs Power BI Desktop.

## Static and data checks (run 18 Nov 2026)

| Task / req. | Check | Evidence | Result |
|---|---|---|---|
| UI01 (data) | ANH 2020-21 values in the loaded table | `baseline_panel.csv`: £341.514m (2017/18 prices); 2,852.389k properties; £119.73 per property; flooding 1.332; pollution 27.650; collapses 6.337; compliance 99.29%. A Desktop match at displayed precision was recorded on 16 Nov. | PASS (data); LIVE recheck pending |
| UI02 (data) | All 45 keys unique; derived intensity correct | 45 rows with 45 unique company-year keys. Spending per property was recomputed for all 45 rows with 0 mismatches. The visuals bind directly to these columns. | PASS (data); LIVE export comparison pending |
| UI03 | Pollution shows its unit and calendar basis | Page 1 chart title: "Pollution \| per 10,000 km \| calendar year". The text box explains the calendar-year label. | PASS on page 1 |
| UI03 / R10 | Unit shown for the historical outcome chart (page 4) | The chart title says to read the definition below, but the table on page 4 has no unit column. | **PARTIAL**: unit not shown on page 4 |
| UI04 | Missing values stay blank, never zero | 45 missing historical values are all blank and flagged unavailable; there are 0 zero values. A Desktop check on 16 Nov kept the ANH 2015-16 pollution value blank. | PASS |
| UI05 | Model results are not refitted by observation filters | `model_results` has no relationship to any other table, and page 3's text states that filters select stored results only. | PASS |
| UI06 | Selecting several metrics never adds unlike units | The historical measure returns BLANK unless exactly one metric is selected. The baseline pages use one measure per outcome. | PASS |
| UI07 / R10 | Every page shows source, unit, price basis and period | See the page checklist below. | **PARTIAL** |
| R10 | Every estimate is shown with its interval | Page 3 shows the lower and upper interval bounds, n and the bootstrap p-value. The number of company clusters is not displayed, although it is in the data. | PARTIAL |
| R07 | No causal wording in outputs | The page 3 table shows raw column names, including **`effect_10pct`**. "Effect" is causal wording. | **FAIL** |
| R06 / readability | Plain-language labels | The tables show raw field names such as `sewer_flooding_rate` and `wcr11_p_zero`, with no display names set. | **FAIL** |
| UI08 (static) | Alt text on visuals | 0 of 18 non-text visuals have alt text. | **FAIL** |
| UI08 (static) | Keyboard tab order | Tab-order values are duplicated: all slicers are 2 and all charts are 3. The focus order is therefore ambiguous. | **PARTIAL** |
| UI08 (static) | Colour is not the only signal | Each company is one coloured line among nine on each chart, so colour is the only way to tell companies apart. | **PARTIAL**: needs labels or tooltips |
| R13 | Export view | Not built (Could priority). | Not started |

### Page checklist for R10 (source / unit / price basis / period)

| Page | Source named | Units | Price basis | Period |
|---|---|---|---|---|
| 1 Company trends | Yes (WCPR) | Yes (chart titles) | Yes | Yes, including the calendar note |
| 2 Audited values | No | Yes | Yes | Reporting year only; no calendar note |
| 3 Adjusted findings | No | Rate difference stated, but per-outcome units not shown | n/a | Not stated |
| 4 Historical outcomes | Yes (PR24 V6.0) | **No** | n/a | Yes (start and end dates) |
| 5 Definitions and limits | Not in the table (`source_item` exists but is not displayed) | Yes | Stated in text | Yes |

## Fixes indicated

These need edits to the report, which should be made in a new report version. The 16 Nov package is frozen by checksums.

1. **Set display names on every table column.** For example, `effect_10pct` becomes "Rate difference for +10% spending" and `wcr11_p_zero` becomes "Bootstrap p-value". This fixes the R07 failure and the readability failure.
2. **Add alt text to all 18 non-text visuals.**
3. **Set a unique tab order on each page:** title, then slicers, then charts, then notes.
4. **Show the unit on page 4.** Relate `historical_outcomes[metric]` to `metric_dictionary[metric]` (the names match exactly) and add a unit card or a dynamic title.
5. **Add the missing context to pages 2 and 3.** Page 2 needs a one-line source and period note; page 3 needs the clusters column and per-outcome units.
6. **Add a second signal besides colour on the company line charts,** such as end-of-line data labels or a company highlight slicer.

## Live checks still needed (Power BI Desktop)

- **UI01:** confirm the ANH 2020-21 values in the rendered report.
- **UI02:** export the page 2 table and compare all 45 rows.
- **UI08:** keyboard navigation and focus order, plus legibility at 100% zoom.
- **UI09:** depends on interpretation; it belongs to the user study (R12b).
- **UI10:** close and reopen the PBIX, then confirm the default filters and content.

---

## Version 2 fixes (built 18 Nov 2026)

**Built by:** `code/build_powerbi.py`, starting from the frozen 16 Nov PBIP.
**Output:** `powerbi/v2/Wastewater_Review.pbip`.

### Changes

1. **Plain-language labels** on every table column, slicer and axis field. `effect_10pct` is now "Rate difference for +10% spending" and `wcr11_p_zero` is now "Wild-bootstrap p-value".
2. **New calculated columns:**
   - model results: Outcome name, Unit, Model specification;
   - historical outcomes: Outcome name, Unit.
   The slicers on pages 3 and 4 now use these readable names.
3. **Alt text** on all 18 non-text visuals.
4. **Tab order** is unique on every page, running top-to-bottom and then left-to-right.
5. **Page 4:** a Unit column is added to the table, and the chart title is now a dynamic measure ("Historical chart title") that shows the selected outcome and its unit.
6. **Page 2:** the header now names the source (Ofwat WCPR 2024-25) and states the calendar-year basis.
7. **Page 3:** the header now names the source and states that values are in each outcome's own unit. A "Companies (clusters)" column is added.
8. **Page 5:** the "Ofwat source item" column is added.
9. **Line charts:** series labels are turned on, so each company line is named on the chart and colour is not the only signal.

### Static re-check of version 2

| Check | Result |
|---|---|
| Causal wording in labels | PASS: no label contains "effect" |
| Raw field names shown | PASS: every bound column has a display name |
| Alt text | PASS: 18 of 18 |
| Tab order | PASS: unique on all five pages |
| Source, unit and period on every page | PASS on the report definition (the page checklist is now met on pages 2–5) |

**Not yet verified:** that Power BI Desktop accepts the new model columns, the dynamic title and the `seriesLabels` setting, and that version 2 refreshes. The live checks below cover this.

## Live checks for version 2 (to be run by the researcher in Power BI Desktop)

The steps and the results table are in `PowerBI_live_check_sheet`.

---

## Version 3 (built 18 Nov 2026)

v3 replaces v2 and is generated by `code/build_powerbi_v3.py`.

**Build-time static checks: all passed.**
- **Fields:** all bound fields exist in the model.
- **Titles and alt text:** all 19 data visuals have both.
- **Tab order:** unique on every page.
- **Labels and units:** plain-language labels and units throughout.
- **Traceability:** each page header names its research questions, objectives and requirements.
- **Portability:** a single `DataFolder` parameter makes the dashboard portable.

**Still needed:** the live checks in Power BI Desktop (L0–L14), recorded in `PowerBI_live_check_sheet`.

### Live checks in Power BI Desktop (18 Nov 2026, run by Claude with Computer use)

| Check | Result |
|---|---|
| L0: open, refresh, row counts (72 / 360 / 20 / 3 / 40 / 6) | PASS |
| L1: Anglian Water 2020-21 values | PASS |
| L2: export of all 72 rows compared with `pbi_panel.csv` (largest difference 0.0005, display rounding) | PASS |
| L3: dynamic title shows the unit | PASS |
| L4: missing years stay blank, not zero | PASS |
| L5: two outcomes selected gives an empty chart and an instruction | PASS |
| L6: "Main model" filter gives 3 rows (72 company-years, 9 companies) | PASS |
| L12: research-question tags on every page header | PASS (seen on all six pages) |
| L13: definitions page | PARTIAL; text cut off, fixed (F5) |

**Problems found in the live checks and fixed in the build script:**
- **F1:** number formats (properties showed "2756272.000").
- **F2:** each slicer showed its name twice.
- **F3:** main models were not listed first; the table title said "all 20" even when filtered.
- **F4:** the plain-language message on page 4 was cut off.
- **F5:** long notes on page 6 were cut off.
- **F6:** the coverage column was cut off.
- **F7:** the theme drew smoothed (curved) lines, which imply values between years; replaced with straight lines and point markers, and the automatic subtitles removed.

F1, F2, F3, F6 and F7 were confirmed fixed in Desktop after a rebuild.

### Second live session (18 Nov 2026, Claude with Computer use)

| Check | Result |
|---|---|
| Page 4 re-check (F4) | PASS: all three plain-language sentences are fully visible |
| Page 6 re-check (F5) | PASS: all six definitions are visible with no horizontal scroll. Minor: the sources table needs a small scroll for its sixth row |
| L8: series labels | PASS: company codes label the line ends on page 1, and line markers add a second cue besides colour |
| L9: keyboard order | **Found and fixed (F8).** Power BI's Selection pane showed tab order running bottom-to-top, because Power BI visits the highest `tabOrder` first. The numbering was reversed and the fix confirmed in the Selection pane: header → tables → note |
| L10: alt text | PASS: present in Power BI's Format pane (General → Alt text) |
| L11: legibility | Improved (F9): header and table text enlarged (tables 11 pt). At this laptop's 1456×819 display, fit-to-page shows the canvas at 63%; titles and tables are readable, while the small header context lines remain small |
| L14: save and reopen | PASS: saved as `powerbi/v3/Wastewater_Dashboard.pbix` (117 KB); reopened with all six pages and the data embedded, so no refresh is needed. It opens on the last active page |

**Status:** all checks L0–L14 have been run. Every one passes after fixes F1–F9, except for one minor cosmetic point: the sources table on page 6 needs a small scroll.

---

## Heuristic review and colour-contrast check (R12a), 20 Nov 2026

**Method:**
- **Heuristic review:** dashboard v3 was inspected page by page in Power BI Desktop against Nielsen's (1994) ten usability heuristics. Each problem was rated on Nielsen's severity scale: 0 = not a problem, 1 = cosmetic, 2 = minor, 3 = major, 4 = catastrophe.
- **Contrast check:** colour contrast was computed against WCAG 2.1 (W3C, 2018) by `code/check_contrast.py`, which writes `outputs/contrast_check.csv`.
- **Who did it:** the review was carried out with AI assistance and checked by the researcher. It is an expert review, not a user study.

### Heuristic review

| # | Heuristic | Evidence | Problem found | Severity | Action |
|---|---|---|---|---|---|
| H1 | Visibility of system status | Selections stay visible in slicers. Header names data sources | Outcome data release date not shown | 1 | Fixed (F12): "V6.0 (Jan 2026)" added |
| H2 | Match with the real world | Plain labels, units, "lower is better" | Statistical terms on page 3 (CV3, wild-bootstrap p-value) | 2 | Mitigated: "How to read this page" box; kept for specialists |
| H3 | User control and freedom | Slicer selections can be cleared | No one-click reset in Desktop | 1 | None |
| H4 | Consistency and standards | Same header pattern, slicer position and unit-in-title on all six pages | None | 0 | None |
| H5 | Error prevention | Two outcomes cannot be combined. Filters cannot refit models | None | 0 | None |
| H6 | Recognition rather than recall | Chart lines labelled with three-letter codes | Codes had to be remembered; long names were cut off in narrow slicers | 2 | Fixed (F11): slicers and tables show "ANH – Anglian Water", code first so it stays visible |
| H7 | Flexibility and efficiency | Slicers, table export | None | 0 | None |
| H8 | Aesthetic and minimalist design | Nine lines per chart; 12-column table on page 3 | Visual density | 2 | Mitigated: company slicer, "Type of result" filter, main models listed first |
| H9 | Recognise and recover from errors | Empty chart explains itself ("Select exactly one outcome") | None | 0 | None |
| H10 | Help and documentation | Definitions page, reading notes, README | No in-report link to help | 1 | None |

**No problem was rated major (3) or catastrophic (4).**

### Colour contrast (WCAG 2.1)

| Element | Result |
|---|---|
| All text colours (5) | PASS: 6.19:1 to 15.52:1 against white (4.5:1 needed, WCAG 1.4.3) |
| Company line colours (9) | 8 PASS. United Utilities' yellow (#D9B300) was 2.02:1, below the 3:1 needed for graphics (WCAG 1.4.11) |

**F10 fix:** United Utilities is now drawn in a darker gold (#9A7B00, 4.03:1).

Changing the theme file stopped the report loading in Desktop, so each company's colour is instead set explicitly on every line chart. A single override had shifted the other companies' colours, which is why all nine are set.

**Re-test in Desktop:**
- every company colour is correct;
- the slicers show "ANH – Anglian Water";
- all 14 colour checks pass;
- the `.pbix` was re-saved.

**Remaining limits:** H2 and H8 at severity 2; small header text at 63% zoom (L11).
