# 3 Feasibility study

Feasibility was assessed against the research questions and the retained source files. The full audit tables appear in Appendices C and D. Record counts reported here are exact for the inspected files; they describe completeness, not measurement accuracy.

## 3.1 Outcome and scale data

Outcomes come from Ofwat's historical performance trends for PR24 (Ofwat, 2026), a single release covering 2015/16–2024/25.

- **Completeness.** Every modelled outcome is complete for all nine companies from 2017/18. Earlier years are patchy; for example, sewer collapses have data for only 2 of 9 companies in 2015/16. Missing values are never filled in.
- **Units.** Flooding is measured per 10,000 connections, collapses per 1,000 km of sewer and pollution per 10,000 km of sewer.
- **Timing.** Pollution and compliance are calendar-year measures, so each record carries its measurement period as well as its reporting label (Environment Agency, 2025b).

The Water Company Performance Report (WCPR) data for 2020/21–2024/25 (Ofwat, 2025b) provide total expenditure, properties and outcomes for comparison. All 270 selected values equal Ofwat's companion workbook (Ofwat, 2025c).

## 3.2 A consistent spending series: a feasibility result

The study first tried to extend total expenditure back to 2015/16. Spending components for the 45 earlier company-years were extracted from historical Annual Performance Reports and passed 1,111 arithmetic checks.

They could not, however, be shown to match the current measure, which Ofwat's table guidance defines through table 4C (Ofwat, 2025d). Network plus became a separate price control only in 2020, so no year was published under both definitions. A join between the two series therefore could not be tested.

The study instead adopted Ofwat's PR24 base-cost data. They restate wastewater network-plus base expenditure on **one definition for every year from 2011/12 to 2024/25**. The main source is the dataset Ofwat republished in October 2025 for the Competition and Markets Authority appeals, which adds companies' actual 2024/25 figures (Ofwat, 2025e). For 2011/12–2023/24 it is identical to the December 2024 final-determination file (Ofwat, 2024). Three checks support the series:

- **Properties.** The dataset's connected-property counts equal the WCPR figures for seven of nine companies in 2020/21–2024/25. Severn Trent is 0.5–1.9% higher, because the series includes its Welsh arm, Hafren Dyfrdwy (about 1% of its base costs). South West Water differs by up to 2.0% in two years.
- **Actuals, not forecasts.** The 2024/25 property counts equal the actual WCPR counts. The December 2024 file's 2024/25 figures, by contrast, were forecasts. Figures from 2025/26 onwards are forecasts and are excluded.
- **Reproduction.** The analysis code reproduces the earlier five-year results exactly, confirming that the change of series did not alter the method.

Combining base expenditure with the outcome coverage gives a **balanced panel of 72 company-years (2017/18–2024/25)**, 60% more than the earlier five-year design.

## 3.3 Analytical and technical feasibility

The panel supports descriptive comparison and a restrained association analysis with company and year effects. Base expenditure exists back to 2011/12, so lagged comparisons do not shorten the outcome window. Nine company clusters limit precision; a minimum-detectable-effect calculation makes that limit explicit rather than leaving it implicit.

Python handles extraction, validation and modelling, and Power BI handles presentation. A database layer was judged unnecessary for a dataset of this size.

## 3.4 Delivery feasibility

The work follows its dependencies in order: definitions, then the validated panel, then analysis, then the dashboard, then evaluation. This prevents visuals from being built on fields whose meaning later changes.

All sources are public Ofwat publications. The essential artefact is a code repository with reproducible outputs and a local Power BI file; online publication is optional. The project is feasible, and its remaining risks concern interpretation rather than data availability.
