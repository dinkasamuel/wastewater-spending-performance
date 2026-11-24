# 2 Research

This chapter is a focused critical review, not a systematic one. It draws on peer-reviewed studies published between 2022 and 2026 and on primary regulatory sources. The regulatory sources establish the reporting setting and the variable definitions. The academic studies inform the analytical argument. Each section ends with the design decision the evidence supports.

## 2.1 Regulatory accountability and attribution

The National Audit Office (2025) finds weaknesses in how regulation secures long-term outcomes. It stresses the importance of asset condition, delivery capacity and value for bill payers. An expenditure figure therefore acquires meaning only in relation to the service it supports. The report is a sector-level judgement, however, not an estimate of what an additional pound of a company's annual wastewater spending achieves.

Ofwat (2023) acknowledges that performance improvements are difficult to attribute to enhancement expenditure. Benefits can extend across several performance commitments, and companies adopt different attribution approaches.

Together, these sources motivate the question without answering it. They support a bounded claim: expenditure–performance associations can be examined, but not presented as an evaluation of programme benefits.

## 2.2 Performance is multidimensional

Vilarinho et al. (2024) combine service dimensions into a customer-centred Water Utility Service Quality Index. A composite index is easy to communicate, but it embeds weighting judgements made for a different purpose from wastewater asset and environmental performance. Combining outcomes could also conceal divergence: an improvement in flooding could offset a deterioration in compliance.

This project therefore keeps each outcome separate and assigns no overall company score. The outcomes also differ in direction and unit. Lower flooding, pollution and collapse rates indicate better performance, whereas higher compliance indicates better performance. Coefficients expressed in different units cannot be ranked against one another. The dashboard must show each outcome's unit and its direction of better performance.

## 2.3 Expenditure is not efficiency

Maziotis et al. (2023) compare classical stochastic frontier analysis, Bayesian stochastic frontier analysis and stochastic non-parametric envelopment for Chilean water companies. The three approaches yield different efficiency estimates and even different directions of change. Efficiency judgements therefore depend on the modelling framework, and the Chilean setting limits direct transfer to England.

Maziotis et al. (2024a) link carbon inefficiency and energy overuse to production costs in English and Welsh drinking-water services over 2010–2019. Their work shows that environmental and economic performance should not be treated independently. Drinking-water production costs are, however, a different construct from wastewater-network expenditure, so their estimates cannot indicate an expected wastewater relationship.

Mukherjee and Jensen (2022) add that institutional and information processes, not only finance, shape service outcomes. Their evidence comes from retail competition rather than sewer assets.

Without a defensible benchmark of outputs and operating conditions, this study does not label low expenditure as efficient or high expenditure as wasteful. It asks a narrower question: how is an observed spending measure associated with observed outcomes? This is more defensible than presenting a spend-per-incident ratio as a measure of value for money.

## 2.4 Company heterogeneity and the limits of comparison

Maziotis and Molinos-Senante (2026) apply a latent-class stochastic cost frontier to English and Welsh utilities over 1991–2019. They identify technologically distinct groups of utilities, which challenges the use of a single undifferentiated benchmark. Molinos-Senante et al. (2025) find that treatment complexity, raw-water sources and population density are associated with energy efficiency in drinking-water services. Operating context, not only managerial choice, explains differences between utilities.

Neither contextual variable set is available for wastewater in this panel. The studies instead justify two design choices.

- **Expenditure is shown in two forms.** Absolute spending and spending per connected property are presented as complementary views, because neither fully adjusts for network age, geography or treatment requirements.
- **Two kinds of evidence are kept apart.** Differences between companies are distinguished from change within the same company. Accounting for persistent company differences reduces, but does not eliminate, confounding.

Within-company analysis carries its own cost: where expenditure or an outcome changes little over a short period, there is little variation from which to estimate an association.

## 2.5 Timing and reporting periods

Maziotis et al. (2024b) separate efficiency change from technological change in English and Welsh eco-productivity over 2011–2018. Their work shows the value of examining performance over time rather than ranking companies at a single point. Their drinking-water framework, however, does not identify when benefits from wastewater spending arrive.

Timing creates two distinct problems here. First, a repair that responds to a collapse produces spending and an adverse outcome in the same period, while a preventive programme produces spending before any improvement. Second, reporting labels can mislead. A pollution figure labelled 2024/25 represents calendar year 2024, which only partly overlaps the April 2024–March 2025 expenditure year. Shifting a column by one row does not resolve this mismatch. The dataset must therefore record the period each observation actually measures, and any lagged comparison must state exactly which periods it pairs.

## 2.6 Inference with few clusters

MacKinnon, Nielsen and Webb (2023) show that cluster-robust inference depends on the number of clusters and their characteristics. With few clusters, they recommend alternatives such as the cluster jackknife (CV3) and the wild-cluster bootstrap.

The 45 company-years in this study come from only nine companies, so they cannot be treated as 45 independent observations, and a conventional significance threshold alone would understate uncertainty. The analysis therefore reports four properties of each association separately: direction, magnitude, stability when individual companies are omitted, and uncertainty. A wide interval is information about precision, not a failure of the study.

The short panel also argues against complexity. Multiple lags, company-specific slopes and large sets of covariates would compete for very limited information.

## 2.7 Research gap and conceptual framework

The reviewed literature contains substantial quantitative work on water utilities. It would therefore be unjustified to claim that expenditure and performance have not been studied. That work, however, concentrates on frontier efficiency, on drinking-water services and on historical periods ending by 2019. Against this, three gaps define the contribution of this project. Each is traced to the artefact in Appendix B.

- **G1 Scope gap.** None of the reviewed studies examines, outcome by outcome, how wastewater network-plus expenditure, distinguishing base (maintenance) spending from total spending, relates to sewer flooding, collapses and pollution for England's water and sewerage companies over 2017/18–2024/25. *(RQ1, RQ2)*
- **G2 Robustness gap.** None of the reviewed sector studies reports few-cluster inference together with sensitivity to the spending measure, timing and influential companies, or states the smallest association its data could detect. *(RQ2, RQ3)*
- **G3 Communication gap.** The regulatory publications reviewed (Ofwat, 2025a; 2025b) present spending beside performance, but they do not estimate the association between them or show its uncertainty. *(RQ4)*

The conceptual framework treats expenditure as a financial input to wastewater service production and the four outcomes as recorded results. Company scale, persistent network characteristics and shared annual conditions can influence both. Poor performance can also prompt spending, which creates a possible reverse relationship.

The framework therefore allows for beneficial, adverse or weak associations. Separate outcomes, explicit period labels and alternative expenditure measures are built into the requirements (Chapter 4), because each of them changes what any resulting association means.
