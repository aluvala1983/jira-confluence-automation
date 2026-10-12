# Jira Sprint Progress Dashboard Requirements

## Purpose

Build a standalone dashboard that helps sprint team members quickly understand
their team's progress in the active sprint and spot work that may need
attention.

## Audience and primary use

- **Primary audience:** Sprint team members tracking daily progress.
- **Primary use:** See how much sprint work is complete versus remaining and
  identify blockers or other risks.

## Product scope

- Build a separate, standalone web app.
- Show one Jira project, configured for the team.
- Show that project's active sprint only. Sprint selection, including viewing
  past sprints, is out of scope for the initial version.
- Use a clean, high-contrast operational dashboard visual style.

## Functional requirements

### Sprint progress

- Show completed and remaining work for the active sprint.
- Represent work using **issue counts**, not story points.
- Include stories, bugs, and tasks in progress totals.
- Exclude subtasks from progress totals.
- Show a sprint burndown chart.

### Risks and issue navigation

- Prominently surface blockers and at-risk issues.
- Let users open a flagged issue directly in Jira.
- The specific rules for identifying "at risk" work have not yet been defined.

### Data refresh

- Refresh dashboard data automatically every few minutes.
- Provide a manual refresh control.
- The exact automatic refresh interval has not yet been specified.

## Jira integration and access

- Integrate with the team's organization-hosted Jira Data Center/Server
  instance (not Jira Cloud).
- Configure one Jira project for the team.
- Have each viewer connect using their own Jira account and personal access
  token; do not use a shared team account.
- Token handling must be appropriate for a user-specific credential. The
  storage and session approach remains to be designed.

## Initial-version boundaries

- One configured project.
- Active sprint only.
- Issue-count progress.
- Stories, bugs, and tasks included; subtasks excluded.
- No requirement yet for editing Jira issues from the dashboard.

## Open questions for implementation

1. What Jira base URL, project key, and Jira Data Center/Server version should
   be used?
2. What issue statuses count as complete, and how should reopened issues be
   counted?
3. Which conditions define a blocker and an at-risk issue?
4. What exact refresh interval should be used?
5. What burndown history should be displayed, and is the required historical
   sprint data available from the Jira instance?
6. How should each viewer's personal access token be entered, stored, and
   cleared? This should be decided before implementing the connection.
