# Implementation Backlog

This backlog is based on the project specification in [project_spec.md](./project_spec.md) and assumes a minimal working local Flask app is the first priority, with Jira integration and full production-hardening layered in after the core flow works.

Current progress: the local Flask app shell, config validation, reporting window logic, demo snapshot generation, and local preview/save flow are implemented in the workspace.

Status note: this is a working local demo of the weekly status workflow, not a live Jira-integrated system. The application UI and mock report data are present, but there is no production Jira PAT flow, no Jira API client, no changelog-based completed-work logic, and no real connectivity/permission validation yet. Phase 3+ items remain pending until those live-data behaviors are implemented.

## Phase 1: Setup

- [x] Confirm the project baseline and target runtime [custom skill]
  - Verify Python 3 version constraints and confirm Flask is the chosen web framework.
  - Record the initial local-only deployment constraints (loopback-only app, no remote hosting).
- [x] Scaffold the application structure [custom skill]
  - Create the package layout for the Flask app, config, services, templates, and report output.
  - Add a `reports/` directory for generated Markdown files and a safe output convention.
- [x] Create the initial dependency manifest [custom skill]
  - Add Flask and any HTTP client dependencies needed for Jira API calls.
  - Confirm pytest is included for early unit testing.
- [x] Define project configuration model [custom skill]
  - Create a config structure for Jira base URL, project key, timezone, issue type mappings, done statuses, blocker signals, and planning source.
  - Keep configuration local to the machine; do not persist PATs.
- [x] Set up environment and local-run workflow [custom skill]
  - Create a repeatable local run command for the app.
  - Document how to start the server on `127.0.0.1` and how to stop it.
- [ ] Establish the initial project folders and conventions [custom skill] [GitHub issue #1]
  - Create directories for routes, forms, services, templates, and report rendering.
  - Add helper modules for validation, Jira API access, and Markdown rendering.
- [ ] Implement robust error handling and logging configuration [custom skill]
  - Set up Python's standard `logging` module to capture app startup, configuration warnings, and Jira API request failures.
  - Add fallback responses or clear error pages for unhandled exceptions during local execution.
- [ ] Add basic unit tests for Jira API service and validation helpers [custom skill]
  - Create a `tests/` directory with `pytest` test cases for configuration parsing and mock Jira API responses.
  - Verify test execution workflow using the command line.
- [ ] Create a local README and developer runbook [custom skill]
  - Document prerequisites (Python version, virtual environment setup), how to configure local environment variables or config files, and troubleshooting tips for local deployment.

## Phase 2: Core Features

- [x] Build the Flask application shell [custom skill]
  - Create the app factory and route structure for configuration, preview, and save flows.
  - Add a home page that explains the weekly report workflow.
- [x] Implement configuration UI and validation flow [custom skill]
  - Add a form for Jira base URL, project key, timezone, issue type mappings, done statuses, and planning source.
  - Validate required fields before allowing generation to proceed.
  - Show actionable error messages when config values are missing or inconsistent.
- [x] Build the reporting period calculation logic [custom skill]
  - Compute the previous Monday through Sunday window in the configured project timezone.
  - Ensure the logic is inclusive of Monday 00:00 and exclusive of the following Monday 00:00.
  - Allow the user to review the selected week before generating.
- [x] Implement a report data model [custom skill]
  - Define a normalized data object for issue counts, completed work, remaining open work, next week's plan, and blockers.
  - Separate Jira-derived facts from manual review fields like health rating and rationale.
- [x] Create the customer and leadership draft templates [custom skill]
  - Build the consistent Markdown structure for both audience drafts.
  - Include headings for health, executive summary, completed items, remaining work, next week, blockers, and support needed.
  - Add audience-specific redaction rules for customer output.
- [x] Implement Markdown rendering for both reports [custom skill]
  - Render deterministic output from the report model.
  - Ensure the same data snapshot feeds both draft outputs.
  - Add placeholders for manual edits while keeping the structure consistent.
- [x] Implement preview and editing workflow [custom skill]
  - Show the generated draft in the browser before saving.
  - Allow the Delivery Manager to review and edit the Markdown in-place.
  - Keep a clear distinction between Jira facts and manual commentary.
- [x] Implement safe file saving behavior [custom skill]
  - Save Markdown drafts under `reports/` with year/date/audience naming conventions.
  - Prevent silent overwrite by prompting or creating a unique filename.
  - Confirm the save path before final write.

## Phase 3: Integration

- [ ] Integrate Jira authentication flow [MCP]
  - Prompt for the user's PAT only during a generation request.
  - Keep the PAT in memory only for the active request and clear the reference afterward.
  - Surface clear errors for invalid credentials or insufficient access.
- [ ] Implement Jira API client [MCP]
  - Build a client for Jira Data Center/Server REST endpoints.
  - Add pagination handling to fetch complete result sets.
  - Handle rate-limit and API errors without reporting partial success as complete.
- [ ] Validate Jira connectivity before generation [MCP]
  - Verify the base URL, project access, permissions, and field availability.
  - Confirm that required issue types, statuses, and changelog access exist.
  - Surface specific error messages for auth, project, field, or changelog failures.
- [ ] Implement issue filtering and normalization [MCP]
  - Include stories, bugs, and tasks; exclude subtasks.
  - Normalize issue records for counts and summaries.
  - Filter issues based on the configured project and reporting window.
- [ ] Implement completed-work logic using changelog history [MCP]
  - Use status-change history to count issues with a configured done status during the reporting period.
  - Handle reopened issues and repeated transitions consistently.
  - Avoid double counting a single issue in the same reporting period.
- [ ] Implement remaining-open logic [MCP]
  - Count in-scope issues that are not in a configured done status at generation time.
  - Keep output aligned with project configuration and reporting-period boundaries.
- [ ] Implement next-week planning logic [MCP]
  - Determine the next sprint/release source based on the configured project rules.
  - Count and summarize issues assigned to the next planned work window.
  - Handle the case where no upcoming sprint/release exists without guessing.
- [ ] Implement blocker and risk detection [MCP]
  - Look for configured blocked status and/or flag signals in Jira issue data.
  - Show issue key, summary, status, and Jira link in the report.
  - Distinguish current blockers from potential risks and customer-sensitive items.
- [ ] Implement health selection workflow [custom skill]
  - Require manual Green/Amber/Red selection by the Delivery Manager.
  - Show a rationale field for human-written evidence.
  - Keep health selection outside of automated calculation logic.
- [ ] Build the same-snapshot generation path [custom skill]
  - Ensure both customer and leadership reports are generated from one validated Jira snapshot.
  - Prevent drift between drafts by reusing the same normalized data.

## Phase 4: Testing

- [ ] Write unit tests for config and date logic [custom skill]
  - Validate reporting-period calculations across week boundaries.
  - Test required field validation and error handling.
- [ ] Write unit tests for Jira filtering and normalization [custom skill]
  - Test story/bug/task filtering and subtask exclusion.
  - Validate normalization of issue payloads and counts.
- [ ] Write unit tests for completed/open/planning logic [custom skill]
  - Confirm completed counts use status history and avoid double counting.
  - Validate remaining-open logic and next-week plan logic.
- [ ] Write unit tests for report rendering [custom skill]
  - Test both customer and leadership Markdown outputs.
  - Verify audience-specific exclusion rules and headings.
- [ ] Write tests for safe file output [custom skill]
  - Ensure write failures are surfaced clearly.
  - Confirm report filenames avoid silent overwrite.
- [ ] Add integration-test coverage for the API flow [custom skill]
  - Mock Jira responses for success and failure paths.
  - Verify pagination, rate-limit handling, and invalid credential errors.
- [ ] Run end-to-end smoke tests locally [custom skill]
  - Validate the full workflow from config to report generation.
  - Confirm the generated Markdown files are saved correctly and displayed in the UI.

## Phase 5: Documentation

- [ ] Document the app workflow for the Delivery Manager [custom skill]
  - Explain how to configure Jira access, select the reporting week, and generate drafts.
  - Describe the difference between customer and leadership versions.
- [ ] Document security requirements [custom skill]
  - Clarify that the PAT is temporary and never persisted.
  - Explain the local-only deployment model and no-AI requirement.
- [ ] Document output conventions and report filenames [custom skill]
  - Describe the naming pattern and location for saved Markdown reports.
  - Explain how to handle existing files and duplicate names.
- [ ] Add troubleshooting guidance [custom skill]
  - Document common Jira authentication and access issues.
  - Add instructions for checking configuration and missing fields.
- [ ] Add developer onboarding notes [custom skill]
  - Document local setup steps, dependency installation, and run commands.
  - Add guidance for testing and debugging the app locally.
- [ ] Review the backlog against the acceptance criteria [custom skill]
  - Confirm each acceptance item is traceable to a build task.
  - Update the implementation plan if requirements change during development.

## Recommended execution order

1. Phase 1: Setup
2. Phase 2: Core Features
3. Phase 3: Integration
4. Phase 4: Testing
5. Phase 5: Documentation

This sequence keeps the first pass focused on a working local Flask app and a reliable weekly status generation flow before deeper Jira integration and hardening.
