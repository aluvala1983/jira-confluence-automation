# How to Fill Out the Weekly Status Report

Use [template.md](./template.md) to prepare a weekly project update. Produce a
separate version for each audience that needs a report:

- **Customer:** Focus on delivery, customer impact, upcoming outcomes, and
  customer-relevant risks. Do not include internal commentary, individual
  staffing details, or sensitive risks.
- **Internal leadership:** Include the delivery context, internal risks,
  decisions, and staffing information needed by leaders. Share only with the
  intended internal audience.

## Before You Start

1. Duplicate the template for the reporting week and audience. Keep a working
   copy so the blank template remains unchanged.
2. Set the reporting period to the previous Monday through Sunday in the
   project's timezone. Write both dates explicitly.
3. Confirm the project name/key, report audience, and preparer's role.
4. Gather Jira data for the configured project. For the weekly report, include
   stories, bugs, and tasks and exclude subtasks.
5. Verify the data is complete and current before writing. If Jira data or
   status history is unavailable, resolve that gap before publishing counts;
   never present partial results as complete.

## Complete Each Section

### Report details

- Replace every bracketed placeholder with a real value, or remove the line
  when it does not apply.
- Use the same reporting period and Jira data snapshot across the two audience
  versions.
- Use a clear date format such as `2026-10-05`.

### Overall Delivery Health

Choose **Green**, **Amber**, or **Red** yourself; do not infer it from issue
counts alone.

- **Green:** Delivery is on track, with no material unresolved threat to
  commitments.
- **Amber:** A meaningful risk or dependency could affect a commitment unless
  mitigated.
- **Red:** A commitment is currently missed or is likely to be missed without
  a material change, escalation, or decision.

Write a short, evidence-based rationale and describe any change since the
previous report. Keep customer rationale free of internal or sensitive detail.

### Executive Summary

In 2-4 sentences, state the week's most important outcome, the overall outlook,
and the most consequential next step, risk, or decision. Lead with impact, not
a list of tickets. Avoid unsupported claims or unexplained jargon.

### Completed This Week

- Count each in-scope issue once if it transitioned into a configured done
  status during the reporting period. Use Jira status-change history; do not
  rely only on resolution dates.
- Summarize outcomes and their impact. Include Jira keys or links only when
  they help the reader follow up.
- If an issue was completed and then reopened in the same week, follow the
  project's agreed counting rule and explain any material effect.

### Remaining Open Work

- Count in-scope issues that are not in a configured done status at the time
  the report data is captured.
- Describe only material work in the summary; the total is not a substitute
  for explaining delivery outlook.
- Do not imply that all open work is scheduled for next week.

### Next Week's Plan

- Count issues assigned to the next upcoming sprint or release, using the
  project's agreed planning source.
- State expected outcomes or priorities. Name an owner only when it clarifies
  responsibility or an action.
- If no upcoming sprint/release is configured, confirm the plan with the
  Delivery Manager rather than guessing.

### Blockers and Risks

- Use the project's configured blocked status and/or Jira flag to identify
  candidates, then confirm each item is still relevant.
- Explain the delivery or customer impact, mitigation/next action, accountable
  owner or role, and target date where known.
- Separate a current blocker from a potential risk. Do not label routine work
  as a blocker.
- For the customer version, include only approved customer-relevant items.
  Remove internal commentary, staffing detail, and anything marked sensitive.
  When classification is uncertain, omit the detail from the customer draft
  and ask the Delivery Manager to review it.
- If there are no material items, state that plainly instead of leaving the
  section blank.

### Decisions or Support Needed

State the decision/action, who needs to provide it, and the date by which it is
needed. Describe the consequence of delay when useful. If none is needed, write
“None this week.”

## Review and Finalize

1. Check that every number and Jira reference matches the same reporting
   snapshot and reporting period.
2. Confirm completed and remaining counts follow the configured status rules
   and do not double-count issues.
3. Confirm the status rating is a human judgment with an appropriate rationale.
4. Read the customer draft separately and remove internal-only or sensitive
   information; do not assume that editing the leadership version also
   produces a safe customer version.
5. Replace or remove all placeholders, resolve notes for confirmation, and
   check spelling, dates, links, and audience label.
6. Save a distinct file for each audience and reporting week. Have the
   Delivery Manager approve the drafts before sharing them; this report is a
   draft, not an automatic distribution.
