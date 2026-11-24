# 1 Introduction

## 1.1 Problem and context

Water and sewerage companies must spend money to operate, maintain and improve their wastewater networks. The amount spent does not, however, establish the service delivered. Ofwat's review of the 2020–25 period reports uneven progress across companies and performance areas: internal sewer flooding improved while pollution remained a concern (Ofwat, 2025a). The National Audit Office (2025) also treats investment, operational delivery and value for bill payers as a single accountability problem.

Comparing spending totals cannot show whether differences in expenditure are associated with differences in performance:

- larger networks need more spending;
- spending can respond to failures rather than prevent them;
- the benefits of spending may arrive after the year in which the money is spent.

This dissertation therefore examines associations, not causal returns or efficiency. It also treats the communication of those associations as a design problem: units, reporting periods and uncertainty must stay visible to the reader.

## 1.2 Aim, objectives and research questions

The aim is to examine the relationship between annual wastewater network-plus base expenditure and selected operational outcomes among England's nine water and sewerage companies over 2017/18–2024/25, and to communicate the evidence through a transparent, reproducible analytical dashboard.

1. Build a documented company-year dataset that links base expenditure, company scale and the selected outcomes, preserving source definitions and reporting periods.
2. Compare expenditure and outcome trajectories across companies and years on consistent financial and measurement bases.
3. Assess expenditure–outcome associations, distinguishing persistent company differences from within-company change and shared annual conditions.
4. Test how sensitive the interpretation is to the spending measure (base or total), expenditure scaling, influential companies and timing assumptions.
5. Develop a Power BI artefact that presents comparisons, relationships, definitions and data-quality information accessibly.
6. Evaluate the artefact's reproducibility, numerical consistency and usability against documented requirements.

**RQ1:** How do base expenditure and the selected outcomes vary across the nine companies between 2017/18 and 2024/25?

**RQ2:** What associations exist between expenditure and each modelled outcome after recognising company scale, persistent company differences and shared annual conditions?

**RQ3:** How sensitive are these associations to the spending measure, influential companies and the timing assigned to expenditure and performance?

**RQ4:** How effectively can a reproducible Power BI artefact communicate these relationships and their limitations to an informed non-specialist?

The questions assume neither a beneficial nor a harmful relationship. A weak or uncertain association is a valid finding.

## 1.3 Scope and boundaries

**Companies and years.** The population comprises the nine water and sewerage companies in the Environment Agency's assessment for England (Environment Agency, 2025a). The main analysis covers 2017/18–2024/25, giving 72 company-years. This is the longest period in which every company reports every modelled outcome, and in which base expenditure is published on a single definition.

**Spending measure.** The explanatory variable is Ofwat's *modelled base expenditure* for wastewater network plus, divided by connected properties (Ofwat, 2025e). Base expenditure is the cost of operating and maintaining existing sewers and treatment works. It excludes enhancement spending on new obligations, so it is not a measure of environmental investment. Total expenditure (totex) for 2020/21–2024/25 is used as a comparison. Bioresources (sludge) spending is excluded from both.

**Outcomes.**
- Internal sewer flooding, sewer collapses and pollution incidents are the modelled outcomes.
- Treatment-works compliance is descriptive context only, because its boundary is wider than network-plus spending.
- Pollution and compliance are measured by calendar year but reported under financial-year labels.

**Out of scope:** causal evaluation, asset-level appraisal, investment recommendations and prediction.

**Structure of the report:** the research context, feasibility, design, implementation and results, followed by the evaluation and the conclusion.
