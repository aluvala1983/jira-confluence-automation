# Implementation Plan: Weekly Jira Status Report Generator

**Source specification:** [specification.md](./specification.md) v1.1
**Constitution:** [constitution.md](./constitution.md) v1.0.0
**Plan status:** Proposed
**Delivery approach:** Sequential milestones with testable exit criteria. No calendar estimates are assigned; phase completion is determined by the gates below.

## 1. Outcome

Deliver a single-user, local-only web application that reads one configured Jira Data Center/Server project, computes a complete weekly report snapshot, generates audience-separated Markdown drafts, and saves independently approved files safely.

The application MUST use React 18/Vite, Node.js/Express, and PostgreSQL 15 via Docker. Jira access is read-only. PostgreSQL stores only non-secret project configuration. The prototype does not access Confluence or distribute reports.

## 2. Delivery Principles

- Finish and verify each milestone before building on it.
- Keep Jira access, reporting calculations, audience policy, and file output behind testable backend modules; keep the frontend responsible for user workflow and presentation.
- Implement failure behavior with the success path: incomplete retrievals, stale snapshots, invalid credentials, unsafe content, and file-write errors must be visible and must not appear successful.
- Never persist or log the Jira token. Never persist Jira issue/changelog snapshots or report content in PostgreSQL.
- Tie implementation and tests to the functional requirements (FR), success criteria (SC), and constitution gates in the source specification.
- Maintain a working local run path and focused tests throughout development.

## 3. Phases and Milestones

### Phase 0 - Confirm Instance Inputs and Close Technical Risks

**Purpose:** Verify the configured target and ensure the selected API assumptions are usable before implementing integration behavior.

**Work:**

- Record the target Jira Data Center/Server base URL, version, project key, project timezone, and PAT authentication method in local, non-secret developer configuration or setup documentation. Never commit credentials.
- Confirm the project's exact issue type names, done statuses, blocked status and/or flag, planning source, and required fields.
- Confirm Jira REST API v2 search, changelog pagination, sprint/release fields, TLS certificate chain, and read permissions against the target instance or a representative test instance.
- Resolve the prototype configuration defaults and ensure fixture data represents the decided rules for reopened issues, issue inclusion, planning selection, and audience classification.
- Do not store the live token in environment files, tests, screenshots, or fixtures.

**Milestone M0 - Integration contract confirmed**

- A written, non-secret configuration record identifies the supported target instance and field/status mapping.
- A repeatable connectivity check confirms the required endpoints and authentication header against the target or representative instance.
- Required Jira facts from §13 of the specification are verified; any unavailable target access is recorded as a blocker rather than guessed.

**Exit gate:** Do not implement or claim live integration support until the API/authentication assumptions are verified. Fixture-based development can proceed for isolated modules while access is pending.

### Phase 1 - Reconcile the Repository and Establish the Runtime Foundation

**Purpose:** Bring the existing prototype into alignment with the approved stack and local deployment boundary.

**Work:**

- Inspect current app/workspace manifests, compose files, server binding, Vite proxy, and README instructions before changing them.
- Align the frontend dependency to React 18 as specified; retain Vite and the existing workspace structure where suitable.
- Retain Node.js and Express for the API; confirm runtime and workspace scripts are consistent.
- Add PostgreSQL 15 to the Docker Compose workflow with a persistent local data volume, health check, non-public database port, and environment-based credentials that are not checked in.
- Add a backend database connection module and migration mechanism; keep database access server-only.
- Confirm frontend-to-API communication uses same-origin `/api` proxying locally. Bind host-facing frontend and API access to loopback by default while allowing container-network service communication as required by Compose.
- Update developer setup/run documentation to reflect Docker/PostgreSQL and the approved stack. Remove obsolete instructions only where they conflict with this feature's target.

**Milestone M1 - Local stack runs**

- Fresh local setup starts frontend, API, and PostgreSQL 15 through documented commands.
- The UI can call the API health endpoint through the intended proxy; user-facing services are loopback-only and the database is not published externally.
- React reports version 18; the frontend production build and API startup checks pass.
- No Jira feature behavior is required at this milestone.

### Phase 2 - Configuration Persistence and Local API Boundaries

**Purpose:** Implement the safe, minimal persisted configuration and API protections before handling Jira credentials or report content.

**Work:**

- Define the configuration schema for one project: Jira origin, project key, IANA timezone, issue-type mappings, done statuses, blocker status/flag rules, one planning source, and filename preferences.
- Implement explicit database migration(s), parameterized queries, validation, create/update/read, and reset behavior.
- Validate required values and identify the configuration field that needs correction.
- Implement API request size/shape validation and JSON error conventions.
- Enforce loopback Host/Origin protections as specified; use same-origin proxy by default.
- Validate Jira URL scheme/origin, reject embedded credentials and loopback/link-local destinations, restrict redirects to the configured origin, and permit organization private-network Jira hosts.
- Verify configuration reset deletes DB configuration without touching report files.

**Milestone M2 - Safe configuration lifecycle**

- Configuration survives application restart and exactly matches the allowlisted fields in specification §7.
- Reset removes the stored configuration while leaving any report files unchanged.
- Tests show credentials, issue content, report contents, and per-issue classifications cannot be persisted through the configuration API.
- Origin/Host and Jira URL tests cover rejected and permitted cases.
- Database migrations apply cleanly to a fresh database and an existing local database.

### Phase 3 - Reporting Rules and Deterministic Domain Model

**Purpose:** Implement reporting calculations independently of Jira transport and UI.

**Work:**

- Implement pure functions for:
  - last fully completed Monday-Sunday period in an IANA timezone, start-inclusive/end-exclusive;
  - UTC conversion of zoned boundaries, including daylight-saving transitions;
  - issue type mapping and exclusion of subtasks/unmapped types;
  - completed unique issue counts from qualifying status transitions, including absent resolution dates;
  - current-open counts and intentional overlap for completed-then-reopened issues;
  - deterministic sprint or release selection and explicit unavailable results;
  - blocker candidates and manual risk classification states;
  - stable issue ordering and zero/unavailable section labels.
- Model snapshot retrieval timestamps and 30-minute save validity without persisting the snapshot.
- Define typed domain interfaces for Jira issue, changelog, planning window, normalized snapshot, review inputs, and rendered drafts.

**Milestone M3 - Business rules verified**

- Fixture/unit tests cover duplicate and reopened transitions, missing resolution dates, project/type scope, timezone week/year boundaries, daylight-saving transitions, planning-source tie-breaks, and missing/ambiguous planning data.
- Customer-safe, internal-only, and unreviewed classification behavior is tested.
- Identical inputs produce identical counts and deterministic report model ordering.

### Phase 4 - Jira Data Center/Server Read Integration

**Purpose:** Retrieve validated, complete source data without leaking credentials or reporting partial success.

**Work:**

- Implement an API client for the verified Jira REST v2 endpoints, with TLS certificate verification and bounded, explicit request behavior consistent with the spec's current prototype limits.
- Implement separate connection-validation and report-generation requests. Accept tokens only in request bodies, keep them in memory for each request only, and clear references in success and failure paths.
- Validate project and access to required fields/changelogs before treating configuration as ready.
- Retrieve in-scope issues using `startAt`/`maxResults`, following Jira completion metadata. Retrieve each required issue changelog through all pages.
- Normalize Jira records into the domain model; preserve generation and retrieval interval metadata.
- Surface authentication, permission, rate-limit, timeout, unsupported-field, truncated-page, and upstream errors without exposing token or unnecessary response content.
- Ensure any failed or incomplete required page invalidates the entire run; do not cache issue data or a partial successful snapshot.

**Milestone M4 - Complete snapshot retrieval**

- Mocked endpoint tests prove pagination reaches the final page for searches and changelogs.
- Failure injection proves interrupted, truncated, or inaccessible required data cannot produce a valid snapshot.
- Token tests verify it is not logged, returned in errors, persisted, or placed in URLs; frontend token input clears after each response.
- When M0 is available, a manual integration check verifies authentication and endpoint behavior against the target instance. This is not broad live-version certification.

**Dependency:** M0 must be complete before asserting actual target compatibility. Fixture development can occur earlier.

### Phase 5 - Report Generation, Disclosure, and Review Workflow

**Purpose:** Deliver the end-to-end user experience using one validated snapshot.

**Work:**

- Build React screens for configuration, connection validation, period confirmation, generation progress/error, and report review.
- Require confirmation of the calculated report period before retrieval.
- Render both drafts from the same snapshot using deterministic templates and stable issue-key ordering.
- Include only specified issue fields; do not fetch or render descriptions, comments, or worklogs.
- Provide human-entered executive summary, rationale, and decisions/actions; keep rationale internal-only.
- Require per-candidate classification as customer-safe, internal-only, or unreviewed; exclude the latter two from customer output.
- Provide independent editable Markdown for each audience while keeping shared health selection and audience-specific approval.
- Sanitize preview: disable raw HTML, images, embeds, and executable URL schemes; permit only HTTPS and `mailto:` where allowed.
- Show retrieval interval, generation time, project, dates, counts, empty/unavailable labels, classification state, and stale state.
- Enforce 30-minute snapshot freshness. A failed refresh disables save for that snapshot while preserving unsaved user edits for review/copying.
- Require health before approval; require explicit approval per audience; require final customer disclosure confirmation.

**Milestone M5 - Human-reviewed report drafts**

- End-to-end UI tests confirm both drafts use the same snapshot and can be edited independently.
- Tests prove internal rationale and sensitive/unreviewed candidates never enter the customer draft before manual free-form edits.
- Approval cannot be completed without health; customer approval requires final disclosure confirmation.
- Sanitization tests cover embedded HTML and unsafe schemes, and no raw Jira content is treated as executable.
- A failed refresh and a snapshot older than 30 minutes both disable saving and communicate why.

### Phase 6 - Safe Markdown Output and Recovery from Partial Save

**Purpose:** Save approved drafts locally without overwriting existing user work or misrepresenting file outcomes.

**Work:**

- Implement a fixed output root at `reports/`; do not accept arbitrary user paths.
- Generate period-start/audience filenames. On collision, select `-2`, then the next available positive integer before `.md`.
- Write each file to a temporary file in the same directory and rename to its unique destination only after the write succeeds.
- Save audience files independently. Retain a successfully written file if its partner fails, accurately report each result, and retry only the failed output.
- Ensure retries do not silently overwrite or duplicate an already successful audience output.
- Preserve the exact reviewed Markdown source for each saved report; preview sanitization must not rewrite the saved source.

**Milestone M6 - Reliable report files**

- Tests prove filenames are audience/period-specific, collision suffixes are deterministic, and no existing file is overwritten.
- Simulated write/rename failures do not leave a truncated destination.
- Partial-pair tests confirm a successful file remains unchanged and only the failed file is retried.
- Saved customer files contain the output of the approved customer draft and never contain credentials or leadership-only rationale.

### Phase 7 - Integration Verification, Documentation, and Prototype Release

**Purpose:** Verify the complete local workflow and document limitations before declaring the prototype usable.

**Work:**

- Run focused frontend build, backend tests/checks, domain tests, API tests, and database migration tests.
- Run local smoke tests using fixtures from clean Compose startup through config, period confirmation, snapshot generation, editing/approval, and Markdown save.
- When target Jira access is available, perform an explicitly authorized manual read-only smoke test and verify counts against known Jira examples. Do not use a live token in automated logs or committed fixtures.
- Update README with setup, configuration meanings, local-only behavior, PostgreSQL lifecycle/reset, report location, token handling, troubleshooting, and manual Jira compatibility prerequisite.
- Document known prototype exclusions and limitations, including no Confluence, no Jira Cloud, no AI, no automatic distribution, no live version certification, no semantic checking of newly typed free-form customer text, and no performance SLA.

**Milestone M7 - Prototype acceptance**

- All applicable constitution gates pass: focused tests, frontend production build, backend checks, migration tests, and privacy/security checks.
- Each specification success criterion SC-001 through SC-012 has test or inspection evidence; any unavailable live-instance evidence is explicitly recorded and does not become a claim of production readiness.
- Documentation accurately describes the actual stack and behavior.
- No unresolved implementation decision contradicts specification v1.1. Any material deviation requires updating the specification or constitution through their governance process.

## 4. Cross-Phase Verification Matrix

| Requirement area | Primary phase | Evidence |
|---|---:|---|
| React 18/Vite, Node/Express, PostgreSQL 15/Docker | 1 | Clean local start, version check, health endpoint, DB health |
| Config persistence, migrations, reset | 2 | Migration and repository/API tests |
| Reporting periods, issue rules, reopened work, planning | 3 | Pure function tests with fixtures and boundary cases |
| PAT lifetime, auth, pagination, changelogs, errors | 4 | Mocked API tests and, when available, target-instance manual check |
| Same-snapshot reports, classification, human review | 5 | Renderer and UI tests across both audiences |
| Sanitized preview and local threat boundary | 2, 5 | Origin/URL and sanitization security tests |
| Freshness and failure/stale states | 3-5 | Clock-controlled domain and UI tests |
| Safe filenames, pair-write outcomes, retries | 6 | Filesystem tests with collision and injected-failure cases |
| Documentation and acceptance coverage | 7 | SC checklist, docs review, focused release verification |

## 5. Dependencies and Gates

- **Target Jira details and access:** Required for confirming actual REST/authentication behavior; unavailable access blocks production compatibility claims, not fixture-based domain development.
- **Project-specific mappings:** Issue types, done statuses, blocked signals, planning source, and timezone must be supplied before a useful target-project report can be generated.
- **React major version alignment:** Current prototype manifest reports React 19; Phase 1 must align it to the constitution's React 18 requirement before feature UI implementation.
- **Database service alignment:** Current Compose setup does not include PostgreSQL; Phase 1 must add the specified PostgreSQL 15 service before database-backed configuration work.
- **No feature-phase bypass:** Do not implement Jira access before the credential, URL validation, and local API controls from Phase 2 are in place.
- **No success-shaped fallback:** A missing configuration, field, permission, page, classification, or output must remain an explicit error/unavailable state.

## 6. Scope Exclusions

The plan does not include Confluence integration, Jira Cloud, multiple projects, multi-user/remote hosting, Jira writes, automatic distribution, AI-generated content, health scoring, story points, historical issue membership reconstruction, deleted/archived issue recovery, point-in-time snapshots, automated backups/config export, semantic detection of new free-form customer text, production Jira compatibility certification, performance SLA/load certification, formal accessibility audit, or broad browser certification.

## 7. Definition of Done

The prototype is done when milestone M7 passes and:

1. A user can configure and validate one supported Jira project and generate a complete snapshot for the confirmed prior full week.
2. The two deterministic audience drafts use the same snapshot and meet all classification, human-review, and health requirements.
3. The user can approve, edit, and safely save each audience-specific Markdown file without silent overwrite.
4. Credentials and Jira content are not persisted beyond the explicitly permitted non-secret project configuration and local report files.
5. Failures, partial retrieval, stale data, and partial file-save outcomes are accurately shown.
6. The stack and deployment behavior match the constitution and the documentation describes limitations honestly.
