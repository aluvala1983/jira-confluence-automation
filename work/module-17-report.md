# Module 17 Completion Report

## Specification Contents
# Feature Specification: Weekly Jira Status Report Generator

**Status:** Review gaps resolved for prototype; production Jira verification remains required
**Source:** `project_spec.md`
**Constitution:** `constitution.md`
**Version:** 1.1

## 1. Summary

Build a local web application for a Delivery Manager to retrieve data from one Jira Data Center/Server project and prepare two editable weekly status report drafts: a customer-facing report and an internal leadership report. The application validates Jira access and configuration, calculates report data deterministically from a complete Jira snapshot, applies audience-specific disclosure rules, and lets the Delivery Manager review and edit both drafts before saving them as Markdown.

The initial release is read-only with respect to Jira. It does not create or edit Jira issues, access Confluence, or distribute reports. The Delivery Manager shares saved reports manually after reviewing and approving each audience-specific draft.

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

1. **Given** a valid Jira base URL, project key, required rules, and a valid personal access token, **when** I choose Validate Connection and submit the token, **then** the backend uses the token only for that validation request, confirms the project and required read access, and discards the token when the request completes; the frontend clears the token field on response.
2. **Given** an invalid token, inaccessible project, missing changelog permission, or required unsupported field, **when** validation runs, **then** the application identifies the actionable failure and does not claim the configuration is ready.
3. **Given** a missing or contradictory required setting, **when** I try to validate or generate, **then** the application identifies the setting and prevents generation until it is resolved.

### User Story 2 - Generate a weekly data snapshot (Priority: P1)

As a Delivery Manager, I want complete, period-specific issue data and counts so that both report drafts are grounded in the same Jira facts.

**Why P1:** A complete and reproducible snapshot is the basis of all report content.

**Acceptance scenarios:**

1. **Given** valid configuration and access, **when** I start generation, **then** the application selects the last fully completed Monday-through-Sunday reporting period in the configured project timezone and shows its inclusive start and exclusive end before retrieval.
2. **Given** issues and changelogs across multiple Jira pages, **when** generation runs, **then** the application fetches every required page and produces counts only after all required requests succeed.
3. **Given** a timeout, rate limit, API error, or incomplete page sequence, **when** generation runs, **then** the application reports the failure, offers a retry where appropriate, and does not present or save a partial snapshot as complete.
4. **Given** source issues include stories, bugs, tasks, subtasks, and unrelated types, **when** the snapshot is normalized, **then** it includes configured stories, bugs, and tasks and excludes subtasks and out-of-scope issue types.
5. **Given** a report period with multiple qualifying done transitions for one issue, **when** completed work is calculated, **then** the issue is counted once under the reopened-issue rule defined in §13.2.
6. **Given** a qualifying issue that is moved out of the project or no longer visible before the current project query, **when** metrics are calculated, **then** it is excluded from both completed and remaining counts because current project/type membership is authoritative.
7. **Given** a configured timezone with a daylight-saving transition in or near the reporting period, **when** the period boundaries are calculated, **then** each local Monday boundary is independently converted to its correct UTC instant and the interval remains start-inclusive/end-exclusive.

### User Story 3 - Review and edit audience-specific drafts (Priority: P1)

As a Delivery Manager, I want customer and leadership drafts separated by audience so that I can review accurate, appropriately disclosed content before sharing.

**Why P1:** Audience-safe reports are the main user-visible outcome, and sensitive information must not leak into customer material.

**Acceptance scenarios:**

1. **Given** a complete validated snapshot, **when** drafts are rendered, **then** both drafts use that same snapshot and deterministic templates, and contain no AI-generated claims.
2. **Given** customer-facing draft content, **when** the customer draft is previewed, **then** internal commentary, staffing details, and designated sensitive risks are excluded before preview.
3. **Given** content whose customer suitability is unknown, **when** drafts are prepared, **then** that content is held out of the customer draft and clearly presented for Delivery Manager classification.
4. **Given** completed drafts, **when** I review them, **then** I select one Green, Amber, or Red health value shared by both drafts, may add an internal-only rationale, and edit each audience's Markdown independently.
5. **Given** edited drafts, **when** I approve them for saving, **then** I approve each audience separately; customer approval includes an explicit confirmation that the final edited content contains no confidential or internal-only material.
6. **Given** generation is in progress or has failed, **when** I view the page, **then** loading and error states are clear and no stale draft is represented as the current successful result.
7. **Given** a Markdown preview includes raw HTML or a link with an executable URL scheme, **when** it is rendered, **then** raw HTML is disabled and the unsafe link is rejected without executing or loading remote content.

### User Story 4 - Save reviewed Markdown safely (Priority: P1)

As a Delivery Manager, I want to save reviewed drafts without losing existing work so that I can share the final files manually.

**Why P1:** Saving is the only first-version distribution path and must preserve user edits.

**Acceptance scenarios:**

1. **Given** both drafts have been reviewed, edited, health-rated, and approved separately, **when** I save them, **then** the application writes editable Markdown files under `reports/` with reporting-period and audience-identifying filenames.
2. **Given** a destination filename already exists, **when** I save, **then** the application writes a uniquely named copy and never offers overwrite in the prototype.
3. **Given** a file write fails, **when** I save, **then** the application reports which output could not be saved and does not show that output as successfully written.
4. **Given** customer content has been edited, **when** I approve its save, **then** I explicitly confirm that the final text contains no confidential or internal-only material; the application excludes source items that are sensitive or unclassified before preview.
5. **Given** one report saves and the other fails, **when** I retry, **then** the successful file remains unchanged and only the failed file is retried.

## 5. Functional Requirements

### Configuration and connection

- **FR-001:** The application MUST allow configuration of Jira base URL, project key, project timezone, issue-type mappings, done statuses, blocker signals, and the authoritative next-sprint/release planning rule.
- **FR-002:** The application MUST connect only to Jira Data Center/Server using a supported REST API and the authenticated user's permissions. The supported Jira version range MUST be confirmed before production use.
- **FR-003:** The application MUST accept the user's personal access token only in the body of an explicit connection-validation or report-generation request. Validation and generation are separate requests; the user re-enters the token for generation. The backend MUST use it only for that request and clear references when the request completes.
- **FR-004:** The token MUST NOT be written to the database, files, browser storage, URL, report output, logs, or error messages.
- **FR-005:** Before fetching report data, the application MUST validate required configuration, project access, authentication, and access to required fields and changelogs.
- **FR-006:** Configuration failures MUST identify the field or permission that needs attention without exposing secrets or unnecessary Jira content.

### Reporting period and issue scope

- **FR-007:** The default reporting period MUST be the last fully completed Monday 00:00 through the following Monday 00:00, with the start inclusive and end exclusive, in the configured project timezone. Calculate the Monday of the current local week and subtract seven calendar days for the start; the end is the Monday of the current local week.
- **FR-008:** The application MUST calculate and show the selected reporting period before retrieving data and require the Delivery Manager to confirm it. Custom period selection is out of scope.
- **FR-009:** Issue types MUST be mapped through project configuration. The initial supported scope is stories, bugs, and tasks; subtasks and unrelated types MUST be excluded.
- **FR-010:** Report totals MUST use issue counts, not story points. Delivery summaries MUST be team-level; individual issue owners may appear only where useful for a specific action item.

### Data retrieval and calculations

- **FR-011:** The Jira client MUST paginate through all required issue and changelog results before declaring the snapshot complete.
- **FR-012:** Jira errors, rate limits, timeouts, and permission failures MUST be surfaced. The application MUST NOT present incomplete data as a successful report.
- **FR-013:** Completed work MUST be based on unique in-scope issues that transitioned into a configured done status during the reporting interval, using changelog history even when the resolution date is absent.
- **FR-014:** An issue MUST be counted at most once in completed work for a report period if it has at least one transition into a configured done status during the interval. Repeated done transitions do not increase the completed count. If the issue is not in a done status at snapshot time, it is also counted in remaining open work; the report labels these as separate period-completed and current-open measures, so overlap is intentional and must not be represented as a partition.
- **FR-015:** Remaining open work MUST include in-scope project issues that are not in a configured done status at snapshot time.
- **FR-016:** Next week's plan MUST be derived from the configured authoritative upcoming sprint or release convention. If no upcoming planning window exists or the source is ambiguous, the application MUST report that fact rather than guess.
- **FR-017:** Blocker/risk candidates MUST be detected only through configured blocked-status and/or Jira-flag signals. Each displayed issue should include its key, summary, current status, and direct Jira link as permitted by audience.
- **FR-018:** The application MUST preserve the snapshot's project, reporting interval, retrieval start/end timestamps, and generation time for preview and audit within the active local workflow. A snapshot may be saved only within 30 minutes of successful retrieval; after that it is stale and a new complete retrieval is required.

### Draft generation, classification, and review

- **FR-019:** The application MUST render separate customer and internal leadership drafts from one validated normalized snapshot.
- **FR-020:** Rendering MUST be deterministic and template-based. The application MUST NOT call AI, summarization, or analytics services or invent narrative facts.
- **FR-021:** Both drafts MUST provide consistent headings for report title/project/period/generation date, delivery health, executive summary, completed work, remaining work, next week's plan, blockers/risks, and required decisions/actions, with audience-specific content.
- **FR-022:** The Delivery Manager MUST select Green, Amber, or Red health during review. The application MUST NOT automatically score health. The user may provide a rationale.
- **FR-023:** The application MUST clearly distinguish Jira-derived facts from human-entered or user-confirmed content.
- **FR-024:** The customer draft MUST exclude internal commentary, individual staffing details, and risks designated sensitive before preview and save. Source-derived entries MUST be classified before they are included in the customer preview.
- **FR-025:** Each blocker/risk candidate MUST have a per-generation classification of `customer-safe`, `internal-only`, or `unreviewed`. Only `customer-safe` candidates may appear in the customer draft. `internal-only` and `unreviewed` candidates MUST be excluded until the next generation/review cycle.
- **FR-026:** The Delivery Manager MUST be able to review and edit both drafts independently. Before saving, each draft requires its own explicit approval. Customer approval MUST include a final human confirmation that the edited customer Markdown contains no confidential or internal-only content. Automated semantic detection of sensitive material newly typed into free-form Markdown is out of scope for this prototype.
- **FR-027:** Before saving, the application MUST preview the configured project, reporting dates, relevant counts, audience identity, and any outstanding classification/review items.

### Output and deployment

- **FR-028:** The application MUST save editable Markdown drafts under the fixed local `reports/` directory; the user cannot supply an arbitrary output path or directory. Filenames MUST identify the report period start date and audience, for example `weekly-status-2026-10-05-customer.md` and `weekly-status-2026-10-05-leadership.md`.
- **FR-029:** Existing output MUST NOT be overwritten silently. The prototype MUST create a unique filename rather than overwrite an existing report.
- **FR-030:** The two reports are saved as independent files, not as an atomic pair. Each individual file MUST first be written to a temporary file in the same directory and then renamed to its unique destination so a failed write does not leave a truncated destination. If one write succeeds and the other fails, the successful file is retained, the failed file is reported, and retry MUST target only the failed file. A retry MUST NOT silently overwrite either file.
- **FR-031:** The application MUST run locally and bind user-facing services to loopback by default. It MUST use HTTPS with certificate verification for Jira connections and MUST NOT disable TLS verification to work around connectivity failures.
- **FR-032:** The first version MUST NOT send reports, Jira data, or credentials to remote hosting, external analytics, third-party AI, or external distribution services.
- **FR-033:** Markdown preview MUST disable raw HTML and sanitize generated HTML. Links MUST use HTTPS, except explicitly permitted `mailto:` links in human-authored text; `javascript:`, `data:`, and other executable or embedded-content schemes MUST be rejected. Images and remote embeds are disabled in preview. Saved Markdown is preserved as text after customer approval.

## 6. Key Entities

### Project Configuration

Non-secret settings for the single configured Jira project: base URL, project key, timezone, issue type mappings, done statuses, blocker signals, and planning-source rules. This configuration is local and editable by the Delivery Manager.

### Generation Credential

The user's personal access token supplied for one generation request. It exists only transiently in application memory for that request and is never persisted.

### Reporting Period

The selected period with a project-timezone identifier, inclusive start, exclusive end, and user-visible date range. The default is the last fully completed Monday-through-Sunday week.

### Jira Snapshot

A complete normalized, read-only set of in-scope issue facts and required status-change history retrieved for a generation. It includes source project, retrieval/generation time, and enough provenance to distinguish Jira facts from review content. It is transient and is not persisted as a database cache.

### Report Draft

An audience-specific, deterministic Markdown document derived from one snapshot, plus Delivery Manager-entered health/rationale and edits. Customer and leadership drafts are distinct disclosure artifacts.

### Risk Classification

A per-generation, Delivery Manager-confirmed indication of whether a blocker/risk is suitable for customer disclosure. The decision is transient and is not stored in PostgreSQL. Unknown or unclassified content is excluded from the customer draft until reviewed.

## 7. Data and Persistence

- **PostgreSQL 15 via Docker** MUST be used for local persistence of exactly one project's non-secret configuration: Jira base URL, project key, timezone, issue type mappings, done statuses, blocked status/flag rules, selected planning source, and filename preferences. No Jira issue content, changelogs, report draft contents, credentials, per-issue disclosure decisions, or user identity are persisted there.
- PostgreSQL MUST NOT store Jira personal access tokens or serve as a cache for Jira issue/changelog content in this first version.
- Saved report drafts MUST be Markdown files in `reports/`; database storage MUST NOT be treated as the canonical copy of report content.
- Database schema changes MUST use explicit, reviewable migrations. Database access MUST be parameterized and remain server-side.
- Local Docker/Compose networking MUST expose only required services. The database MUST NOT be published to external interfaces by default.
- There is no automatic retention or cleanup. The operator removes report files manually. PostgreSQL stores only the current configuration; updating it replaces the prior values without history. Configuration export, automated backup, and recovery are out of scope for the prototype; local database backup is the operator's responsibility. A reset operation MUST delete the stored configuration without deleting report files.

## 8. Technical Constraints and Architecture

- **Frontend:** React 18 with Vite.
- **Backend:** Node.js with Express.
- **Database:** PostgreSQL 15 running via Docker.
- The browser communicates with the Express API; only the backend accesses PostgreSQL and Jira.
- The API owns configuration validation, credential lifetime, Jira REST calls, pagination, normalization, reporting calculations, audience filtering, deterministic rendering, and safe report file writes.
- The frontend owns configuration and review flows, visible validation/error/loading states, report previews, edits, and explicit save confirmation.
- Keep report rules independent from HTTP and UI presentation so they can be tested as pure units.
- Keep Jira base URLs validated and use TLS verification; credentials must not appear in request URLs or client-side persistent storage.
- In development, browser API calls MUST use the same-origin `/api` proxy. If a separate origin is used, the API MUST allow only the explicitly configured loopback frontend origin and MUST reject mismatched `Origin`/`Host` values for state-changing requests.
- Jira URLs MUST use HTTPS, contain no embedded credentials, and be restricted to the configured origin for redirects. The configured organization-hosted Jira may resolve to private network addresses. Loopback and link-local Jira destinations are rejected. Protecting against a malicious administrator-controlled DNS environment is outside the single-user prototype threat model.
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

The customer draft contains the selected health value but not its rationale. The optional rationale is internal-only and appears only in the leadership draft. The customer draft excludes internal commentary, staffing detail, and explicitly sensitive risks. Unclassified source-derived items remain excluded until reviewed. The leadership draft may include internal commentary, staffing-related information when relevant, and sensitive risks, subject to user review.

The two drafts MUST be generated from the same snapshot. For generated issue rows, use Jira issue key, summary, issue type, and current status; include due date only when present and relevant. Do not fetch or reproduce Jira descriptions, comments, or worklogs. Sort issue rows lexicographically by issue key. Include every in-scope issue; do not silently truncate lists. Keep headings even when sections are empty, using “No in-scope issues” for zero items and “Unavailable: [reason]” when a source is unavailable. The executive summary, rationale, and required decisions/actions are optional human-entered text; no narrative is inferred. Narrative text MUST otherwise be deterministic or entered/edited by the Delivery Manager.

## 10. Error Handling and Edge Cases

- **Invalid authentication:** Identify that credentials were rejected; do not echo or log the token.
- **Insufficient project/changelog permissions:** Identify the required access and block generation of misleading counts.
- **Missing or unsupported Jira fields/statuses:** Identify the configuration or compatibility issue and require resolution.
- **Pagination/API interruption or rate limit:** Mark the retrieval incomplete, report whether retry is possible, and do not render a success-shaped complete report.
- **No upcoming sprint/release:** Show that no configured plan source was found and leave planned work empty/explicitly unavailable; do not substitute another source.
- **Ambiguous blocker or customer classification:** Show for human review; do not silently include in customer output.
- **Issue completed then reopened:** Count once in completed work if any qualifying done transition occurred in the period, and count as remaining open if current status is not done; label the measures separately.
- **Report name collision:** Create a unique copy using the suffix rule in §13.6; never overwrite.
- **One output write succeeds and another fails:** Report each file's outcome and provide a safe retry path without falsely claiming an atomic two-file save.
- **Unsafe or malformed source text:** Escape it in the UI; do not interpret it as executable markup or HTML.
- **Jira unavailable or stale data:** Show the failed retrieval/freshness information and prevent save as a current complete report. A previously retrieved snapshot remains editable but cannot be saved after 30 minutes or after a failed refresh marks it stale.

## 11. Success Criteria

- **SC-001:** A Delivery Manager can configure one Jira Data Center/Server project and receive distinct, actionable feedback for invalid credentials, inaccessible project, missing changelog access, and unsupported required fields.
- **SC-002:** For any configured timezone, period calculations use the last fully completed Monday 00:00 through the following Monday 00:00, both interpreted in that timezone and represented to Jira as UTC instants, with the start inclusive and end exclusive. Tests cover Monday generation, year boundaries, and daylight-saving transitions.
- **SC-003:** Fixture-based tests confirm issue type inclusion/exclusion and verify that completed counts use changelogs when resolution dates are absent and never count one issue more than once.
- **SC-004:** A complete paginated fixture produces the same normalized snapshot and counts independent of page boundaries; an incomplete or failed fetch cannot produce a success result or saved report.
- **SC-005:** Next-week counts match the configured sprint/release source; when it is absent or ambiguous, the application reports unavailable rather than guessing.
- **SC-006:** Customer-output tests prove that internal commentary, staffing details, and sensitive or unclassified content are absent from customer preview and saved Markdown.
- **SC-007:** Customer and leadership drafts are deterministic for identical input, template version, and human review values, and both derive from the same snapshot.
- **SC-008:** The Delivery Manager can select shared health, enter an internal-only rationale, edit both drafts independently, review dates/counts/classifications, and approve each audience separately. Customer approval requires an explicit final disclosure confirmation.
- **SC-009:** Collision and file-write tests prove existing files are not replaced, each file's save state is accurate, and retrying a failed file leaves a previously successful file unchanged.
- **SC-010:** Tests and inspection confirm tokens are absent from persisted configuration, browser storage, URLs, reports, logs, and surfaced error messages.
- **SC-011:** The affected frontend build, backend checks, focused unit tests, and database migration tests pass before release. Tests cover credential non-persistence, origin/host validation, markdown sanitization, report-period boundaries, final customer approval, configuration reset, and partial-save retry behavior.
- **SC-012:** The application runs locally with the specified React 18/Vite, Node.js/Express, and PostgreSQL 15/Docker stack, with user-facing access bound to loopback by default.

## 12. Assumptions and Dependencies

- A Jira Data Center/Server instance is reachable from the local machine over HTTPS and supports personal access token authentication and the required REST endpoints.
- The Delivery Manager can obtain read access to the configured project's issues, changelogs, and required fields.
- Jira field names, issue type names, done statuses, blocker signals, and planning conventions differ by project and therefore require configuration.
- A local `reports/` directory is writable by the application user and is treated as sensitive local output.
- The single-user local deployment remains in effect for the first version.
- No Jira write or report distribution capability is required.

## 13. Resolved Decisions and Prototype Boundaries

The following decisions close the review gaps recorded in `clarify.md`. They are binding for the prototype.

1. **Credential flow:** Connection validation and generation are separate user actions and separate requests to the local loopback API. The token is submitted in the request body, held in frontend memory only while the request is in flight, and cleared from the input on response. It is re-entered for generation. Each backend request discards the credential after its operation, including failure. The backend uses HTTPS with certificate verification to connect to Jira. Automatic credential-retaining retries are not supported.
2. **Completed/reopened issues:** Count a unique issue once as completed if any transition into a configured done status occurred during the reporting period. Count its current open state independently if it is not done at snapshot time. Repeated transitions do not multiply completed count. The report labels counts as period-completed and currently-open, and does not imply the two are mutually exclusive.
3. **Customer edits and disclosure:** Source-derived content is filtered/classified before customer preview. At save, customer Markdown requires explicit human confirmation after editing. Automated semantic detection of new sensitive wording manually typed into Markdown is out of scope; the final disclosure decision is the Delivery Manager's responsibility.
4. **Review and approval:** Saving requires explicit approval for each audience-specific draft. Health is mandatory before approval. Customer approval is a distinct action with a final disclosure confirmation. A saved file remains a manually distributed report; the application does not send it.
5. **Report content sources:** Issue rows use key, summary, issue type, current status, and optional due date; descriptions, comments, and worklogs are not read. Executive summary, rationale, and required decisions/actions are optional human-entered content. The rationale is shared as input but rendered only in the leadership draft.
6. **Pair-save behavior:** The files are written independently. A successful file remains saved if its partner fails. The UI reports each status and allows retry of only the failed file. Filename collisions always produce a unique filename by appending `-2`, then the next available positive integer before the `.md` extension; overwrite is not supported in the prototype.
7. **Reporting period:** Use the last fully completed local Monday-Sunday week. Compute the Monday of the current week in the configured project timezone and subtract seven calendar days; the exclusive end is the next Monday. This also applies when generation begins on Monday. Show the dates first and require confirmation before retrieval. Convert zoned boundaries to UTC instants for Jira; handle daylight-saving transitions using the timezone database, not fixed offsets.
8. **Issue population:** Determine project and issue type from the records currently visible in the configured Jira project. Completed and remaining metrics use this same current project/type eligibility; an issue moved out or no longer visible is excluded. Historical membership reconstruction, deleted/archived issue recovery, and cross-project tracking are out of scope.
9. **Snapshot/retrieval:** Use Jira Data Center REST API v2 search with explicit `startAt`/`maxResults` pagination and retrieve required per-issue changelog pages until Jira reports completion. Snapshot retrieval is best-effort over a recorded start/end interval, not a transactional Jira point-in-time snapshot. Any failed or truncated required page invalidates the run. There is no hard maximum request duration in the prototype; the 30-minute save freshness window applies after successful retrieval.
10. **Jira compatibility:** Prototype integration targets Jira Data Center/Server REST API v2 and personal access token authentication using the instance's documented bearer-token mechanism. Mock fixtures are sufficient for development tests. Live compatibility certification against every supported Jira release, a production compatibility matrix, and release qualification against a customer instance are out of scope; production use requires verification against the actual instance before release.
11. **Blocker/risk definitions:** A blocker candidate is an issue in a configured blocked status or with the configured Jira flag set. A risk candidate is either such a blocker or an issue manually designated a risk during review. For each candidate, the Delivery Manager chooses one of `customer-safe`, `internal-only`, or `unreviewed`; only `customer-safe` may appear in the customer draft, while the latter two are excluded. Per-issue decisions are transient and reset on the next generation.
12. **Planning source:** Configuration selects exactly one source: next future sprint or next unreleased fix version. Sprint selection is the earliest future sprint by start date, then ID; it must not already be closed. Release selection is the unreleased fix version with the earliest non-null release date on or after the current local date, then ID. Issues are included only when Jira explicitly assigns them to the selected sprint/version. If source or membership is ambiguous or unavailable, show unavailable; never fall back to the other source. Implementation must validate source-specific fields against the chosen instance.
13. **Health and rationale:** One required Green/Amber/Red value applies to both drafts. Rationale is optional, shared as review input, and internal-only; it is excluded from the customer draft. Health must be selected before approval or save.
14. **Persistence/lifecycle:** PostgreSQL stores only the single project's non-secret settings listed in §7. It stores no reports, snapshots, credentials, user identity, or per-issue classification. Configuration changes replace the current values; reset deletes configuration only. Report files have no automatic retention; operator deletion and database backup are manual. Config export, backup automation, and recovery tooling are out of scope.
15. **Local threat boundary:** The prototype protects the browser/API boundary with same-origin proxying by default and strict configured loopback-origin and Host checks when origins differ. HTTPS Jira URLs are required; credentials in URLs are rejected; redirects must remain on the configured origin; loopback/link-local targets are rejected, while organization private-network Jira hosts are allowed. Protection against a malicious local administrator or compromised DNS is out of scope.
16. **Markdown preview:** Raw HTML, remote images, and embeds are disabled. Preview HTML is sanitized; links permit HTTPS and `mailto:` only; executable schemes are rejected. Jira issue links are constructed from the validated configured Jira origin and issue key. Saved Markdown remains source text and is not rewritten by preview sanitization.
17. **Output structure:** Keep all defined headings and list all eligible items ordered lexicographically by issue key. Do not truncate. Use “No in-scope issues” for a zero-result section and “Unavailable: [reason]” for missing data. The UI must not invent a summary. Optional summary and actions are written by the Delivery Manager.
18. **Freshness:** Retrieval start/end and generation time are shown. Saving is allowed for 30 minutes after successful retrieval; after that a new complete retrieval is required. A failed refresh marks the current snapshot stale and disables save but retains unsaved edits for copying/review. No background refresh is performed.
19. **Observable language:** “Actionable” errors name the affected setting/permission and next step. “Material work items” means the configured in-scope issue list; “customer-relevant” is limited to content explicitly approved as customer-safe. “Concise” is not a separate automated content-generation requirement; no narrative compression occurs. Use the exact empty/unavailable labels in decision 17.
20. **Quality/performance:** Formal performance SLA, load benchmark, and large-project capacity guarantee are out of scope for this prototype. There is no latency or max-issue threshold; the app must display progress and allow cancellation where the request can be safely aborted. UI must use semantic controls, keyboard-operable review/save flows, and accessible labels. Current stable Chrome and Firefox are the manual smoke-test browsers; broader browser certification and formal accessibility audit are out of scope.
21. **Constitution check:** Compliance is a design requirement, not a claim that implementation has already been verified. The prototype decisions above resolve the relevant spec-level conflicts. Implementation must still pass the constitution's tests and review gates; any deviation blocks approval until corrected or formally amended.
22. **Acceptance coverage:** Tests must exercise timezone and DST boundaries, duplicate/reopened issues, failed/truncated pages, invalid credentials, token non-persistence, customer filtering before preview, explicit approval after edits, Markdown sanitization, save collisions, partial-write retry, 30-minute freshness, config reset, and configured-origin checks. This supplements the scenario tests and success criteria.

### Prototype Out of Scope

- Confluence integration, Jira Cloud, multiple projects, multi-user hosting, Jira writes, automated distribution, AI, health scoring, and story points.
- Historical reconstruction of issue project/type membership, deleted/archived issue recovery, and transactional point-in-time Jira snapshots.
- Live Jira-version certification and production compatibility qualification; the prototype uses REST v2 fixtures and must be verified against the actual instance before production.
- Automated semantic detection of sensitive material newly added in free-form Markdown; explicit human final approval remains required.
- Configuration export, automated backups/recovery, report-file cleanup/retention automation, performance SLA/load certification, formal accessibility audit, and broad browser certification.
- Defense against a malicious local administrator or compromised DNS infrastructure.

## 14. Constitution Check

- This specification follows the constitution's local-control, transient-credential, least-privilege, no-third-party-AI, human-accountability, audience-boundary, and stack requirements.
- Customer source content is filtered before preview/save; final free-form edits require explicit human approval. Automated semantic scanning of user-added free text is an explicit prototype limitation.
- Jira operations are read-only, output is local, and the user-facing services bind to loopback by default.
- The implementation stack is React 18/Vite, Node.js/Express, and PostgreSQL 15 via Docker; the earlier Python/Flask proposal in `project_spec.md` is superseded for this feature.
- This is spec-level alignment only. Implementation conformance must be verified through focused tests, build checks, and review before claiming the feature passes the constitution's quality gates.

## Commit History
3efe354 Module 17 working
af9d218 module 17 Clarify,plan,task commit
deb8dcb Module 17 fisrt commit
2400eb6 chore: project skeleton for prototype
865caff chore: project skeleton for prototype
3219e4b module 15 report
c7bfc5b module 15 py script and walkthru md
14b1355 module 15 bulk Apporach update commit
6605b55 more tasks addition for module 14 completion
34a3120 more tasks addition for module 14 task2
857a96f more tasks addition for module 14 task
c2d963b issues creation done
67513d1 update for github integration
ba444a9 github mcp
b62556b Merge origin/main initial commit into main
a257c63 Initial commit
33b77c2 ot rt back jira
4c1789c MCP json syntax error2
5b15da4 MCP json syntax error
8e41e85 MCP Server on Echo
7ba0041 AI skill Instructions and tools
9fa6b0d module 10 task report
160586a New Agents for jira  workflow
ae9411c New Agents for workflows
2464725 adding creating-instructions.agent.md
ad72e49 Agent memory management practicals
3728652 Creation of backlog.md
1fdf6cd Add Jira dashboard requirements and report template
36ed01c Add weekly Jira report specification
ee09477 Initial calculator with add and subtract
fb87bca Add initial project files

## Commit Count
31

## Project Files
.github/copilot-instructions.md
.github/prompts/to-calculate-compound-interest.prompt.md
.github/prompts/to-create-status-report.prompt.md
.github/prompts/to-creating-instructions.prompt.md
.github/prompts/to-run-unit-tests-and-coverage.prompt.md
.github/prompts/to-use-calculate-velocity.prompt.md
.github/prompts/to-use-format-report.prompt.md
.github/prompts/to-use-normalize-issues.prompt.md
.github/prompts/to-validate-safe-report-output.prompt.md
.github/prompts/to-work-with-jira-reporting-data.prompt.md
.gitignore
.vscode/mcp.json
.vscode/settings.json
JIRA-SPRINT-DASHBOARD-REQUIREMENTS.md
PROJECT_IDEAS.md
README.md
TODO.md
app.py
apps/api/Dockerfile
apps/api/package.json
apps/api/src/data/demo-report.json
apps/api/src/server.js
apps/api/test/server.test.js
apps/web/Dockerfile
apps/web/index.html
apps/web/package.json
apps/web/src/App.jsx
apps/web/src/main.jsx
apps/web/src/styles.css
apps/web/vite.config.js
backlog.md
calculator/main.py
calculator/operations.py
data/.gitkeep
data_fetcher.py
docker-compose.yml
formatting.py
instructions/calculate-compound-interest.agent.md
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/main.agent.md
instructions/run-unit-tests-and-coverage.agent.md
instructions/use-calculate-velocity.agent.md
instructions/use-format-report.agent.md
instructions/use-normalize-issues.agent.md
instructions/validate-safe-report-output.agent.md
instructions/work-with-jira-reporting-data.agent.md
modules/Customer-walkthrough.md
modules/Delivery-Manager-walkthrough.md
modules/Project-Overview-walkthrough.md
modules/Senior-Leadership-walkthrough.md
package-lock.json
package.json
project_spec.md
report_generator.py
reporting_service.py
reports/.gitkeep
reports/example.md
reports/instructions.md
reports/template.md
reports/weekly-status-report.md
requirements.txt
spec/analyze.md
spec/clarify.md
spec/constitution.md
spec/plan.md
spec/specification.md
spec/target-jira-inputs.md
spec/tasks.md
src/calculate.py
src/get_time.py
src/mcp-echo.py
templates/index.html
tests/test_calculate_velocity.py
tests/test_format_report.py
tests/test_normalize_issues.py
tests/test_report_generator.py
tests/test_reporting_service.py
tests/test_validate_walkthroughs.py
tools/calculate_velocity.py
tools/compound_interest.py
tools/format_report.py
tools/normalize_issues.py
tools/validate_walkthroughs.py
validation-rules.md
weekly-status-report-template.md
work/module-03-report.md
work/module-08-report.md
work/module-09-report.md
work/module-10-report.md
work/module-12-report.md
work/module-13-report.md
work/module-14-report.md
work/module-15-report.md
work/module-16-report.md
work/module03-task
