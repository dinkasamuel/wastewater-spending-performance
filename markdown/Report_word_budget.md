# Report word budget

Prepared 18 November 2026. Limit: 5,000–6,000 words. The abstract, references and appendices are excluded. Target: **5,800 words**, which leaves 200 words of margin.

**To confirm with the supervisor:** whether tables, figure captions and headings count toward the limit. The current counts below include table text. If tables are excluded, there is more room.

## Where the preliminary draft stands

| Current chapter | Words now |
|---|---:|
| 1 Introduction | 1,230 |
| 2 Literature review | 1,885 |
| 3 Feasibility | 1,599 |
| 4 Requirements | 791 |
| 5 Conceptual design | 842 |
| **Total (Ch 1–5)** | **≈6,350** |

The draft already exceeds the whole-report limit, before Implementation and Results are written.

## Budget by required section

The order follows the supervisor's feedback of 3 October. The weights follow the marking criteria.

| # | Section | Budget | Criteria served (marks) | Change from current |
|---|---|---:|---|---:|
| 1 | Introduction and scope | 500 | Rationale/scope/objectives (5) | −730 |
| 2 | Research (literature review) | 1,300 | Literature review (20); Novelty (10) | −585 |
| 3 | Feasibility study | 450 | Design and approach (15) | −1,150 |
| 4 | Design: requirements, UML, ethics by design | 1,000 | Design and user requirements (15); Ethics (10) | −630 |
| 5 | Implementation | 800 | Implementation (15) | new |
| 6 | Results (RQ1–RQ3) | 900 | Implementation (15); Novelty (10) | new |
| 7 | Evaluation and reflection (incl. RQ4, ethics review, planning/supervision) | 700 | Evaluation/reflection/planning (15); Ethics (10) | new |
| 8 | Conclusion | 150 | Presentation (10) | new |
| | **Total** | **5,800** | | |

The literature review keeps the biggest share because it carries the most marks. The feasibility section takes the largest cut, because its detail is evidence rather than argument and fits naturally in an appendix.

## What moves out of the body

| Appendix | Content | Source |
|---|---|---|
| A | Ethics review (A.1–A.4) and AI-use disclosure | To write; UWE ethics guidance |
| B | Full requirements register (R01–R14), dependency diagram, traceability matrix (requirement → UML element → artefact location → RQ/objective) | Ch 4 table; `docs/requirements_and_traceability.csv` |
| C | Data coverage, operational definitions, integration-risk controls | Ch 3 tables 3.1–3.2 and §3.3–3.6 |
| D | Source reconciliation and the financial-definition decision (why 2015–2020 spending is excluded) | `Financial_definition_decision.md`, `Reconciliation_findings.md` |
| E | Model specifications and all 17 results, sensitivity tables, diagnostics | `results/`, `fact_model_results.csv` |
| F | Power BI page guide and validation checks | `powerbi/Desktop_validation.md` |
| G | Project plan, Gantt chart and supervision log | `Supervisor_Progress_Note.md`, Gantt preview |
| H | Code repository guide and how to rerun the analysis | Review-version `README.md` |

## Section-by-section cutting guide

**1 Introduction (1,230 → 500).**
- Merge 1.1 and 1.2 into one problem statement (about 200 words).
- Reduce 1.3 (scope development) to one sentence; the story belongs in the reflection.
- Keep the aim, the objectives and RQ1–RQ4 almost as they are; they are the traceability anchors.
- Reduce 1.7 to the key boundaries and 1.8 to a two-line roadmap.

**2 Research (1,885 → 1,300).**
- Keep 2.3–2.6 and 2.8, because they justify design decisions. Trim each by about 25%.
- Reduce 2.7 (Mukherjee and Jensen) to one sentence.
- Merge 2.1 into the introduction to the chapter.
- Combine 2.9 and 2.10 into a single "gap and conceptual framework" section. It must name the gap explicitly, so that Results and Evaluation can show it has been covered (supervisor point 3).

**3 Feasibility (1,599 → 450).**
- Keep one summary paragraph on each of: data, analysis, technical, and delivery feasibility.
- Keep the coverage table only if tables are excluded from the count; otherwise move it to Appendix C.
- State the 16 November decision (five-year modelling window) here as a feasibility result.

**4 Design (1,633 → 1,000).**
- Explain how the requirements were derived, then show a short table of the "Must" requirements; the full register goes to Appendix B.
- Add the three UML diagrams that already exist (component, activity, use case) and map each requirement to a UML element (supervisor point 2).
- Write a short ethics-by-design paragraph: how ethical choices shaped the design, such as no causal language, showing missing values, and not ranking companies.

**5 Implementation (800, new).**
- Cover the pipeline stages, the validation checks, the modelling approach (company and year effects, CV3 intervals, wild-cluster bootstrap) and the Power BI build.
- Point to the RQ/objective tags in the notebook (supervisor point 1).

**6 Results (900, new).**
- Answer RQ1, RQ2 and RQ3 in turn, with one key figure or table each. The full tables go to Appendix E.

**7 Evaluation and reflection (700, new).**
- Data, analytical and artefact evaluation, against the acceptance tests.
- RQ4: how well the dashboard communicates the results.
- Limitations and an honest reflection, including the change of scope and the expenditure-reconciliation setback.
- Use of supervision.

**8 Conclusion (150, new).**
- One answer per research question, and future work.

## Checkpoints

| Date | Check |
|---|---|
| 27 Nov | Sections 1–4 condensed to ≤3,250; Implementation drafted |
| 11 Dec | Results drafted; running total ≤5,000 |
| 18 Dec | Evaluation and conclusion drafted; total ≤5,800 |
| ~24 Dec | Supervisor's last draft-reading date (2 weeks before submission) |
