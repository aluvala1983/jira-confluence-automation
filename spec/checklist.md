# Specification Implementation Checklist

**Reviewed specification:** [specification.md](./specification.md) v1.1  
**Review date:** 2026-10-14  
**Scope:** Current repository implementation, tests, and locally running prototype at review time.

## Status Definitions

- **Implemented:** Corresponding behavior exists in the current application.
- **Partial:** Some related behavior exists, but one or more required parts are missing or differ from the specification.
- **Not implemented:** No implementation of the required behavior was found.
- **Works:** Exercised successfully by a focused test, build, or live local request.
- **Not verified:** Not exercised, or depends on external Jira/database behavior not present in the current application.
- **N/A:** The criterion cannot meaningfully be exercised because its feature is not implemented.

Passing a local fixture check does not establish Jira integration, production compatibility, or report correctness. The user-requested local-data mode is explicitly identified separately from requirements that still describe live Jira access.

## Summary

| Area | Result |
|---|---|
| Current application behavior | A React/Vite status page and a local Express API with health and synthetic fixture endpoints. |
| Active data source | Synthetic local fixture (`DEMO`); `/api/health` reports `dataSource: local-fixture` and `jiraIntegration: disabled`. |
| Jira integration and weekly report generation | Not implemented; this is consistent with the latest request to defer Jira and always use local data, but does not satisfy Jira-dependent requirements in specification v1.1. |
| Backend tests | 3 passed, 0 failed (`npm test --workspace @weekly-report/api`). |
| Frontend production build | Passed (`npm run build:web`). |
| Live local checks | `GET /api/health`, `GET /api/report-data`, and frontend `/` returned HTTP 200. |
| PostgreSQL | Not part of the current Compose stack or application runtime; no app-to-database integration was tested. |
| Overall | Prototype foundation works; the specified report product is largely unimplemented. |

## Functional Requirements

| ID | Requirement (summary) | Implemented? | Does it work? | Evidence / gap |
|---|---|---|---|---|
| FR-001 | Configure Jira URL, project, timezone, mappings, statuses, blocker signals, planning rule | No | N/A | No configuration UI, API, or persistence. Current fixture is fixed synthetic data. |
| FR-002 | Connect read-only to supported Jira Data Center/Server REST API | No | N/A | Jira integration is disabled; no Jira client or API routes exist. |
| FR-003 | Accept PAT only in explicit validation/generation request bodies and clear references | No | N/A | No credential requests or Jira routes exist. |
| FR-004 | Never persist/expose PAT in storage, URLs, reports, logs, or errors | Partial | Not verified | No PAT handling exists, so no token leak path is present in current routes. There are no dedicated security tests covering future credential flows. |
| FR-005 | Validate configuration, auth, project access, fields, and changelogs before fetching | No | N/A | No configuration or connection validation. |
| FR-006 | Give actionable configuration failures without secrets or unnecessary Jira data | No | N/A | No configuration validation/error behavior. |
| FR-007 | Calculate prior completed Monday-Sunday period in configured timezone with correct boundaries | No | N/A | Fixture contains a static UTC date range; no period calculation. |
| FR-008 | Show calculated period before retrieval and require confirmation | No | N/A | No period UI or generation action. |
| FR-009 | Map issue types; include Story/Bug/Task and exclude subtasks/unmapped types | No | N/A | Fixture includes three typed demo issues but performs no filtering or mapping. |
| FR-010 | Use issue counts, not points; team-level summaries | No | N/A | No report calculations or summary output. |
| FR-011 | Paginate all required Jira issue and changelog results | No | N/A | No Jira HTTP client. |
| FR-012 | Surface Jira errors, rate limits, timeouts, and permissions; reject partial success | No | N/A | No Jira integration or generation state. |
| FR-013 | Count unique in-scope issues transitioned into done during period, including missing resolution date | No | N/A | Fixture has one `completedAt` value but no changelog-based calculation. |
| FR-014 | Count each qualifying issue once; allow intentional overlap with currently open | No | N/A | No completed/open calculation or labels. |
| FR-015 | Calculate current open work from configured done statuses | No | N/A | No status-based calculations. |
| FR-016 | Select configured sprint/release plan; report unavailable rather than guess | No | N/A | No planning-source integration or output. |
| FR-017 | Detect configured blocker/risk candidates and show required fields/link | No | N/A | Fixture has a blocked-looking status but no candidate logic, links, or audience rules. |
| FR-018 | Preserve snapshot provenance and enforce 30-minute save freshness | No | N/A | No generated snapshot, timestamps, save flow, or freshness logic. |
| FR-019 | Render separate customer and leadership drafts from one normalized snapshot | No | N/A | No report renderer or drafts. |
| FR-020 | Deterministic template rendering; no AI or invented facts | No | N/A | No rendering. The current API serves static fixture JSON only. |
| FR-021 | Render required headings and audience-specific content | No | N/A | No report output. |
| FR-022 | Require human-selected Green/Amber/Red health; no automatic score | No | N/A | No review UI. |
| FR-023 | Distinguish Jira facts from human content | No | N/A | No report or review model. |
| FR-024 | Exclude internal/staffing/sensitive content from customer output before preview/save | No | N/A | No audience filtering or customer draft. |
| FR-025 | Classify each candidate per generation; only customer-safe candidates may appear in customer draft | No | N/A | No classification workflow or persistence/state model. |
| FR-026 | Independent edits, per-audience approval, customer final disclosure confirmation | No | N/A | No editing, approval, or save controls. |
| FR-027 | Preview project, dates, counts, audience, and outstanding review items | No | N/A | No report preview. |
| FR-028 | Save editable Markdown under fixed `reports/` with period/audience filenames | No | N/A | No file-save endpoint or report generation. |
| FR-029 | Avoid overwrites and create unique filename | No | N/A | No output file handling. |
| FR-030 | Atomic independent writes, per-file result, retry only failed file | No | N/A | No save, retry, or atomic write implementation. |
| FR-031 | Local loopback operation and verified HTTPS Jira connections | Partial | Partial | Dev servers bind loopback by default and Compose publishes only the web UI on loopback; container API uses internal `0.0.0.0`. Jira HTTPS/TLS behavior is unimplemented. |
| FR-032 | Do not send reports/data/credentials to remote services | Partial | Works for current paths | Current API reads local fixture; no Jira or external service calls in current implementation. This does not establish behavior for future integrations. |
| FR-033 | Safe Markdown preview, allowed links only, disabled raw HTML/images/embeds; preserve Markdown source | No | N/A | No Markdown editor or preview. |

## Success Criteria

| ID | Success criterion | Implemented? | Does it work? | Evidence / gap |
|---|---|---|---|---|
| SC-001 | Configure Jira and distinguish invalid auth, project, changelog permission, unsupported fields | No | N/A | No configuration or Jira validation; no live Jira calls. |
| SC-002 | Correct timezone-aware reporting period including Monday, year, and DST tests | No | N/A | No period function or tests. |
| SC-003 | Fixture tests for issue scope, changelog completion, missing resolution, deduplication | No | N/A | The three backend tests cover fixture endpoint, health mode, and port parsing only. |
| SC-004 | Pagination-independent complete snapshot; failed fetch never succeeds/saves | No | N/A | No pagination, snapshot, or generation behavior. |
| SC-005 | Correct next-plan counts and explicit unavailable state | No | N/A | No planning integration or logic. |
| SC-006 | Sensitive/internal/unclassified content excluded from customer preview and saved Markdown | No | N/A | No reports, disclosure filtering, preview, or save. |
| SC-007 | Deterministic audience drafts from same snapshot | No | N/A | No renderer or snapshot. |
| SC-008 | Shared health, rationale, independent edits/approval, disclosure confirmation | No | N/A | No review UI. |
| SC-009 | Collision safety, accurate save state, retry preserves successful output | No | N/A | No save implementation or tests. |
| SC-010 | Prove PAT absence from all prohibited destinations | Partial | Not verified | No PAT is currently accepted; there are no dedicated tests/inspection artifacts for token handling. |
| SC-011 | Build/check/test/migration gates and listed focused security/domain tests | Partial | Partial | Frontend build and 3 API tests pass. Backend checks, domain/UI tests, PostgreSQL migrations, origin/host, Markdown, period, approvals, reset, and retry tests are absent. |
| SC-012 | React 18/Vite, Node/Express, PostgreSQL 15/Docker; loopback binding | Partial | Partial | Vite and Express run locally and bind loopback by default. Web package currently uses React 19; Compose has no PostgreSQL service; Docker is unavailable in the environment. |

## User Scenarios and Other Specification Areas

| Spec area | Implemented? | Does it work? | Current assessment |
|---|---|---|---|
| User Story 1: configure and validate Jira | No | N/A | No settings form or connection-validation request. |
| User Story 2: generate complete weekly snapshot | No | N/A | No Jira retrieval, date calculation, normalization, or metrics. |
| User Story 3: review/edit audience drafts | No | N/A | UI is a single status panel with an API health badge; no review workflow. |
| User Story 4: safe Markdown save/retry | No | N/A | No report output or save API. |
| Error and edge-case behavior (§10) | Partial | Partial | Local health and fixture behavior work. Jira, stale data, partial retrieval, classification, save collisions, and retry errors are not implemented. |
| Data persistence (§7) | No | N/A | PostgreSQL is absent from Compose and no database client, schema, or migrations exist. |
| API/frontend responsibilities (§8) | Partial | Partial | Browser-to-Express same-origin proxy and health check work. Required backend responsibilities for Jira/reporting are absent. |
| Report content and templates (§9) | No | N/A | No generated report files or drafts. |
| Accessibility and manual browser checks (§13.20) | Partial | Not verified | Basic semantic text and section markup exist; keyboard workflow and cross-browser review are not implemented or tested. |

## Verification Performed

- `npm test --workspace @weekly-report/api` — **passed, 3 tests**.
- `npm run build:web` — **passed**.
- `GET http://127.0.0.1:3001/api/health` — **HTTP 200**; response reports local fixture mode and disabled Jira integration.
- `GET http://127.0.0.1:3001/api/report-data` — **HTTP 200**; returns the synthetic `DEMO` fixture.
- `GET http://127.0.0.1:5173/` — **HTTP 200**; Vite serves the frontend.
- The active fixture is static sample data. It is not the configured `EPM-INBL` Jira project and must not be represented as live project information.
- No PostgreSQL-backed test was possible because no database service is defined in the current Compose stack.

## Main Gaps and Scope Note

The current implementation is intentionally local-fixture-only following the request to deprioritize Jira integration. That operating mode must remain clearly labeled. It differs from Jira-dependent portions of specification v1.1; therefore those requirements are marked unimplemented rather than treated as satisfied by synthetic examples.

The repository also currently declares React 19 instead of React 18, and the Compose stack has no PostgreSQL service. Report configuration persistence, generation, review, Markdown preview, file output, and almost all specified acceptance tests remain unimplemented.

