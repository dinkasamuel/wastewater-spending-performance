# Wastewater spending and sewer performance in England: project briefing

**MSc Data Science dissertation, UWE Bristol** · Dinka Christabel Samuel · status as of 20 November 2026

Project repository: https://github.com/dinkasamuel/wastewater-spending-performance

## 1. The question (Chapter 1)

Water companies spend billions running and maintaining England's sewers. Regulators and bill payers want to know whether that spending buys better service. Ofwat's own review of 2020–25 found uneven progress: internal sewer flooding improved, but pollution remained a concern.

Comparing spending totals cannot answer the question fairly, for three reasons:

- **Size.** Bigger companies spend more simply because they are bigger.
- **Reverse cause.** Companies may spend *because* something failed, not to prevent failure.
- **Timing.** Benefits may arrive years after the money is spent.

The project therefore asks a careful question: **when a company spends more than its own usual amount on its wastewater network, do sewer flooding, sewer collapses and pollution incidents change?** It covers England's **nine water and sewerage companies**. The answer is presented through an interactive dashboard that an informed non-specialist can understand.

| # | Research question |
|---|---|
| RQ1 | How have spending and outcomes changed across the companies and years? |
| RQ2 | Is more spending associated with fewer problems, once company size, permanent company differences and shared yearly conditions are allowed for? |
| RQ3 | How robust is that answer to the spending measure, timing and individual companies? |
| RQ4 | Can a dashboard communicate this, including its limits, to a non-specialist? |

The project measures **associations, not cause and effect**. It does not rank companies or forecast, and it makes no investment recommendations.

## 2. What existing research tells us (Chapter 2)

Previous studies of English and Welsh water companies focus on **cost efficiency**, on **drinking water** rather than wastewater, and on periods **ending by 2019**. Regulators publish spending beside performance but do not test the link between them. The review identified three gaps:

- **G1 Scope:** no reviewed study examines wastewater network spending outcome by outcome, for England's companies, over the recent period.
- **G2 Robustness:** no reviewed study combines methods built for small samples with checks on the spending measure, timing and individual companies, or says how large a link its data could detect.
- **G3 Communication:** the regulatory publications do not estimate the link or show its uncertainty.

Each gap is traced through to a specific part of the finished artefact.

## 3. Can it be done? The data journey (Chapter 3)

This is where the project changed most, and the change is part of the story.

1. **The first plan** used ten years of *total* spending (2015–2025). Earlier figures were extracted from 45 company annual reports and passed 1,111 arithmetic checks. They still could not be joined to the modern figures. Ofwat only began reporting the "network plus" spending category in 2020, and no year was published under both definitions, so a joined series could never be tested.
2. **The fix:** Ofwat's own price-review dataset restates **base spending** (running and maintaining existing sewers and treatment works) on **one consistent definition for every year**. Three checks support it:
   - **Property counts agree:** connected properties match the regulator's published figures exactly for 7 of 9 companies, and the other two differences are explained.
   - **Actual 2024-25 figures:** a version Ofwat republished in October 2025 adds companies' actual 2024-25 figures, identical to the earlier release for every other year.
   - **Earlier results reproduced:** the new analysis code reproduces the original five-year results exactly.
3. **The result** is a **balanced dataset of 72 company-years (9 companies × 8 years, 2017-18 to 2024-25)**. That is 60% more evidence than the original design, and every company has every outcome in every year.

All data are public Ofwat publications. Every source file is kept unchanged, with a digital fingerprint (SHA-256 hash) recorded before and after each run.

## 4. How it was designed (Chapter 4)

- **14 requirements**, each prioritised (Must, Should, Could, Won't), linked to the research questions and dependent on each other in a set order.
- **Two UML diagrams.** One shows the **whole project workflow** across four roles (researcher, Python analysis, Power BI dashboard, supervisor), including the real decision points. The other shows every requirement, its purpose, and where it is delivered.
- **Ethics by design:**
  - no causal language;
  - missing data never shown as zero;
  - no company league table;
  - every result shown with its uncertainty.
- **User study:** the planned 3–5 person study needs UWE ethics approval, because the current declaration covers public data only. A full low-risk ethics pack has been drafted.

## 5. What was built (the artefact)

| Component | What it is |
|---|---|
| Analysis code (Python) | Loads and validates the data (15 automatic checks), builds the panel, runs the models and writes the results. Two fresh runs produce byte-identical output. |
| Notebook | The same analysis as an executed walk-through. A blue box on each section names the research question it answers, and a green box states the insight. |
| Dashboard (Power BI) | Six pages: trends; audited values; associations; what can be detected; history and data coverage; definitions and limits. Each page header names the question it answers. It opens with the data built in. |
| Documents | Chapters 1–4, requirements register, decision log, evaluation log, ethics pack and references, in Word and Markdown. |

## 6. What we found

### RQ1: what changed between 2017-18 and 2024-25

| Measure | 2017-18 | 2024-25 | Companies improving |
|---|---|---|---|
| Base spending per property (2022-23 prices) | £136 | £172 (+27%) | All 9 spent more |
| Internal sewer flooding (per 10,000 connections) | 2.76 | 1.67 | 7 of 9 |
| Sewer collapses (per 1,000 km of sewer) | 11.9 | 6.6 | 7 of 9 |
| Pollution incidents (per 10,000 km of sewer) | 33.5 | 53.4 | Only 2 of 9 |

Spending rose across the sector while flooding and collapses fell and pollution worsened. That sector-wide pattern alone does not show that spending made the difference.

### RQ2: comparing each company with itself, with shared yearly conditions removed

| Outcome | Change for 10% more spending | 95% range |
|---|---|---|
| Internal sewer flooding | +0.06 | −0.29 to +0.41 |
| Sewer collapses | −0.22 | −1.58 to +1.14 |
| Pollution incidents | +0.84 | −4.97 to +6.66 |

**There is no clear association in either direction for any outcome.**

### RQ3: the answer holds up

- **No single company drives it:** removing any one company in turn leaves the picture unchanged.
- **Alternative measures agree:** base and total spending give the same answer.
- **Different timing agrees:** pairing outcomes with spending from earlier years gives the same answer.
- **One pattern is worth discussing, not claiming:** last year's spending goes with lower pollution. It is not robust across methods.

### What the data can and cannot detect

With nine companies, the data could only reveal a link of about **a fifth of the average rate for every 10% more spending**. So "no clear link" means **"no large link"**, not "spending makes no difference". Smaller links may exist; nine companies are too few to see them. This is shown openly on the dashboard's "What can be detected" page.

## 7. Quality checks so far

- **Data and code:** 15 automatic checks; reruns are identical; earlier results reproduced exactly.
- **Dashboard:** every acceptance check (L0–L14) was run in Power BI Desktop, and **nine real problems were found and fixed**, including:
  - keyboard order running in reverse;
  - curved lines suggesting values that do not exist;
  - text cut off;
  - number formats.

  The exported dashboard data matches the analysis for all 72 rows.

## 8. What happens next

| When | What |
|---|---|
| Now | Supervisor review of the user study (ethics decision by 4 December) |
| Late Nov – mid Dec | Chapter 5 (Implementation) and Chapter 6 (Results); user study sessions if approved (9–15 Dec) |
| By 22 December | Chapter 7 (Evaluation and reflection), Chapter 8 (Conclusion), appendices; agreed sections to the supervisor |
| 23 Dec – 6 Jan | Reference checks, word count (Chapters 1–4 currently slightly over), final rerun, report assembled |
| 6 January | Submission, a day ahead of the 7 January deadline |

## Bottom line

Over eight years, England's water companies spent about **27% more per property** on maintaining their sewers. Flooding and collapses fell, but pollution worsened. Comparing each company with itself, there is **no evidence of a large link** between spending more and having fewer problems. The tools built to show this are open, reproducible and honest about what nine companies can and cannot reveal.
