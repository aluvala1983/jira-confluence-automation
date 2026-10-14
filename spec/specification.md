# Feature Specification: Weekly Jira Status Report Generator

**Status:** Draft
**Source:** `project_spec.md`
**Constitution:** `constitution.md`
**Version:** 1.0

## 1. Summary

Build a local web application for a Delivery Manager to retrieve data from one Jira Data Center/Server project and prepare two editable weekly status report drafts: a customer-facing report and an internal leadership report. The application validates Jira access and configuration, calculates report data deterministically from a complete Jira snapshot, applies audience-specific disclosure rules, and lets the Delivery Manager review and edit both drafts before saving them as Markdown.

The initial release is read-only with respect to Jira. It does not create or edit Jira issues, access Confluence, or distribute reports. The Delivery Manager shares saved reports manually.

## 2. Problem and Goals

Preparing weekly status updates currently requires manual collection and reconciliation of Jira information. The application should reduce that effort while preserving the Delivery Manager's control over delivery health, sensitive information, and final wording.

### Goals

- Retrieve complete, authorized data from one configured Jira Data Center/Server project.
- Calculate completed, remaining, planned, and blocked/risk issue counts using documented rules.
- Generate consistent customer and internal leadership drafts from the same validated data snapshot.
- Keep Jira credentials and project data local; require human review before a report is saved for sharing.
- Make failures, missing permissions, incomplete data, and unresolved review items visible and actionable.

### Non-goals

- Jira Cloud support, multiple projects, cross-project rollups, or team-wide accounts.
- Confluence access or automation in this feature.
- Creating, updating, transitioning, or commenting on Jira issues.
- Automatic health scoring or AI-generated/summarized content.
- Story-point or velocity reporting.
- Scheduled generation or automatic email, chat, or other external distribution.
- Multi-user/team-hosted operation.
- A sprint dashboard, burndown chart, or automatic blocker alerting.

## 3. Users and Permissions

### Primary user: Delivery Manager

The Delivery Manager runs the local application, configures the Jira project and reporting rules, supplies their own personal access token for a generation request, selects health, reviews and edits both report drafts, and saves the approved Markdown files.

### Stakeholders

Stakeholders receive reports outside the application. They do not need application accounts or access to the application.

### Permission model

- Jira reads use the authenticated user's own permissions. The application must not elevate access or use a shared service account.
- The first version has one local operator and must bind its user-facing service to loopback by default.
- Jira operations are read-only. Report saving writes only to the application's local `reports/` output directory.

## 4. User Scenarios and Testing

### User Story 1 - Configure and validate Jira access (Priority: P1)

As a Delivery Manager, I want to configure one Jira project and validate my access so that report generation uses the right project and rules.

**Why P1:** No report can be trustworthy without a validated project, permissions, and field/status mappings.

**Acceptance scenarios:**

1. **Given** a valid Jira base URL, project key, required rules, and a valid personal access token, **when** I validate the connection, **then** the application confirms the project and required read access without saving or logging the token.
2. **Given** an invalid token, inaccessible project, missing changelog permission, or required unsupported field, **when** validation runs, **then** the application identifies the actionable failure and does not claim the configuration is ready.
3. **Given** a missing or contradictory required setting, **when** I try to validate or generate, **then** the application identifies the setting and prevents generation until it is resolved.

### User Story 2 - Generate a weekly data snapshot (Priority: P1)

As a Delivery Manager, I want complete, period-specific issue data and counts so that both report drafts are grounded in the same Jira facts.

**Why P1:** A complete and reproducible snapshot is the basis of all report content.

**Acceptance scenarios:**

1. **Given** valid configuration and access, **when** I start generation, **then** the application selects the previous Monday-through-Sunday reporting period in the configured project timezone and shows its inclusive start and exclusive end.
2. **Given** issues and changelogs across multiple Jira pages, **when** generation runs, **then** the application fetches every required page and produces counts only after all required requests succeed.
3. **Given** a timeout, rate limit, API error, or incomplete page sequence, **when** generation runs, **then** the application reports the failure, offers a retry where appropriate, and does not present or save a partial snapshot as complete.
4. **Given** source issues include stories, bugs, tasks, subtasks, and unrelated types, **when** the snapshot is normalized, **then** it includes configured stories, bugs, and tasks and excludes subtasks and out-of-scope issue types.
5. **Given** a report period with multiple qualifying done transitions for one issue, **when** completed work is calculated, **then** the issue is counted no more than once and its treatment follows an explicitly configured reopened-issue rule.

### User Story 3 - Review and edit audience-specific drafts (Priority: P1)

As a Delivery Manager, I want customer and leadership drafts separated by audience so that I can review accurate, appropriately disclosed content before sharing.

**Why P1:** Audience-safe reports are the main user-visible outcome, and sensitive information must not leak into customer material.

**Acceptance scenarios:**

1. **Given** a complete validated snapshot, **when** drafts are rendered, **then** both drafts use that same snapshot and deterministic templates, and contain no AI-generated claims.
2. **Given** customer-facing draft content, **when** the customer draft is previewed, **then** internal commentary, staffing details, and designated sensitive risks are excluded before preview.
3. **Given** content whose customer suitability is unknown, **when** drafts are prepared, **then** that content is held out of the customer draft and clearly presented for Delivery Manager classification.
4. **Given** completed drafts, **when** I review them, **then** I can select Green, Amber, or Red health, add an optional rationale, and edit each audience's Markdown independently.
5. **Given** generation is in progress or has failed, **when** I view the page, **then** loading and error states are clear and no stale draft is represented as the current successful result.

### User Story 4 - Save reviewed Markdown safely (Priority: P1)

As a Delivery Manager, I want to save reviewed drafts without losing existing work so that I can share the final files manually.

**Why P1:** Saving is the only first-version distribution path and must preserve user edits.

**Acceptance scenarios:**

1. **Given** both drafts have been reviewed and edited, **when** I save them, **then** the application writes editable Markdown files under `reports/` with reporting-period and audience-identifying filenames.
2. **Given** a destination filename already exists, **when** I save, **then** the application never silently replaces it; it asks for explicit overwrite confirmation or writes a uniquely named copy.
3. **Given** a file write fails, **when** I save, **then** the application reports which output could not be saved and does not show that output as successfully written.
4. **Given** reports are saved, **when** I inspect the files, **then** they contain no personal access token and the customer file respects the customer disclosure rules.

## 5. Functional Requirements

### Configuration and connection

- **FR-001:** The application MUST allow configuration of Jira base URL, project key, project timezone, issue-type mappings, done statuses, blocker signals, and the authoritative next-sprint/release planning rule.
- **FR-002:** The application MUST connect only to Jira Data Center/Server using a supported REST API and the authenticated user's permissions. The supported Jira version range MUST be confirmed before production use.
- **FR-003:** The application MUST accept the user's personal access token only for an active generation request, hold it in memory for that request, and clear references when the request completes.
- **FR-004:** The token MUST NOT be written to the database, files, browser storage, URL, report output, logs, or error messages.
- **FR-005:** Before fetching report data, the application MUST validate required configuration, project access, authentication, and access to required fields and changelogs.
- **FR-006:** Configuration failures MUST identify the field or permission that needs attention without exposing secrets or unnecessary Jira content.

### Reporting period and issue scope

- **FR-007:** The default reporting period MUST be the previous Monday 00:00 through the following Monday 00:00, with the start inclusive and end exclusive, in the configured project timezone.
- **FR-008:** The application MUST show the selected reporting period and allow the Delivery Manager to review it before retrieving data. Custom period selection is not in first-release scope unless separately approved.
- **FR-009:** Issue types MUST be mapped through project configuration. The initial supported scope is stories, bugs, and tasks; subtasks and unrelated types MUST be excluded.
- **FR-010:** Report totals MUST use issue counts, not story points. Delivery summaries MUST be team-level; individual issue owners may appear only where useful for a specific action item.

### Data retrieval and calculations

- **FR-011:** The Jira client MUST paginate through all required issue and changelog results before declaring the snapshot complete.
- **FR-012:** Jira errors, rate limits, timeouts, and permission failures MUST be surfaced. The application MUST NOT present incomplete data as a successful report.
- **FR-013:** Completed work MUST be based on unique in-scope issues that transitioned into a configured done status during the reporting interval, using changelog history even when the resolution date is absent.
- **FR-014:** An issue MUST be counted at most once in completed work for a report period. Treatment of issues completed and reopened in the same period MUST follow an explicit project rule resolved before implementation; until then, the behavior is an open decision and MUST NOT be silently chosen.
- **FR-015:** Remaining open work MUST include in-scope project issues that are not in a configured done status at snapshot time.
- **FR-016:** Next week's plan MUST be derived from the configured authoritative upcoming sprint or release convention. If no upcoming planning window exists or the source is ambiguous, the application MUST report that fact rather than guess.
- **FR-017:** Blocker/risk candidates MUST be detected only through configured blocked-status and/or Jira-flag signals. Each displayed issue should include its key, summary, current status, and direct Jira link as permitted by audience.
- **FR-018:** The application MUST preserve the snapshot's project, reporting interval, generation time, and freshness context for preview and audit within the local workflow.

### Draft generation, classification, and review

- **FR-019:** The application MUST render separate customer and internal leadership drafts from one validated normalized snapshot.
- **FR-020:** Rendering MUST be deterministic and template-based. The application MUST NOT call AI, summarization, or analytics services or invent narrative facts.
- **FR-021:** Both drafts MUST provide consistent headings for report title/project/period/generation date, delivery health, executive summary, completed work, remaining work, next week's plan, blockers/risks, and required decisions/actions, with audience-specific content.
- **FR-022:** The Delivery Manager MUST select Green, Amber, or Red health during review. The application MUST NOT automatically score health. The user may provide a rationale.
- **FR-023:** The application MUST clearly distinguish Jira-derived facts from human-entered or user-confirmed content.
- **FR-024:** The customer draft MUST exclude internal commentary, individual staffing details, and risks designated sensitive before preview and save.
- **FR-025:** Content with unknown customer-suitability MUST be excluded from the customer draft until the Delivery Manager explicitly classifies or clears it for inclusion.
- **FR-026:** The Delivery Manager MUST be able to review and edit both drafts before saving. Customer and leadership edits MUST remain separate.
- **FR-027:** Before saving, the application MUST preview the configured project, reporting dates, relevant counts, audience identity, and any outstanding classification/review items.

### Output and deployment

- **FR-028:** The application MUST save editable Markdown drafts under the local `reports/` directory. Filenames MUST identify the report period and audience, for example `weekly-status-2026-10-05-customer.md` and `weekly-status-2026-10-05-leadership.md`.
- **FR-029:** Existing output MUST NOT be overwritten silently. The application MUST require explicit overwrite confirmation or select a unique filename.
- **FR-030:** File writes MUST be safe against partial output. If either write fails, the application MUST report the exact outcome and MUST NOT claim both files were saved.
- **FR-031:** The application MUST run locally and bind user-facing services to loopback by default. It MUST use HTTPS with certificate verification for Jira connections and MUST NOT disable TLS verification to work around connectivity failures.
- **FR-032:** The first version MUST NOT send reports, Jira data, or credentials to remote hosting, external analytics, third-party AI, or external distribution services.
- **FR-033:** The frontend MUST render Jira- and user-sourced content safely, escaping untrusted text to prevent script injection.

## 6. Key Entities

### Project Configuration

Non-secret settings for the single configured Jira project: base URL, project key, timezone, issue type mappings, done statuses, blocker signals, and planning-source rules. This configuration is local and editable by the Delivery Manager.

### Generation Credential

The user's personal access token supplied for one generation request. It exists only transiently in application memory for that request and is never persisted.

### Reporting Period

The selected period with a project-timezone identifier, inclusive start, exclusive end, and user-visible date range. The default is the previous Monday through Sunday.

### Jira Snapshot

A complete normalized, read-only set of in-scope issue facts and required status-change history retrieved for a generation. It includes source project, retrieval/generation time, and enough provenance to distinguish Jira facts from review content. It is transient and is not persisted as a database cache.

### Report Draft

An audience-specific, deterministic Markdown document derived from one snapshot, plus Delivery Manager-entered health/rationale and edits. Customer and leadership drafts are distinct disclosure artifacts.

### Risk Classification

A configured or Delivery Manager-confirmed indication of whether a blocker/risk is suitable for customer disclosure. Unknown or unclassified content is excluded from the customer draft until reviewed.

## 7. Data and Persistence

- **PostgreSQL 15 via Docker** MUST be used for local persistence of non-secret application configuration and preferences needed between runs.
- PostgreSQL MUST NOT store Jira personal access tokens or serve as a cache for Jira issue/changelog content in this first version.
- Saved report drafts MUST be Markdown files in `reports/`; database storage MUST NOT be treated as the canonical copy of report content.
- Database schema changes MUST use explicit, reviewable migrations. Database access MUST be parameterized and remain server-side.
- Local Docker/Compose networking MUST expose only required services. The database MUST NOT be published to external interfaces by default.
- Data retention, backup, and removal expectations for configuration and generated report files MUST be documented for local operators.

## 8. Technical Constraints and Architecture

- **Frontend:** React 18 with Vite.
- **Backend:** Node.js with Express.
- **Database:** PostgreSQL 15 running via Docker.
- The browser communicates with the Express API; only the backend accesses PostgreSQL and Jira.
- The API owns configuration validation, credential lifetime, Jira REST calls, pagination, normalization, reporting calculations, audience filtering, deterministic rendering, and safe report file writes.
- The frontend owns configuration and review flows, visible validation/error/loading states, report previews, edits, and explicit save confirmation.
- Keep report rules independent from HTTP and UI presentation so they can be tested as pure units.
- Keep Jira base URLs validated and use TLS verification; credentials must not appear in request URLs or client-side persistent storage.
- Preserve local-only behavior and loopback binding. Any deployment beyond one local operator requires a separate specification and security review.

## 9. Report Content

Both report drafts use a consistent structure:

1. Report title, project, reporting period, and generation date.
2. Overall delivery health selected by the Delivery Manager, with optional rationale.
3. Executive summary.
4. Completed this week: count and key outcomes.
5. Remaining open work: count and material work items.
6. Next week's plan: count and priorities/outcomes.
7. Blockers, risks, and required decisions/actions.

The customer draft is concise and customer-relevant. It excludes internal commentary, staffing detail, and explicitly sensitive risks. Unclassified items remain excluded until reviewed. The leadership draft may include internal commentary, staffing-related information when relevant, and sensitive risks, subject to user review.

The two drafts MUST be generated from the same snapshot. Narrative text MUST be deterministic or entered/edited by the Delivery Manager.

## 10. Error Handling and Edge Cases

- **Invalid authentication:** Identify that credentials were rejected; do not echo or log the token.
- **Insufficient project/changelog permissions:** Identify the required access and block generation of misleading counts.
- **Missing or unsupported Jira fields/statuses:** Identify the configuration or compatibility issue and require resolution.
- **Pagination/API interruption or rate limit:** Mark the retrieval incomplete, report whether retry is possible, and do not render a success-shaped complete report.
- **No upcoming sprint/release:** Show that no configured plan source was found and leave planned work empty/explicitly unavailable; do not substitute another source.
- **Ambiguous blocker or customer classification:** Show for human review; do not silently include in customer output.
- **Issue completed then reopened:** Apply only the explicitly selected policy. This must be resolved before implementation because it affects counts.
- **Report name collision:** Confirm overwrite or create a unique copy without losing the existing file.
- **One output write succeeds and another fails:** Report each file's outcome and provide a safe retry path without falsely claiming an atomic two-file save.
- **Unsafe or malformed source text:** Escape it in the UI; do not interpret it as executable markup or HTML.
- **Jira unavailable or stale data:** Show the failed retrieval/freshness information and prevent save as a current complete report.

## 11. Success Criteria

- **SC-001:** A Delivery Manager can configure one Jira Data Center/Server project and receive distinct, actionable feedback for invalid credentials, inaccessible project, missing changelog access, and unsupported required fields.
- **SC-002:** For any configured timezone, period calculations use the previous Monday 00:00 inclusive through the next Monday 00:00 exclusive, including week/year and daylight-saving boundaries.
- **SC-003:** Fixture-based tests confirm issue type inclusion/exclusion and verify that completed counts use changelogs when resolution dates are absent and never count one issue more than once.
- **SC-004:** A complete paginated fixture produces the same normalized snapshot and counts independent of page boundaries; an incomplete or failed fetch cannot produce a success result or saved report.
- **SC-005:** Next-week counts match the configured sprint/release source; when it is absent or ambiguous, the application reports unavailable rather than guessing.
- **SC-006:** Customer-output tests prove that internal commentary, staffing details, and sensitive or unclassified content are absent from customer preview and saved Markdown.
- **SC-007:** Customer and leadership drafts are deterministic for identical input, template version, and human review values, and both derive from the same snapshot.
- **SC-008:** The Delivery Manager can select health, edit both drafts independently, review dates/counts/classifications, and save Markdown files using audience-identifying filenames.
- **SC-009:** Collision and file-write tests prove existing files are not silently replaced and incomplete writes are reported accurately.
- **SC-010:** Tests and inspection confirm tokens are absent from persisted configuration, browser storage, URLs, reports, logs, and surfaced error messages.
- **SC-011:** The affected frontend build, backend checks, focused unit tests, and database migration tests pass before release.
- **SC-012:** The application runs locally with the specified React 18/Vite, Node.js/Express, and PostgreSQL 15/Docker stack, with user-facing access bound to loopback by default.

## 12. Assumptions and Dependencies

- A Jira Data Center/Server instance is reachable from the local machine over HTTPS and supports personal access token authentication and the required REST endpoints.
- The Delivery Manager can obtain read access to the configured project's issues, changelogs, and required fields.
- Jira field names, issue type names, done statuses, blocker signals, and planning conventions differ by project and therefore require configuration.
- A local `reports/` directory is writable by the application user and is treated as sensitive local output.
- The single-user local deployment remains in effect for the first version.
- No Jira write or report distribution capability is required.

## 13. Open Questions - Resolve Before Implementation

1. What Jira base URL, exact Jira Data Center/Server version, project key, and personal-token authentication behavior should be supported?
2. What is the project timezone?
3. Which exact Jira issue types map to stories, bugs, and tasks, and how should aliases be handled?
4. Which statuses count as done? If an issue enters a done status and is reopened in the same week, does it count as completed for that week, remaining open at snapshot time, or both?
5. What is the authoritative blocked status and/or Jira flag field/value?
6. Is next week's plan based on the next sprint, a release, or an explicitly chosen source? If both exist, which takes precedence and how are issues assigned to the window?
7. How are sensitive risks identified, and what review interaction is required before a risk is cleared for the customer draft?
8. What report filename collision behavior is preferred: explicit overwrite confirmation or always create a unique copy?
9. What local retention, backup, and removal policy applies to saved report files and PostgreSQL configuration?
10. What Jira pagination/rate-limit behavior and maximum request duration should the client support for the target instance?

## 14. Constitution Check

- The feature complies with the local-control, transient-credential, least-privilege, and no-third-party-AI principles in `constitution.md`.
- It preserves human ownership of health ratings, risk classification, and final report wording.
- It applies customer/internal disclosure filtering before preview and save.
- It avoids Jira/Confluence writes and external distribution in the initial release.
- It uses the constitution's required frontend, backend, and database stack; the earlier Python/Flask design in `project_spec.md` is superseded for implementation of this feature.
- Open business rules remain explicit and must be resolved before implementing affected calculations.
