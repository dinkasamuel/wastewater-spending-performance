# 7 Evaluation and reflection

The artefact was evaluated at three levels, each against the acceptance tests in the requirements register (Appendix B): the data, the analysis and the dashboard. Full records are in the evaluation log (Appendix F).

## 7.1 Data and analysis

**Checks.** Fifteen automatic checks pass on every run. They confirm three things:
- one spending definition holds across all 117 shared company-years of the two Ofwat cost files;
- every selected WCPR value equals Ofwat's companion workbook;
- the inputs are unchanged by the run.

**Reproducibility.** Two independent fresh runs produced byte-identical outputs, and the earlier five-year design was reproduced exactly. Together these give strong evidence that the code does what Chapter 5 describes. That covers requirements R01–R08 and R11.

**What the checks cannot establish.** Validity is limited in four ways:
- **Association, not cause.** Fixed effects remove permanent company differences and shared yearly conditions, but not conditions that change within a company over time. They also cannot exclude spending that responds to failures (Section 2.7).
- **Resolution.** With nine companies, only associations of about a fifth of the average rate per 10% more spending can be detected (Table 6.3).
- **Measurement.** Base spending excludes enhancement spending. The Severn Trent series includes Hafren Dyfrdwy, about 1% of its costs.
- **Generalisation.** The findings describe England's nine water and sewerage companies over 2017-18 to 2024-25 only.

## 7.2 Dashboard (R09, R10, R12a)

The dashboard went through three evaluation rounds, and each round found real defects:

1. **Static inspection of version 1.** This found causal wording in a column label ("effect"), raw field names, no alt text on any of 18 visuals, an ambiguous keyboard order, and missing units and sources on two pages. All were fixed in version 2.
2. **Live checks of version 3 in Power BI Desktop (L0–L14).**
   - **Data accuracy:** the dashboard loaded the expected row counts in all six tables. An export of its values table matched the analysis for all 72 company-years, with a largest difference of 0.0005 (display rounding).
   - **Behaviour:** missing years stayed blank, and selecting two outcomes produced an instruction instead of a misleading combined line.
   - **Defects:** nine were found and fixed (F1–F9). The two most significant: keyboard focus ran bottom-to-top, because Power BI visits the highest tab number first; and the theme drew smoothed lines, implying values between years that do not exist.
3. **Re-test after the fixes.** All checks pass, with one cosmetic exception: one table needs scrolling for its last row.

**Remaining limitation.** On a 1456×819 laptop screen, the page fits at 63% zoom, and small header text remains hard to read.

**[TO COMPLETE before submission: structured heuristic review against Nielsen's ten usability heuristics and a colour-contrast check (R12a); add the Nielsen reference.]**

## 7.3 User evaluation (R12b) and RQ4

**[TO UPDATE after the supervisor's ethics decision, due 4 December 2026.]**
- **If the study is approved:** report task success, System Usability Scale scores and interpretation accuracy for 3–5 participants.
- **If it is not approved:** state that no participant study took place, because the existing ethics declaration covered public data only and approval could not be obtained in time.

**RQ4 at present.** The evidence answers RQ4 only partly. The dashboard is shown to be accurate, traceable and accessible by design. Whether non-specialists interpret it correctly has not yet been tested with users.

## 7.4 Requirements

| Status | Requirements |
|---|---|
| Met and tested | R01–R11 |
| Partly met | R12a: live checks done; heuristic review and contrast check outstanding |
| Pending ethics | R12b |
| Not attempted | R13 (Could): no export view |
| Respected | R14: no forecast or company ranking is produced |

## 7.5 Reflection

**Data definitions.** The largest lesson was that the data had to be understood before the method. I first tried to build ten years of total spending, extracting and checking 45 annual reports. Only then did I establish that the old and new definitions could never be joined. Recording this as a decision rather than forcing the series kept the analysis defensible. It also led to a better source: Ofwat's single-definition base-cost data, and later a republished version containing 2024-25 actuals. Checking definitions at the start would have saved time.

**Supervision.** Supervision shaped the artefact directly. The 3 October feedback on traceability became the research-question tags in the code, notebook and dashboard, and the requirement–UML links in Figure 4.2. The England-only scope was agreed with my supervisor. Later narrowing, to water and sewerage companies and then to wastewater spending, was recorded in a decision log.

**Ethics and evaluation.** I recognised too late that user testing needs its own ethics approval. Starting that process earlier would have protected RQ4.

**Testing.** Testing the dashboard live, rather than trusting its specification, exposed defects that no static check would have found.

**AI assistance.** Generative AI was used throughout, for drafting, coding and checking. Every result was verified against the data and the outputs (Appendix A).
