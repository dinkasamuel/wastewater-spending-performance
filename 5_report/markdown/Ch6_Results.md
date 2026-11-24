# 6 Results

All figures in this chapter come from the run of 18 November 2026 (`3_results/tables/model_results.csv`). Differences are expressed in each outcome's own unit for 10% more base spending per property. Ranges are 95% CV3 intervals. All results are associations, not causal effects.

## 6.1 Data coverage

The main panel contains 72 company-years: nine companies over eight years, 2017-18 to 2024-25, with no missing values (Figure 6.1). Earlier outcome years are incomplete. For example, sewer collapses have data for only two of nine companies in 2015-16 and 2016-17, and pollution for none. Those years are therefore used only in the unbalanced sensitivity check.

*Figure 6.1 Outcome coverage by year; the red box marks the main window (`3_results/figures/fig_outcome_coverage.png`).*

## 6.2 RQ1: how spending and outcomes changed

Average base spending per property was stable from 2017-18 to 2020-21, then rose to £172 by 2024-25 (Table 6.1). That is 27% above 2017-18 in real terms. All nine companies spent more per property in 2024-25 than in 2017-18. The largest rises were at South West Water (+£99), Southern Water (+£57) and Thames Water (+£54).

**Table 6.1 Unweighted company averages**

| Measure | 2017-18 | 2020-21 | 2024-25 | Companies lower in 2024-25 than in 2017-18 |
|---|---|---|---|---|
| Base spending per property (£, 2022-23 prices) | 135.7 | 135.3 | 172.1 | 0 of 9 (all spent more) |
| Internal sewer flooding (per 10,000 connections) | 2.76 | 2.21 | 1.67 | 7 of 9 |
| Sewer collapses (per 1,000 km) | 11.89 | 9.09 | 6.58 | 7 of 9 |
| Pollution incidents (per 10,000 km) | 33.52 | 39.58 | 53.39 | 2 of 9 |

Flooding and collapses fell across most companies, but pollution rose to its highest level in the period. Company paths differ widely (Figure 6.2). Yorkshire Water's collapse rate fell from 26.8 to 7.0 per 1,000 km. Southern Water's pollution rate peaked above 100 incidents per 10,000 km in 2019.

Rising spending alongside falling flooding and collapses is a sector-wide pattern. On its own it does not show that the two are linked, because both may follow shared trends. RQ2 addresses this.

*Figure 6.2 Company trajectories, 2017-18 to 2024-25 (`3_results/figures/fig_company_trends.png`).*

## 6.3 RQ2: associations after adjustment

**Table 6.2 Main models (72 company-years, nine companies)**

| Outcome | Difference for +10% spending | 95% range | Bootstrap p | Holm-adjusted p |
|---|---|---|---|---|
| Internal sewer flooding | +0.06 | −0.29 to +0.41 | 0.68 | 1.00 |
| Sewer collapses | −0.22 | −1.58 to +1.14 | 0.72 | 1.00 |
| Pollution incidents | +0.84 | −4.97 to +6.66 | 0.78 | n/a |

Comparing each company with itself and allowing for shared yearly conditions, **there is no clear association between base spending and any outcome**. Every range includes zero, and none of the bootstrap tests gives evidence against zero. The point estimates are also small relative to average rates: the flooding estimate is 3% of the average flooding rate, and the collapse estimate 2% of the average collapse rate.

## 6.4 RQ3: sensitivity

The conclusion holds across every planned check (Figure 6.3):

- **Influential companies.** Leaving out each company in turn keeps every estimate close to the main result. The ranges are −0.05 to +0.14 for flooding, −0.53 to +0.26 for collapses and −1.34 to +2.12 for pollution.
- **Sample and scale.** The unbalanced panel (81 and 76 company-years for flooding and collapses) and the model with total spending and size entered separately give the same picture. Every interval includes zero.
- **Timing.** Spending one year earlier gives −0.12 for flooding and −0.12 for collapses. For pollution, last year's spending gives −2.12 (range −4.83 to +0.59). Its bootstrap p-value is 0.02, and all nine leave-one-out estimates are negative. However, the CV3 interval includes zero, the two inference methods disagree, and it is one of 20 specifications, so it is treated as a pattern for discussion, not a finding. Spending two years earlier, which wholly precedes the calendar-year outcome, gives −0.07.
- **Spending measure.** On the same 45 company-years (2020-21 to 2024-25), neither base nor total spending shows a clear association with any outcome.
- **Reproduction.** The earlier five-year total-spending design is reproduced exactly (+0.013 for flooding, +0.311 for collapses).

*Figure 6.3 All 20 estimates with 95% ranges; the shaded band marks the range the main model cannot reliably detect (`3_results/figures/fig_association_estimates.png`).*

## 6.5 What the data can detect

The minimum detectable effects explain what "no clear association" means here (Table 6.3).

**Table 6.3 Smallest association detectable with 80% power (main models)**

| Outcome | Average rate | Detectable difference for +10% spending | As % of average |
|---|---|---|---|
| Internal sewer flooding | 2.23 | 0.49 | 22% |
| Sewer collapses | 8.97 | 1.88 | 21% |
| Pollution incidents | 39.19 | 8.06 | 21% |

With nine companies, only an association of about a fifth of the average rate per 10% more spending would reliably be detected. The results therefore show the **absence of a large link**, not proof that spending makes no difference. Smaller associations may exist but cannot be distinguished from noise with nine companies.

## 6.6 Summary against the research gaps

- **G1 (scope).** The project provides an outcome-by-outcome analysis of wastewater network base spending for England's nine companies over 2017-18 to 2024-25. It finds no clear association for flooding, collapses or pollution.
- **G2 (robustness).** Few-cluster inference, the sensitivity checks and the detectable-effect calculation show that this conclusion is stable, and they state its resolution: it rules out large links only.
- **G3 (communication).** The dashboard presents these results, their uncertainty and Table 6.3 in plain language. Chapter 7 evaluates it (RQ4).
