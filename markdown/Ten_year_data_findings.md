# Ten-year expenditure and outcomes: what the data can support

**Date:** 18 November 2026.
**Evidence:** `ten_year_checks.py`, which writes `overlap_checks.csv` and `botex_coverage.csv`. It reads the retained files without changing them.

## Why the current ten-year attempt is stuck

The validated five-year series is WCPR actual **totex** for wastewater network plus (APR 4C.5, item B0143TAWWNP).
- The WCPR file does contain rows for 2017-18 to 2019-20, but they are empty for all nine companies. Network plus did not exist as a separate price control before 2020.
- The 2015/16–2019/20 figures that were extracted from APR PDFs were built from table 4E service components. They cannot be certified as equivalent to 4C.5.
- There is no year in which both definitions were published, so the gap between them cannot be measured.

Joining the two series would therefore combine two different definitions, and no year exists in which to test whether they match.

## Different route: one definition for every year

Ofwat's **PR24 cost-assessment master dataset** for wholesale wastewater base costs (v4, April 2023) is already in `Data/Ofwat_verified_2026-11-13/`. Ofwat built it for its own econometric benchmarking, so the definition is consistent across years.

| Item | Coverage in the retained v4 file |
|---|---|
| Wastewater network plus **botex** (base operating plus capital maintenance spending), £m in 2017-18 CPIH prices | 2011-12 to 2021-22, all nine companies (99 of 99 values) |
| Connected properties | Same years and companies |

### Checks against the validated WCPR baseline (overlap years 2020-21 and 2021-22, 18 company-years)

- **Connected properties:** identical for 7 of 9 companies.
  - SVE is +1.9% higher, because the cost-assessment dataset combines Severn Trent with Hafren Dyfrdwy (code SVH) to keep a constant boundary.
  - SWB is −2.0% lower.
  - Both differences are known boundary effects and must be documented.
- **Botex as a share of totex:** between 0.59 and 0.92, depending on the company and year. Botex is therefore a **different variable** from totex: it excludes enhancement spending. Using it changes the explanatory variable and is not a substitute for totex.
- **A defect in Ofwat's own file:** the `F_Outputs_S` sheet's 2021-22 column repeats the 2012-13 values. The `F_Outputs_prep (PQ)` sheet holds the genuine values, and the script uses that sheet.

### Extending the series to 2024-25

- Ofwat's PR24 final determinations (December 2024) added **2023-24 outturn** to the base-cost dataset. The feeder models and Stata files are on Ofwat's "Final determinations models" page. They have **not yet been downloaded or checked**.
  - If they cover 2011-12 to 2023-24 on the same definition, botex is available for **2015/16–2023/24 (9 years)**.
- **2024-25** is not in any cost-assessment dataset identified so far. It could be reconstructed from the 2024-25 APR tables, using a rule that is first validated on 2022-23 and 2023-24, where both sources exist. If the rule does not reproduce those years within tolerance, 2024-25 stays out of the botex models.

## Outcomes over ten years (PR24 historical performance trends V6.0, retained)

| Outcome | Complete for all 9 companies | Gaps |
|---|---|---|
| Internal sewer flooding | 2016/17–2024/25 (9 years) | 2015/16: 0 of 9 |
| Sewer collapses | 2017/18–2024/25 (8 years) | 2015/16 and 2016/17: 2 of 9 each |
| Pollution incidents | 2017/18–2024/25 (8 years) | 2015/16 and 2016/17: 0 of 9 |
| Treatment compliance | 2017/18–2024/25 (8 years) | 2015/16 and 2016/17: 7 of 9 each |

The long-term trends file has internal flooding for all 10 years, but it is a different release and would be kept separate.

Missing outcome years cannot be filled in. A ten-year panel would therefore be **unbalanced**: about 8–9 usable years per outcome. That is still far more than the current 5.

## Options

| Option | Expenditure variable | Years in models | Evidence still needed | Risk |
|---|---|---|---|---|
| **A. Consistent base-cost panel (recommended)** | Network plus botex, one Ofwat definition | Flooding 2016/17–2023/24 (8 years); others 2017/18–2023/24 (7 years); up to 2024/25 if the bridge passes | Download and check the final-determination base-cost data (2022-23, 2023-24); optional validated 2024-25 bridge | Low to moderate; one source, consistent definition |
| B. Join totex series | 4E components for 2015–20 joined to WCPR 4C.5 for 2020–25 | 2015/16–2024/25 | Extract about 45 more APR PDFs for 2020–25 to build one component definition for all years | High; still a self-built definition, and much extraction work before 7 January |
| C. Keep the current design | WCPR totex | 2020/21–2024/25 | None | Low, but the ten-year aim is lost |

**Why A:**
- It is the only route in which one published definition covers almost every year, and in which the overlap with the validated baseline can be checked.
- It keeps the five-year totex models as a sensitivity comparison.
- It gives a stronger story for the report: spending to *maintain* the network (botex) is closer to collapses and flooding than total spending that includes enhancement programmes.

**What option A changes:**
- The explanatory variable becomes "wastewater network plus base expenditure". The aim, RQ2, Chapters 1–4, the requirements and the decision log all need updating.
- Severn Trent appears as SVH (including Hafren Dyfrdwy) in the expenditure data.

## Update, later on 18 November 2026: final-determination data adopted

Ofwat's PR24 final-determination model CA08 was downloaded with the student's approval. It supersedes the v4 dataset described above.

- **Definition:** a single definition of wastewater network-plus *modelled base costs*, restated by Ofwat for 2011-12 to 2023-24 (actual years) in 2022-23 prices.
- **Forecast years:** values for 2024-25 onwards are forecasts and are excluded.
- **Main analysis:** a balanced panel for 2017-18 to 2023-24 (63 company-years).
- **Where to find the details:** decision D-2026-11-18c in the decision log, and `code/wastewater_analysis.py` with its outputs in `outputs/`.
- **Retired script:** the earlier evidence script `ten_year_checks.py` is not in the project repository, because its checks are now part of the main analysis (checks T01, T02, T05 and T08).
