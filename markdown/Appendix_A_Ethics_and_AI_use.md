# Appendix A Ethical review and use of generative AI

## A.1 Nature of the research

The analysis uses only public, company-level regulatory data published by Ofwat under the Open Government Licence. No personal data are processed in the analysis, and no human participants are involved in it. The supervisor's ethics declaration covers this use of public data [student to insert the declaration date and reference].

## A.2 Responsible analysis and presentation

The main ethical risk is misrepresenting what the data show. The design responds with five rules (Section 4.5), each checked in the evaluation (Chapter 7):

- associations are never described as causes;
- missing values are never shown as zero;
- no company ranking or forecast is produced (requirement R14);
- every estimate is shown with its uncertainty;
- the dashboard states what nine companies can and cannot detect.

## A.3 Evaluation involving people

A small usability study with 3–5 adult volunteers was designed to be low risk:
- no recording;
- anonymous notes only;
- no incentives;
- withdrawal allowed for 7 days.

It requires its own review under UWE's Student Ethical Review Record, because the existing declaration covers public data only. The study pack (protocol, information sheet, consent form, privacy notice, session script and recruitment message) is in the project documents.

[Student to complete after the supervisor's decision, due 4 December 2026, choosing one:
- **Approved:** the approval date and outcome, with a reference to Section 7.3.
- **Not approved in time:** "The study was not conducted; no participant was contacted."]

## A.4 Use of generative AI

**Declaration.** Generative AI was used in this project, and its use is acknowledged here in line with UWE Bristol guidance on using generative AI in assessments (UWE Bristol, n.d.b). [Student to confirm with the module leader that the use described below is permitted, and record the date of that confirmation.]

**Tools.**
- **Claude (Anthropic), model Claude Opus 5.5,** used through the Claude Code desktop application in November 2026 (Anthropic, 2026).
- [Student to list any other AI tools used earlier in the project, with dates and purposes.]

**What the AI was used for.**

| Area | Use |
|---|---|
| Code | Writing and debugging the Python analysis, the statistical-methods module, the scripts that generate the notebook, UML figures, Power BI dashboard and Word documents, and the reproducibility and contrast checks |
| Data | Locating and checking Ofwat data sources, and comparing releases (for example, confirming that the October 2025 base-cost file matches the December 2024 file) |
| Testing | Operating Power BI Desktop, with the student's permission, to run the dashboard acceptance checks, the heuristic review and the contrast check |
| Writing | Drafting text for Chapters 1–7, the ethics pack and project documents. [Student to confirm: the submitted text was rewritten by the student in their own words.] |

**What the student did.**
- **Set the research questions, scope and priorities.**
- **Made the key decisions,** recorded in the decision log (Appendix G):
  - restricting the study to England's water and sewerage companies;
  - rejecting the joined total-spending series;
  - adopting base spending over 2017-18 to 2024-25;
  - the balanced panel;
  - the requirements changes;
  - the handling of the user study.
- **Approved each data download,** and reviewed the code, outputs and drafts.

**How outputs were verified.**
- **Data:** every number reported is produced by code from the original Ofwat files and protected by 15 automatic checks.
- **Reproducibility:** repeat runs are byte-identical, and the earlier verified results are reproduced exactly.
- **Dashboard:** checked live in Power BI Desktop.
- **References:** each one was checked against its source by the student. [Student to confirm once the reference check is complete.]
- **Errors caught:** AI-drafted statements that could not be supported were removed or corrected. For example, a value misread from a chart was replaced by the value in the data.

**Data protection.** No personal or sensitive data, beyond the student's own name, were entered into the AI tool. No participant data exist.
