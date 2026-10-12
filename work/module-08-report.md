# Module 08 Completion Report

## Tracked Files
.gitignore
JIRA-SPRINT-DASHBOARD-REQUIREMENTS.md
PROJECT_IDEAS.md
calculator/main.py
calculator/operations.py
project_spec.md
weekly-status-report-template.md
work/module-03-report.md
work/module03-task

## Spec Commit History
36ed01c Add weekly Jira report specification

## project_spec.md Contents
# Weekly Jira Status Report Generator

## 1. Purpose

Build a local web application that gathers Jira data for a development project
and generates two editable weekly status report drafts: one for customers and
one for internal senior leadership.

The primary user is a Delivery Manager responsible for a 10-person development
team. The generator should reduce manual status gathering while keeping the
Delivery Manager in control of health ratings, sensitive content, and final
wording.

## 2. Goals and non-goals

### Goals

- Generate consistent, fact-based reports from one Jira Data Center/Server
  project.
- Summarize work completed during the reporting week, open work, next week's
  plan, blockers/risks, and overall delivery health.
- Produce separate customer and leadership drafts with audience-appropriate
  detail.
- Let the Delivery Manager review and edit the drafts before sharing.
- Keep Jira credentials and project data local to the user's machine.

### Non-goals for the first version

- Jira Cloud support.
- Multiple projects or team roll-ups.
- Automatic report emailing, Slack/Teams posting, or other distribution.
- Scheduled generation; reports are generated on demand.
- Creating or editing Jira issues.
- AI-generated summaries or automatic Green/Amber/Red health scoring.
- Story-point or velocity reporting.

## 3. Users and permissions

- **Delivery Manager:** Connects to Jira with their own account, configures the
  project/report settings, generates and edits both report drafts, selects
  delivery health, and saves the final Markdown files.
- **Stakeholders:** Receive the saved reports outside the application; they do
  not need application accounts.

The initial application is for one local user. It must not expose a network
service for team-wide use.

## 4. Scope and reporting rules

### Project and issue scope

- One configured Jira Data Center/Server project.
- Include stories, bugs, and tasks; exclude subtasks.
- Use issue counts, not story points.
- Keep delivery summaries at team level. Include individual issue owners only
  where useful for an action item.

### Reporting period

- The reporting period is the previous Monday through Sunday in the configured
  project timezone.
- Treat the interval as Monday 00:00 inclusive through the following Monday
  00:00 exclusive, to avoid boundary ambiguity.
- The default week is calculated when generation begins. The user can review
  the selected week before generating.

### Measures and content

- **Completed:** Count unique in-scope issues that transitioned to a configured
  done status during the reporting period, using Jira status-change history
  (changelog), including cases where the resolution date is missing.
- **Remaining open:** Count in-scope project issues not in a configured done
  status when the report is generated.
- **Next week's plan:** Count and summarize issues assigned to the next
  upcoming sprint or release. The project configuration must identify which
  Jira sprint/release field or convention is authoritative.
- **Blockers and risks:** Identify candidate issues using the project's
  dedicated blocked status and/or Jira flag. Show the issue key, summary,
  current status, and Jira link as appropriate to the audience.
- **Health:** Require the Delivery Manager to select Green, Amber, or Red
  during review. Do not infer a health rating automatically.

The treatment of an issue completed and then reopened within the same reporting
period must be explicitly configured or settled during implementation; do not
silently double-count an issue.

## 5. Functional requirements

### Jira connection and configuration

1. Provide configuration for Jira base URL, project key, project timezone,
   issue-type mappings, done statuses, blocker signals, and next-sprint/release
   selection rules.
2. Use the Jira Data Center/Server REST API and the authenticated user's
   permissions. Verify compatibility with the Jira version available to the
   Delivery Manager.
3. Prompt for the user's personal access token when a report is generated.
   Keep it in memory only for the request; do not persist it in a file,
   database, browser storage, or logs.
4. Validate the connection and configuration before fetching report data.
   Show actionable errors for authentication failures, inaccessible projects,
   missing changelog access, and unsupported or missing fields.
5. Fetch complete result sets using pagination and respect Jira API errors and
   rate limits; do not present partial data as a successful full report.

### Report generation and review

1. Generate two drafts from the same validated Jira data snapshot:
   - **Customer report:** concise delivery progress and customer-relevant
     upcoming work/risks. Exclude internal commentary, staffing details, and
     sensitive risks.
   - **Internal leadership report:** full delivery detail, including
     internal commentary, staffing-related information when relevant, and
     sensitive risks.
2. Include completed work, remaining open work, next week's plan,
   blockers/risks, and a health field in each report as appropriate to its
   audience.
3. Use deterministic templates populated from Jira facts. Do not call an AI
   service or invent narrative facts.
4. Let the Delivery Manager review and edit each draft before saving.
5. Clearly distinguish Jira-derived facts from fields that require human input
   or confirmation.
6. Provide a preview of the reporting dates, configured project, and counts
   before save.

### Output and distribution

- Save editable Markdown drafts in a `reports/` directory.
- Use filenames that include the reporting period and audience, for example:
  `weekly-status-2026-10-05-customer.md` and
  `weekly-status-2026-10-05-leadership.md`.
- Do not overwrite an existing report silently. Ask for confirmation or save a
  uniquely named copy.
- Saving drafts is the only distribution behavior in the first version. The
  user shares the reviewed reports manually.

## 6. Draft report structure

Both audience drafts should use consistent headings, with audience-specific
content and redaction:

1. Report title, project, reporting period, and generation date.
2. Overall delivery health (Delivery Manager-selected Green/Amber/Red and
   optional rationale).
3. Executive summary.
4. Completed this week, including issue count and key outcomes.
5. Remaining open work, including issue count and material work items.
6. Next week's plan, including issue count and priorities/outcomes.
7. Blockers, risks, and required decisions/actions.

The customer version must not contain internal commentary, individual
staffing details, or risks designated sensitive. If content cannot be
classified safely, present it for Delivery Manager review rather than
automatically including it in the customer draft.

## 7. Proposed technical design

The repository currently has Python examples but no established application
framework or dependency manifest. For a simple local web application, the
proposed first implementation is:

- **Language/runtime:** Python 3.
- **Web layer:** Flask with server-rendered templates and minimal client-side
  JavaScript.
- **Jira client:** A maintained Python HTTP client or the standard HTTP
  library, selected after confirming Jira API/version compatibility.
- **Report rendering:** Deterministic Python report model plus Markdown
  templates.
- **Persistence:** No database required for the first version. Store
  non-secret project/report configuration locally; save report output as
  Markdown. Do not store the PAT.

Suggested component flow:

`Local browser -> localhost web app -> configuration validator -> Jira REST
client -> normalized report data -> customer/leadership renderers -> preview
and edits -> Markdown files`

Bind the web server to loopback (`127.0.0.1`) by default. Use HTTPS when
connecting to Jira, verify TLS certificates, and do not disable certificate
validation to work around a connection issue.

## 8. Security, privacy, and reliability

- Keep the app local-only; do not add remote hosting or external analytics.
- Accept a Jira personal access token only for a generation session. Keep it
  out of logs, error messages, URLs, report files, and persistent browser
  storage; clear in-memory references when the request completes.
- Do not send Jira content to third-party AI or summarization services.
- Escape user/Jira-sourced content in the web preview to prevent script
  injection.
- Treat customer and leadership report outputs as separate disclosure
  boundaries. Apply the customer exclusions before preview/save and make
  audience identity visible in the UI and filename.
- Avoid partial or stale-looking success: if Jira data cannot be fully fetched
  or required configuration is missing, explain the failure and do not save a
  report that appears complete.
- Report file writes should be safe and should not silently replace existing
  user-authored reports.

## 9. Acceptance criteria

1. The app can connect to the configured Jira Data Center/Server project using
   the user's PAT and reports invalid credentials or insufficient access
   clearly.
2. The selected reporting period is the previous Monday-Sunday in the
   configured timezone, with correct inclusive/exclusive boundaries.
3. Counts and summaries include stories, bugs, and tasks, and exclude
   subtasks.
4. Completed counts use status-change history in the reporting period even
   when the resolution date is absent; each issue is counted at most once.
5. Remaining-open counts reflect configured done statuses at generation time.
6. Next-week plan reflects the configured upcoming sprint/release source.
7. Blocker candidates are detected from configured blocked status/flag
   signals, and linked issues open in Jira.
8. The app generates separate deterministic customer and leadership drafts
   from the same data snapshot. Customer drafts exclude internal commentary,
   staffing details, and sensitive risks.
9. The Delivery Manager can select health, review/edit both drafts, and save
   them as Markdown under `reports/` without silent overwrite.
10. The PAT is not persisted or logged, and no Jira data is sent to an AI
    service.
11. Jira API, authentication, pagination, and file-write failures are
    surfaced; the application does not save incomplete output as a successful
    report.

## 10. Open decisions and setup inputs

Resolve these before or during implementation:

- Jira base URL and exact Jira Data Center/Server version.
- Jira project key and the user's permission to read issues and changelogs.
- Project timezone.
- Exact Jira issue type names corresponding to stories, bugs, and tasks.
- Exact done statuses, including handling of reopened work and repeated
  transitions within one week.
- How the blocked status and/or Jira flag is represented in this project.
- Whether the next-week planning source is the next sprint, a release, or a
  configured choice when both are used; confirm how the relevant issues are
  identified.
- Which risks are sensitive and must be excluded from the customer version,
  and how a Delivery Manager marks or reviews them.
- Whether the proposed Flask-based local application is acceptable for the
  workspace.

