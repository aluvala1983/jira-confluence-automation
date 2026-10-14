# Implementation Tasks: Weekly Jira Status Report Generator

**Source plan:** [plan.md](./plan.md)
**Source specification:** [specification.md](./specification.md) v1.1
**Status:** Proposed

Tasks are grouped by delivery phase. Dependencies are explicit; a task may start only when its listed prerequisites are complete. M0 is required before claiming compatibility with a live target Jira instance. Fixture-based work that does not depend on live integration may proceed before M0 is complete.

## Phase 0 - Confirm Jira Instance Inputs

### T001 - Record non-secret target Jira and project inputs

**Depends on:** None
**Acceptance criteria:**

- A local, non-secret record identifies the target Jira Data Center/Server version, base URL, project key, IANA timezone, authentication method, issue type mapping, done statuses, blocker signals, and selected planning source.
- The record contains no token, password, or other secret and is not committed if it contains environment-specific details.
- Any unavailable value is explicitly recorded as a blocker rather than guessed.

### T002 - Verify Jira API and permissions contract

**Depends on:** T001
**Acceptance criteria:**

- REST v2 search, changelog pagination, required sprint/release fields, TLS certificate validation, and read permissions are checked against the target instance or a representative instance.
- A repeatable non-secret verification procedure is documented.
- Deviations from specification §13 are reported for spec update before implementation relies on them.

### T003 - Prepare Jira fixtures for prototype rules

**Depends on:** T001
**Acceptance criteria:**

- Fixtures cover stories, bugs, tasks, subtasks, unmapped types, done transitions with missing resolution dates, reopened issues, blockers, risk classifications, planning windows, and Jira errors.
- Fixtures contain no live Jira customer data, credentials, or personal data not necessary for the scenario.
- Fixture expectations match the specification's count, classification, and source-selection rules.

**Milestone M0 exit:** T001-T003 are complete; if live access is unavailable, this is recorded and live compatibility remains unverified.

## Phase 1 - Establish the Local Runtime

### T004 - Align the frontend runtime to React 18

**Depends on:** None
**Acceptance criteria:**

- The web workspace declares compatible React 18 and React DOM versions while retaining Vite.
- The lockfile is updated consistently using the repository package manager.
- The production frontend build succeeds.

### T005 - Verify Node.js/Express workspace and API startup

**Depends on:** None
**Acceptance criteria:**

- The API workspace uses the supported Node.js runtime and Express dependency.
- Existing workspace scripts start the API without interactive prompts.
- API health check returns a successful JSON response and binds to the configured host/port.

### T006 - Add PostgreSQL 15 to the local Compose stack

**Depends on:** None
**Acceptance criteria:**

- Compose runs PostgreSQL 15 with a persistent local volume and a health check.
- Database credentials are environment-driven and no secrets are committed.
- PostgreSQL is not published to an external host interface.
- API and web services can reach only the required Compose services.

### T007 - Configure local frontend/API routing and bind addresses

**Depends on:** T005, T006
**Acceptance criteria:**

- Frontend API calls use the same-origin `/api` proxy in local development.
- Host-facing frontend and API services bind to loopback by default.
- Compose networking permits the web/API services to communicate without exposing the API or database unnecessarily.
- A smoke check confirms the browser reaches API health through the configured proxy.

### T008 - Update local setup and run documentation

**Depends on:** T004, T005, T006, T007
**Acceptance criteria:**

- README instructions describe installing dependencies and starting/stopping the React 18/Vite, Express, and PostgreSQL 15 stack.
- Documentation describes loopback access and does not claim Jira generation is implemented before later milestones.
- A clean local setup can follow the documented commands successfully.

**Milestone M1 exit:** T004-T008 pass; local stack starts, frontend build passes, API health is reachable, and PostgreSQL is healthy but not externally published.

## Phase 2 - Configuration Persistence and Local API Boundaries

### T009 - Define and migrate the project configuration schema

**Depends on:** T006
**Acceptance criteria:**

- A migration creates storage for exactly one project's approved non-secret configuration fields.
- Schema constraints prevent multiple active project configurations where the specification requires one.
- Migrations apply cleanly to a fresh database and can be re-applied safely according to the chosen migration tool.
- No token, issue/changelog data, report body, user identity, or per-issue classification field is included.

### T010 - Implement configuration validation and repository operations

**Depends on:** T009
**Acceptance criteria:**

- Backend supports read, create/update, and reset for the approved configuration fields.
- Required values are validated, including Jira HTTPS origin, project key, timezone, issue mappings, status rules, and exactly one planning source.
- Database queries are parameterized.
- Validation errors identify the affected setting and a correction action without disclosing secrets.

### T011 - Implement configuration API and request validation

**Depends on:** T010
**Acceptance criteria:**

- Express routes expose validated configuration read/update/reset behavior with documented JSON success and error shapes.
- Request bodies are size- and shape-validated; unknown or secret-bearing fields are rejected.
- Tests verify invalid requests do not modify stored configuration.

### T012 - Enforce browser-to-API origin and host protections

**Depends on:** T007, T011
**Acceptance criteria:**

- Same-origin proxy operation succeeds.
- Requests with mismatched or unconfigured `Origin`/`Host` on state-changing endpoints are rejected.
- Tests cover allowed loopback origins, disallowed origins, absent/malformed host values, and direct API access.

### T013 - Validate configured Jira destination and redirects

**Depends on:** T010, T011
**Acceptance criteria:**

- Only HTTPS Jira URLs without embedded credentials are accepted.
- Loopback and link-local Jira destinations are rejected; configured private-network Jira hosts remain allowed.
- Redirects are limited to the validated configured origin.
- Tests cover malformed URLs, credential-bearing URLs, rejected addresses, permitted private hosts, and cross-origin redirects.

### T014 - Implement configuration reset and persistence tests

**Depends on:** T009, T010, T011
**Acceptance criteria:**

- Configuration persists across API restart.
- Reset removes configuration but leaves the `reports/` directory and its files untouched.
- Tests prove the configuration store cannot persist tokens, issue content, report contents, or per-issue review classifications.

**Milestone M2 exit:** T009-T014 pass; schema, lifecycle, request validation, and origin/destination protections are verified.

## Phase 3 - Reporting Domain and Deterministic Rules

### T015 - Define domain types and normalized snapshot shape

**Depends on:** T003
**Acceptance criteria:**

- Typed models exist for configuration, Jira issue, changelog entry, planning window, reporting period, snapshot metadata, review input, and audience draft.
- Snapshot fields include project, period, retrieval start/end, and generation timestamp.
- Snapshot and per-issue classification are in-memory only and have no persistence path.

### T016 - Implement timezone-aware reporting-period calculation

**Depends on:** T015
**Acceptance criteria:**

- The function calculates the last fully completed Monday 00:00 through the current-week Monday 00:00 in the configured IANA timezone.
- Start is inclusive and end exclusive; both zoned boundaries are independently converted to UTC instants.
- Tests cover generation on Monday, year transitions, and daylight-saving time changes.

### T017 - Implement issue eligibility and completion/open calculations

**Depends on:** T015
**Acceptance criteria:**

- Configured stories, bugs, and tasks are included; subtasks and unmapped types are excluded.
- Completed counts use changelog transitions into configured done statuses, work without resolution dates, and count each issue at most once.
- Current-open count uses current status; completed-then-reopened issues can appear in both separately labeled measures.
- Current project/type eligibility is applied consistently; moved-out or no-longer-visible issues are excluded.

### T018 - Implement planning-window selection and issue assignment

**Depends on:** T015
**Acceptance criteria:**

- Exactly one configured source is used: next future sprint or next unreleased fix version.
- Sprint and release tie-breaks follow specification §13.12.
- Only explicitly assigned issues are included.
- Missing, unsupported, ambiguous, or empty source results produce an explicit unavailable outcome; no fallback source is selected.

### T019 - Implement blocker/risk classification and stable report model

**Depends on:** T015, T017, T018
**Acceptance criteria:**

- Blocker candidates are derived from configured status/flag signals; risks may also be manually designated.
- `customer-safe`, `internal-only`, and `unreviewed` classification is represented per generation.
- Only customer-safe candidates are eligible for customer output.
- Issue rows are sorted lexicographically by issue key; zero and unavailable states use the exact specified labels.

### T020 - Implement snapshot freshness and deterministic calculation tests

**Depends on:** T016, T017, T018, T019
**Acceptance criteria:**

- Save validity is true only for 30 minutes after successful retrieval.
- Tests use a controllable clock and confirm stale snapshots cannot be saved.
- Identical fixture inputs yield identical normalized counts and ordering.
- Tests cover all M3 scenarios: duplicate/reopened transitions, absent resolution dates, issue scope, DST, planning ties, and missing/ambiguous planning data.

**Milestone M3 exit:** T015-T020 pass as focused unit tests without requiring Jira transport or UI.

## Phase 4 - Jira Read Integration

### T021 - Implement authenticated Jira HTTP client

**Depends on:** T002, T013, T015
**Acceptance criteria:**

- Client targets the verified Jira Data Center/Server REST API v2 endpoint contract.
- TLS certificate verification is enabled; redirects cannot leave the configured origin.
- PAT is sent using the configured bearer-token mechanism, never in a URL.
- Network errors and sanitized Jira error responses map to explicit domain/API errors.

### T022 - Implement connection validation request

**Depends on:** T011, T021
**Acceptance criteria:**

- A dedicated API request accepts a token in the request body and validates project access and required fields/permissions.
- Token is not persisted, logged, returned, or stored in browser storage; frontend input clears after response.
- Invalid auth, inaccessible project, and missing changelog/field access produce distinct actionable errors.
- Backend releases token references on success and failure.

### T023 - Implement paginated issue retrieval and normalization

**Depends on:** T017, T021
**Acceptance criteria:**

- Search uses explicit `startAt` and `maxResults`; retrieval continues until Jira indicates completion.
- Only required issue fields are requested.
- Normalized issue eligibility follows T017.
- Tests verify page-boundary independence and no issue duplication from pagination.

### T024 - Implement complete changelog retrieval

**Depends on:** T017, T021
**Acceptance criteria:**

- Required changelog pages are retrieved for eligible issues until Jira reports completion.
- Changelog timestamps and status transitions are normalized for period calculations.
- Missing resolution dates do not prevent completion calculation.
- Any inaccessible or truncated required changelog invalidates the run.

### T025 - Implement generation endpoint and incomplete-run handling

**Depends on:** T016, T018, T019, T022, T023, T024
**Acceptance criteria:**

- Generation is a separate request from connection validation and requires the user to re-enter the token.
- Request performs complete retrieval, normalization, calculations, and returns one transient snapshot with retrieval metadata.
- Any failed required page, timeout, rate limit, or upstream error invalidates the complete run; partial results are never returned as successful.
- API error output never contains the PAT or unnecessary upstream response content.

**Milestone M4 exit:** T021-T025 pass with mocked endpoint fixtures and failure injection. M0 is complete before claiming target-instance compatibility.

## Phase 5 - Report Rendering and Review UI

### T026 - Build configuration and connection UI

**Depends on:** T011, T012, T013, T022
**Acceptance criteria:**

- User can view/update the single project configuration and receive field-specific validation messages.
- Connection validation is an explicit action with token input; the token is held only in volatile component state while the request is active and cleared on response.
- Loading, success, and failure states are accessible and distinguishable.

### T027 - Build report-period confirmation and generation progress UI

**Depends on:** T016, T025, T026
**Acceptance criteria:**

- UI displays the calculated prior full-week dates and timezone before retrieval and requires confirmation.
- Generation progress and cancellation are shown where the request can be safely aborted.
- Failed/partial retrieval shows an error and never leaves a success-shaped report draft.

### T028 - Implement deterministic customer and leadership renderers

**Depends on:** T015, T017, T018, T019
**Acceptance criteria:**

- Both audience drafts use the same snapshot and the specified headings.
- Issue fields are limited to key, summary, type, status, and optional relevant due date; no descriptions, comments, or worklogs are fetched or rendered.
- Human-entered summary/actions are not fabricated; health is shared and rationale is internal-only.
- Stable ordering and exact empty/unavailable labels are applied.

### T029 - Build review, classification, and editing UI

**Depends on:** T026, T027, T028
**Acceptance criteria:**

- UI supports manual risk designation and required per-candidate `customer-safe`, `internal-only`, or `unreviewed` classification.
- UI supports independent Markdown edits, one shared health selection, optional rationale, optional summary/actions, and separate approvals.
- Unknown/internal-only candidate items remain absent from customer preview.
- Review state and issue data are transient and reset on a new generation; no review content is stored in PostgreSQL.

### T030 - Implement secure Markdown preview and freshness states

**Depends on:** T027, T028, T029
**Acceptance criteria:**

- Raw HTML, remote images/embeds, and executable URL schemes are disabled; preview HTML is sanitized.
- HTTPS and permitted `mailto:` links work; Jira links use the validated origin and issue key.
- UI displays retrieval interval, generation time, project, period, counts, and empty/unavailable states.
- Snapshot older than 30 minutes or marked stale after failed refresh cannot be saved; unsaved edits remain available for copying/review.

**Milestone M5 exit:** T026-T030 pass UI and renderer tests, including same-snapshot behavior, disclosure filtering, manual approval, sanitized preview, and stale/error states.

## Phase 6 - Safe Markdown File Output

### T031 - Implement unique report filename selection

**Depends on:** T028
**Acceptance criteria:**

- Output root is fixed to `reports/`; user-provided paths are rejected or not exposed.
- Base filenames include report period start date and audience.
- Existing names produce `-2`, then the next available positive integer before `.md`.
- Tests verify repeated collisions and no overwrite.

### T032 - Implement safe per-file atomic write

**Depends on:** T031
**Acceptance criteria:**

- Each approved draft is written to a temporary file in the destination directory, then renamed into its unique destination.
- A simulated write or rename failure does not leave a truncated destination file.
- Saved Markdown matches the approved source text; preview sanitation does not silently rewrite it.

### T033 - Implement independent pair-save status and failed-file retry

**Depends on:** T029, T030, T032
**Acceptance criteria:**

- Each audience requires its own approval; customer save additionally requires final disclosure confirmation.
- Files save independently and the UI reports success/failure per audience.
- If one save succeeds and the other fails, the successful file remains unchanged and retry targets only the failed file.
- Saved output contains no token or leadership-only rationale in the customer report.

**Milestone M6 exit:** T031-T033 pass collision, atomic-per-file write, partial pair failure, retry, approval, and output-content tests.

## Phase 7 - End-to-End Verification and Prototype Release

### T034 - Run acceptance and security verification

**Depends on:** T004-T033
**Acceptance criteria:**

- Frontend production build, backend checks, focused unit/API/UI tests, and migration tests pass.
- Every SC-001 through SC-012 has linked test or inspection evidence.
- Evidence covers token non-persistence, local origin/destination constraints, no partial retrieval success, customer disclosure/approval, freshness, reset, and partial save retry.
- Any target-instance test not performed is explicitly marked unverified; no production compatibility claim is made.

### T035 - Run complete local workflow smoke test

**Depends on:** T034
**Acceptance criteria:**

- From a clean local Compose startup, operator can configure project rules, validate mocked/authorized Jira access, confirm period, generate fixture-backed drafts, edit/classify/approve them, and save Markdown.
- A failed Jira retrieval and a simulated output failure show the required error states and permit safe recovery.
- User-facing services remain loopback-bound and PostgreSQL remains unpublished.

### T036 - Update onboarding and prototype limitations

**Depends on:** T008, T034, T035
**Acceptance criteria:**

- README documents setup, configuration fields, token handling, local-only boundaries, database lifecycle/reset, report output, troubleshooting, and target-Jira verification prerequisite.
- Documentation lists prototype exclusions: Confluence, Jira Cloud, writes, external distribution, AI, live compatibility certification, free-form semantic disclosure detection, performance SLA, and automated backup/export.
- Documented commands and behavior match the verified implementation.

**Milestone M7 exit:** T034-T036 pass; prototype behavior matches specification v1.1 and implementation limits are honestly documented.

## Dependency Summary

- T001 -> T002, T003
- T004-T008 establish the local runtime; T006 is also prerequisite to T009.
- T009 -> T010 -> T011; T012/T013 establish controls required by the integration phase.
- T015-T020 are independently testable domain work, with explicit dependencies among rules.
- T021-T025 depend on the security foundation and domain contracts; T002 is required for live-instance claims.
- T026-T030 deliver the review flow after backend/domain interfaces exist.
- T031-T033 implement safe file output after draft generation and approval flows are defined.
- T034-T036 are final verification, smoke-test, and documentation gates.

## Prototype Exclusions

Do not create tasks or implementation scope for Confluence integration, Jira Cloud, multiple projects, team-hosted/remote service, Jira writes, automated report distribution, AI/summarization, health scoring, story points, historical membership reconstruction, deleted/archived issue recovery, transactional point-in-time snapshots, automated backup/export/recovery, semantic detection of new free-form customer text, live Jira compatibility certification, performance SLA/load certification, formal accessibility audit, or broad browser certification.
