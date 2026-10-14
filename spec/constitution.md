# Project Constitution: Jira/Confluence Automation

This constitution defines the non-negotiable principles for product specifications, implementation, and review in this repository. Every feature spec and implementation must comply with it. If a requirement conflicts with a principle, record the conflict and resolve it explicitly before implementation.

## Core Principles

### 1. Verified Facts and Human Accountability

- Present Jira and Confluence-derived information accurately, with its source and relevant time context where practical. Never invent, silently infer, or present unavailable data as fact.
- Keep deterministic calculations and source data distinct from human-authored commentary and decisions.
- Delivery health ratings, risk acceptance, and final report wording remain under human control; do not infer or generate these automatically.
- Define business rules for status history, reopened work, time zones, and ambiguous source data in the relevant feature spec. Do not silently choose behavior where it changes reported outcomes.

### 2. Privacy, Least Privilege, and Local Control

- Treat Jira and Confluence content, personal access tokens, and generated reports as sensitive data.
- Use the current user's own credentials and only the permissions required for the requested operation. Never introduce a shared account by default.
- Keep credentials transient for the active operation. Do not persist them in files, the database, browser storage, URLs, or logs; clear references when the operation ends.
- Keep the application and project data local unless a separately approved specification explicitly changes the deployment boundary. Do not send source content to third-party AI, analytics, or summarization services.
- Do not log secrets or unnecessary personal or project content. Return actionable errors without exposing credentials or sensitive response bodies.

### 3. Audience-Safe Disclosure and Human Review

- Treat customer-facing and internal outputs as separate disclosure boundaries.
- Apply audience-specific inclusion and redaction rules before content reaches preview, save, export, or distribution surfaces. Customer-facing output must exclude internal commentary, staffing details, and sensitive risks unless a feature spec explicitly approves an exception.
- Generate related outputs from the same validated source snapshot to avoid factual drift.
- Require a person to review and approve generated drafts before they are saved for sharing or distributed.

### 4. Reliable and Honest Integrations

- Validate configuration, authentication, permissions, and required Jira/Confluence fields before presenting results as complete.
- Handle pagination, rate limits, timeouts, and upstream failures explicitly. Never report partial or stale data as a successful complete result; identify omissions and let the user retry or cancel.
- Respect the upstream service's authorization and API contracts. Do not perform writes to Jira or Confluence unless the feature specification explicitly authorizes the operation, its confirmation flow, and its failure handling.
- Make refresh behavior, data freshness, and time-zone or date-window boundaries explicit wherever they affect results.

### 5. Testable, Maintainable Engineering

- Keep business rules in testable units and separate them from UI rendering, HTTP transport, and persistence concerns.
- Add or update focused tests for changed behavior, including failure paths, boundary conditions, security-sensitive handling, and customer/internal disclosure rules where relevant.
- Prefer accessible, understandable interfaces with clear loading, empty, stale, and error states.
- Document setup, configuration, and operational behavior when a change affects how the application is built, run, deployed, or used.

## Technology and Architecture Constraints

- **Frontend:** React 18 with Vite.
- **Backend:** Node.js with Express.
- **Database:** PostgreSQL 15, run through Docker for local development and deployment workflows.
- Keep the frontend, backend, and database responsibilities separate. Access PostgreSQL through the backend; never connect to it directly from the browser.
- Manage schema changes as explicit, reviewable migrations. Use parameterized database access, enforce integrity constraints in the database where appropriate, and do not store Jira/Confluence credentials in application tables.
- Keep configuration environment-based and out of version control when it contains secrets. Compose services should expose only the ports needed for their intended use and should not publish the database unnecessarily.
- Use compatible versions and established repository conventions; any proposed deviation from this stack requires a documented rationale and explicit approval in the applicable spec.

## Product Scope and Specification Requirements

- Each feature spec must define its users, data sources, permissions, inputs and outputs, error behavior, privacy impact, and acceptance criteria before implementation.
- Jira/Confluence operations must state whether they are read-only or write-capable. Write-capable operations require explicit user intent, a review/confirmation step appropriate to their impact, and a clear result.
- Report generation must identify the reporting period and source snapshot, use documented rules, and preserve a review/edit step before saving or sharing.
- Dashboard and alert features must define their completion, blocker, risk, refresh, and stale-data rules; unresolved policy choices must remain explicit open questions rather than implicit defaults.
- Keep features within the approved scope of their spec. Do not add automatic external distribution, multi-project access, or issue/page mutation as incidental behavior.

## Quality and Verification Gates

A change is ready when all applicable gates pass:

1. Its behavior and acceptance criteria are represented in the relevant spec or tests.
2. Focused automated tests cover the changed behavior and important failure cases.
3. The frontend production build and backend checks pass for affected components.
4. Database changes are covered by migrations and, where applicable, migration/integration tests.
5. No credentials or sensitive project data are introduced into source, logs, browser persistence, or unintended outputs.
6. Documentation and examples reflect the actual behavior and deployment boundaries.

If a gate cannot be met, document the specific limitation and its impact; do not imply verification that did not occur.

## Governance

- This constitution applies to all repository work and takes precedence over conflicting implementation conventions. Product-specific specs may add stricter rules but may not weaken these principles without an approved amendment.
- Amendments must update this file, increment the constitution version, record the rationale and date, and identify affected specs or implementation decisions that need review.
- Feature specs and implementation plans must check their decisions against this constitution. Reviews must call out material violations before approval.
- Use semantic versioning for the constitution: MAJOR for incompatible principle changes, MINOR for new or materially expanded principles, and PATCH for clarifications that do not change obligations.

**Version:** 1.0.0  
**Ratified:** 2026-10-14  
**Last amended:** 2026-10-14
