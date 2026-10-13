# Instructions Catalog

Each entry below is an instruction file with a one-line description. Keywords help route matching requests to the right instruction.

---

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — Create and maintain portable project instructions and IDE integrations.
  + Keywords: create instructions, update instructions, instruction catalog, configure Copilot
- [`./instructions/calculate-compound-interest.agent.md`](./calculate-compound-interest.agent.md) — Calculate compound interest using the project command-line tool.
  + Keywords: compound interest, interest calculation, annual rate, compounding frequency, compound_interest.py
- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Generate concise weekly status reports from approved project updates.
  + Keywords: weekly status, status report, accomplishments, blockers, next week
- [`./instructions/run-unit-tests-and-coverage.agent.md`](./run-unit-tests-and-coverage.agent.md) — Run scoped unit tests and report measured coverage.
  + Keywords: run tests, unit tests, test coverage, pytest, coverage report
- [`./instructions/validate-safe-report-output.agent.md`](./validate-safe-report-output.agent.md) — Validate report content and destination before safe Markdown output.
  + Keywords: validate report, safe report output, report filename, customer report, prevent overwrite
- [`./instructions/use-format-report.agent.md`](./use-format-report.agent.md) — Format supplied Jira issues as a Markdown status report using the local CLI.
  + Keywords: format Jira issues, format_report.py, Markdown status report, Jira JSON report, upcoming plans
- [`./instructions/use-calculate-velocity.agent.md`](./use-calculate-velocity.agent.md) — Calculate sprint velocity from supplied completed story-point values.
  + Keywords: calculate sprint velocity, calculate_velocity.py, story points, velocity total, completed story points
- [`./instructions/use-normalize-issues.agent.md`](./use-normalize-issues.agent.md) — Filter and normalize supplied Jira issue data into metrics-ready JSON.
  + Keywords: normalize Jira issues, normalize_issues.py, filter subtasks, Jira issue metrics, normalized JSON
- [`./instructions/work-with-jira-reporting-data.agent.md`](./work-with-jira-reporting-data.agent.md) — Fetch and format Jira issues, draft common JQL queries, and summarize sprint data.
  + Keywords: Jira workflow, Jira issues, JQL query, sprint summary, issue data