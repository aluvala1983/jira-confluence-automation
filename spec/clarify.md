# Specification Review: Gaps, Contradictions, and Clarifications

**Reviewed documents:** [constitution.md](./constitution.md), [specification.md](./specification.md)
**Review perspective:** Senior engineering / implementation readiness
**Original assessment:** The review below identified items needing resolution. Dispositions in the final section supersede the original questions and have been incorporated into [specification.md](./specification.md) v1.1. Items explicitly marked out of scope are not part of the prototype.

## P0 - Resolve Before Implementation

### 1. Credential lifetime conflicts with connection validation

**References:** User Story 1, acceptance scenarios 1-2; FR-003 and FR-005; Key Entity: Generation Credential.

The user story has a distinct “validate connection” operation that authenticates with a personal access token. FR-003 allows the token only for an active generation request. It is unclear whether connection validation is itself part of generation, whether it is a separate request, and which UI component holds the token while validation and subsequent retrieval occur.

**Clarify:** Define the exact sequence for entering, validating, and using the token; whether validation is a separate user action; how many backend requests may use it; and when the UI/backend clears it. Ensure retries do not require unintended persistence or retention.

### 2. Reopened-issue policy is required but not specified

**References:** User Story 2, acceptance scenario 5; FR-013-FR-015; Error Handling; Open Question 4.

FR-014 requires an explicit project rule, but FR-001 does not include a reopened-issue setting. The open question offers materially different outcomes: count as completed, remaining open, or both. Counting both is possible under the current definitions, but may make report totals appear inconsistent.

**Clarify:** Choose a default policy or add a required configuration decision. Define how repeated done transitions, reopen transitions, and final status at snapshot time affect completed and remaining counts. State whether overlap is intentional and how it is labeled.

### 3. Customer disclosure can be bypassed by manual editing

**References:** FR-024-FR-026; User Story 3, acceptance scenarios 2-4; Constitution, “Audience-Safe Disclosure and Human Review.”

The specification filters sensitive and unclassified items before preview, but then permits free-form Markdown edits. It does not say whether a user can reintroduce excluded material, how edits are checked, or whether final approval re-runs disclosure checks. This leaves a path for accidentally saving sensitive material to the customer file.

**Clarify:** Define the enforcement boundary after editing: for example, classify structured content before rendering and validate the final customer Markdown at save, or explicitly make the Delivery Manager responsible for final disclosure with a mandatory confirmation. Define how false positives, manual overrides, and detected violations are handled.

### 4. Human review and approval are not a defined state or save gate

**References:** Constitution, “Audience-Safe Disclosure and Human Review”; FR-022, FR-026-FR-029; User Story 4.

The constitution requires review and approval before drafts are saved for sharing/distributed. The feature saves editable “drafts” and lets the user share them manually, but defines no distinction between draft save and approval, no approval action, and no condition preventing an unreviewed draft from being treated as final.

**Clarify:** Decide whether saving creates an unapproved draft or an approved shareable artifact. Define the user-visible review/approval action, whether both audiences must be approved independently, and whether an unapproved or disclosure-flagged draft may be saved.

### 5. Report source fields and human-authored content are unspecified

**References:** Goals; FR-010, FR-017, FR-021-FR-026; Key Entities: Jira Snapshot and Report Draft.

The specification calls for executive summaries, key outcomes, material work items, priorities, decisions/actions, internal commentary, staffing detail, and risk classification. It does not identify which Jira fields supply these values, which are entered by the Delivery Manager, or what the UI collects. “Deterministic” rendering alone does not define how Jira records become narrative text.

**Clarify:** For every report section, specify the source fields and selection/order rules, or define the corresponding human-input fields and required/optional status. Define whether issue summaries may be reproduced verbatim, how comments/descriptions are treated, and what happens when source values are missing.

### 6. The two-file save requirements conflict on partial success

**References:** FR-030; Error Handling, “One output write succeeds and another fails”; User Story 4, acceptance scenarios 2-3.

“Safe against partial output” may require an all-or-nothing pair save, while the edge case explicitly anticipates one file succeeding and the other failing. The spec requires truthful reporting but does not define whether the successful file is retained, rolled back, or retried.

**Clarify:** Choose and specify the contract: atomic pair write with rollback, or per-file success with a clear partial-save state and retry of only the failed output. Also define how confirmation and overwrite apply when only one destination already exists.

### 7. “Previous Monday” and the reporting-period review flow need a precise rule

**References:** User Story 2, acceptance scenario 1; FR-007-FR-008; SC-002; Key Entity: Reporting Period.

“Previous Monday” could mean the Monday of the just-completed week or the Monday immediately before the current date. The generation scenario says the period is selected when generation starts and then shown, while FR-008 requires review before retrieval. No exact ordering is stated. Daylight-saving behavior is mentioned but not how local boundaries map to Jira timestamps.

**Clarify:** Define the reference clock/time zone used to calculate the previous week, the behavior when generation is started on Monday, and the UI sequence: calculate and display period, user confirms, then retrieve. Specify conversion of local inclusive/exclusive boundaries to Jira timestamps and handling of daylight-saving transitions.

## P1 - Resolve Before Finalizing Design and Acceptance Tests

### 8. Jira issue scope across time is ambiguous

**References:** FR-009-FR-015; Key Entity: Jira Snapshot.

Completed work is based on status transitions during the period, while remaining work is a current-state count. The specification does not define whether an issue must belong to the configured project and an in-scope issue type both now and at the time of completion, or how project/type changes, deleted issues, moved issues, and archived issues are treated.

**Clarify:** Define the issue population for each metric and how Jira project/type membership is evaluated over time. State whether “remaining open work” is the entire current project backlog or a period-limited subset.

### 9. Retrieval completeness and snapshot consistency are underdefined

**References:** FR-011-FR-012, FR-018; Jira Snapshot; SC-004; Open Question 10.

Pagination is required, but the query, page termination rules, and changelog retrieval strategy are not described. Jira pages and per-issue changelogs are fetched over time and may change during retrieval; a set of fully paginated responses is not necessarily a point-in-time snapshot. “Stale” and “complete” have no freshness or consistency threshold.

**Clarify:** Identify the Jira endpoints/data required, pagination completion checks, treatment of inaccessible or truncated per-issue changelogs, and retry policy. Define whether the snapshot is best-effort with a recorded retrieval interval or requires consistency checks, and state the maximum acceptable retrieval duration/freshness.

### 10. Jira version and authentication support are deferred despite being foundational

**References:** FR-002; Assumptions; Open Question 1.

The supported Jira Data Center/Server version and PAT behavior are open, but these determine endpoint availability, authentication headers, pagination behavior, and permissions. The spec says support must be confirmed before production, without defining a development/test baseline or a release gate.

**Clarify:** Set the target Jira version (or range), supported auth flow, required REST API version/endpoints, and a test environment or representative fixtures. Define whether production release is blocked until compatibility is verified against a live supported instance.

### 11. Risk and blocker semantics are conflated

**References:** Goals; FR-017, FR-024-FR-025; Report Content; Open Questions 5 and 7.

FR-017 detects blocker/risk candidates only using blocked status and/or a Jira flag, but “risk” may include conditions beyond those signals. The spec does not define whether a flag is a blocker, a risk, or merely a candidate, nor how sensitive classification is configured or stored.

**Clarify:** Define blocker versus risk, exact candidate rules, the fields/statuses to inspect, and whether users classify individual records or configure rules. Specify how classifications persist and reset when the source issue changes.

### 12. Upcoming planning-window selection lacks deterministic rules

**References:** FR-001, FR-016; Report Content; Open Question 6; SC-005.

The authoritative source is configurable, but the selection rule for “next upcoming” is not defined when multiple future sprints/releases exist, a window is active, dates overlap, issues belong to multiple windows, or the source has no dates.

**Clarify:** Define selection ordering, inclusion/exclusion boundaries, issue membership rules, timezone handling, and fallback behavior. Specify whether the report shows an explicit unavailable state or a zero count when no window is found.

### 13. Required health selection and rationale behavior are unclear

**References:** FR-022; Report Content; User Story 3, acceptance scenario 4.

The user must select Green/Amber/Red, but the spec does not say whether the selection is required before preview, before saving either draft, or before approving a draft. It also does not define whether the rationale is shared or audience-specific, or whether customer rationale is separately classified/redacted.

**Clarify:** Define the requiredness and save/approval gate, where rationale is entered, whether it is shared between audiences, and which rationale content may appear in the customer draft.

### 14. PostgreSQL persistence and data lifecycle need a concrete model

**References:** FR-001; Key Entity: Project Configuration; Data and Persistence; Open Question 9.

PostgreSQL must persist non-secret configuration and preferences, but the specification does not define which settings persist, whether there is exactly one configuration, how configuration changes are versioned, or what reset/export/deletion means. Report files are durable while snapshots are transient, but no retention or cleanup behavior is defined.

**Clarify:** Enumerate persisted fields and their sensitivity, define configuration lifecycle and schema migration strategy, and decide retention/deletion/backup behavior for DB data and report files. Confirm whether generated human edits are recoverable only from Markdown.

### 15. Local-only deployment does not define the local threat boundary

**References:** Constitution, “Privacy, Least Privilege, and Local Control”; FR-031-FR-033; Technical Constraints and Architecture.

Loopback binding is specified, but there is no requirement for protecting local API routes from cross-origin requests, DNS rebinding, or requests from other local processes. Jira base URL is configurable and must be validated, but validation does not define how the backend prevents unintended requests to local or unrelated network services. “Local-only” does not itself establish a browser/API trust boundary.

**Clarify:** Define the intended threat model and controls for browser-to-API access, allowed origins/hosts, Jira URL validation, redirects, and private-network Jira instances. Avoid an allowlist rule that would unintentionally prohibit the intended organization-hosted Jira deployment.

### 16. Preview rendering and Markdown safety need a more precise contract

**References:** FR-033; Error Handling, “Unsafe or malformed source text.”

“Escape” is ambiguous if the application converts Markdown to HTML for preview. There is no renderer policy for raw HTML, links, images, or unsafe URL schemes; nor does the requirement state whether saved Markdown remains unmodified while preview sanitizes it.

**Clarify:** Specify whether raw HTML is disabled, which URL schemes are permitted, how Jira links are constructed/validated, and whether sanitization is applied only in preview or also at save. Define tests for scriptable URLs and embedded HTML.

### 17. Draft completeness, content ordering, and empty-state rules are missing

**References:** FR-021, FR-027; Report Content.

The heading list is defined but not the exact output shape, issue ordering, maximum detail/length, treatment of empty sections, unavailable metrics, or whether “required decisions/actions” is sourced from Jira or manually supplied. This affects deterministic outputs and customer readability.

**Clarify:** Define stable ordering and formatting, empty/unavailable labels, whether zero-count sections remain visible, item selection/limits, and the source/entry method for decisions and actions.

### 18. The phrase “freshness” and stale-report prevention have no measurable rule

**References:** FR-018; Error Handling, “Jira unavailable or stale data”; User Story 3, acceptance scenario 5.

The workflow is on-demand and the snapshot is transient, but no maximum age, refresh control, expiration event, or stale indicator behavior is defined. It is therefore unclear what makes a report stale or whether users can save a draft after a later API failure.

**Clarify:** Define when the snapshot is considered current, whether edits remain available after retrieval, when a failed refresh invalidates an earlier snapshot, and how the UI labels reports generated from older data.

## P2 - Improve Precision and Verification

### 19. Requirements use subjective terms without observable criteria

**References:** FR-006, FR-010, FR-017, FR-018, FR-027; Report Content.

Terms such as “actionable,” “unnecessary,” “useful,” “material,” “customer-relevant,” “concise,” and “freshness context” are not measurable. Different implementations could satisfy the wording while producing substantially different user experiences.

**Clarify:** Replace or supplement these terms with examples, field-level rules, limits, or observable acceptance assertions.

### 20. Success criteria do not set measurable quality or performance bounds

**References:** SC-001-SC-012; Constitution, “Quality and Verification Gates.”

The criteria are useful functional checks, but do not define performance expectations for project size, Jira request latency, maximum report generation time, maximum issue count, test coverage expectations, or supported browser/accessibility baseline.

**Clarify:** Set any required thresholds based on the target Jira project and intended local machine; otherwise state explicitly that there are no release thresholds beyond functional correctness and the constitution’s affected-build/test gates.

### 21. Constitution compliance is asserted while material decisions remain open

**References:** Specification §14, “Constitution Check”; Constitution, “Governance” and “Quality and Verification Gates”; Open Questions.

The constitution check states that the feature complies, although human approval semantics, final customer-output safety after edits, credential flow, and data lifecycle remain unresolved. The document is marked Draft and also lists unresolved business rules as pre-implementation work.

**Clarify:** Mark the constitution check as provisional and enumerate blocking findings until decisions are made; update it to a verified compliance statement after the spec is resolved.

### 22. No acceptance scenarios cover several explicit requirements

**References:** FR-018, FR-021-FR-025, FR-030-FR-033; SC-001-SC-012.

There are no scenario-level checks for safe preview rendering, configured timezone boundaries through DST, edit-induced customer disclosure, final approval, config persistence/deletion, unsafe Jira URLs, or the chosen pair-save failure contract.

**Clarify:** Once the related decisions above are settled, add acceptance scenarios and tests that exercise each security and lifecycle boundary, not only the renderer or API response in isolation.

## Original Recommended Resolution Order (Superseded)

1. Resolve P0 items 1-7 before implementation, especially the credential flow, reopened-issue calculation, final customer disclosure check, approval gate, and two-file save contract.
2. Resolve P1 items 8-18 before finalizing API/data architecture and test fixtures.
3. Tighten P2 wording and acceptance coverage before calling the specification implementation-ready.

## Dispositions

Every finding below has either been answered in specification §13 and incorporated into the relevant requirements, or is explicitly out of scope for the prototype.

| # | Disposition | Specification resolution |
|---|---|---|
| 1 | Answered | §13.1: validation and generation use separate loopback API requests; credentials are transient, cleared after response, and re-entered for generation. |
| 2 | Answered | §13.2: an issue completed at least once in-period counts once; if currently open it also appears in current-open count, with the measures clearly labeled. |
| 3 | Answered / limited | §13.3: filter source items before preview; require final human disclosure confirmation. Automated detection of sensitive free-form edits is out of scope. |
| 4 | Answered | §13.4: require separate explicit approval for each audience before saving; customer approval includes a disclosure confirmation. |
| 5 | Answered | §13.5 and §9: specify Jira fields, exclude descriptions/comments/worklogs, and make summaries/actions human-entered. |
| 6 | Answered | §13.6: write files independently; retain successful output, retry only failed output, and use unique suffixes rather than overwriting. |
| 7 | Answered | §13.7: use the last fully completed local Monday-Sunday period, show and confirm before retrieval, and convert zoned boundaries to UTC. |
| 8 | Answered | §13.8: current project/type membership governs both metrics; moved-out, deleted, archived, and historical membership reconstruction are excluded. |
| 9 | Answered / limited | §13.9: define REST v2 pagination, changelog retrieval, best-effort retrieval interval, failure conditions, and freshness. Point-in-time transactions are out of scope. |
| 10 | Answered / out of scope | §13.10: prototype targets Jira Data Center/Server REST v2 with PAT bearer authentication; live-version certification and production qualification are out of scope. |
| 11 | Answered | §13.11: define blocker candidates, manual risk designation, customer-safe/internal-only/unreviewed classification, and transient classification state. |
| 12 | Answered | §13.12: define one selected planning source and deterministic sprint/release selection and membership rules; no fallback. |
| 13 | Answered | §13.13: one shared mandatory health value; optional rationale appears only in leadership output. |
| 14 | Answered / out of scope | §13.14 and §7: enumerate persisted configuration, reset and report retention rules. Export, automated backup, and recovery are out of scope. |
| 15 | Answered / limited | §13.15 and §8: specify origin/host checks, HTTPS, redirect restrictions, and permitted private Jira hosts. Malicious local-admin/compromised-DNS defense is out of scope. |
| 16 | Answered | §13.16 and FR-033: disable raw HTML, sanitize preview, restrict URL schemes, disable embeds, and preserve saved Markdown text. |
| 17 | Answered | §13.17 and §9: define stable ordering, full lists, section headings, empty/unavailable text, and human-entered narrative/actions. |
| 18 | Answered | §13.18 and FR-018: snapshots can be saved for 30 minutes; stale snapshots require retrieval again; failed refresh disables saving while preserving edits. |
| 19 | Answered | §13.19: replace subjective descriptions with operational definitions and fixed labels. |
| 20 | Answered / out of scope | §13.20: define basic keyboard/semantic UI and smoke-test browsers. Performance SLA/load testing, formal accessibility audit, and broad browser certification are out of scope. |
| 21 | Answered | §13.21 and §14: constitution alignment is specified but implementation compliance remains subject to tests and review. |
| 22 | Answered | §13.22 and SC-011: enumerate required regression/security scenarios and focused tests. |

Prototype-level assumptions are decisions for this implementation, not claims about every Jira deployment. Before production use, verify the chosen authentication and required REST endpoints against the actual target instance.
