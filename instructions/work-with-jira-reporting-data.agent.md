# Jira Reporting Data Workflow

Use this workflow to retrieve and format Jira issue data, draft JQL for common reporting needs, and summarize sprint data.

## Input Format

Accept any available subset of:
- Jira deployment type/version and base URL, if known.
- Project key or permitted project scope.
- Reporting period, timezone, and purpose of the query.
- Issue types, statuses, assignee, sprint, or other filters.
- Jira issues, REST API responses, sprint data, or a request to fetch data.
- Desired output format, audience, and summary fields.

Ask for missing information when it changes query scope or report meaning. Do not request or accept credentials in chat; use only an authorized, configured Jira client/session for live access. If no live client or payload is available, provide JQL or a formatting template rather than claiming data was fetched.

## Processing Steps

1. Confirm the project and date boundaries. For a previous-Monday-through-Sunday reporting week, use an inclusive Monday start and exclusive following-Monday boundary; express date filters in a Jira-compatible way and state any timezone assumptions.
2. For common reporting needs, draft focused JQL for the requested case, such as issues by project and reporting period, unresolved work, blockers, or sprint scope. Use only fields and functions known to exist in the target Jira deployment; identify assumptions or version-dependent syntax.
3. When fetching live data, use the authorized Jira Data Center/Server REST API configuration and request only necessary fields. Follow pagination to completion and respect rate limits and API errors. Do not present partial results as complete.
4. Normalize retrieved issues consistently, preserving key, summary, issue type, status, assignee when relevant, sprint/release, and issue URL when available. Keep missing values explicitly marked as unavailable rather than inferred.
5. Summarize sprint data in a compact table with sprint name/state/date range and available issue counts by status or requested category. Reconcile totals against the fetched records and disclose missing, duplicate, or paginated data concerns.
6. Distinguish fetched Jira facts from assumptions, query examples, and any human interpretation.

## Output Format

Return Markdown with only the sections applicable to the request:

- **JQL** — fenced `jql` query and a brief description of what it selects.
- **Issues** — a table of normalized issue fields requested or needed for the task.
- **Sprint Summary** — a table with sprint name, state, date range, total issues, and requested status/category counts.
- **Scope and completeness** — project, reporting boundaries/timezone, source/mode (live data or supplied payload), and pagination/completeness status.
- **Notes** — field assumptions, unavailable values, API errors, or any interpretation requiring confirmation.

If no issue or sprint records were supplied or fetched, return the JQL or an empty table template and state that no live records were retrieved.

## Constraints

- Never fabricate Jira issues, counts, sprint dates, fields, links, API results, or execution status.
- Do not claim a JQL query was run unless it was actually executed against Jira.
- Do not claim a result set is complete unless every page was fetched successfully.
- Keep query scope limited to the requested project and reporting period; avoid broad or unbounded queries unless explicitly requested.
- Do not assume custom fields, plugins, status names, sprint functions, or Jira-version behavior. Mark uncertain syntax and fields for verification.
- Do not expose, log, or repeat personal access tokens, cookies, or other credentials.
- Do not create, edit, transition, or delete Jira issues; this workflow is read-only.
- Use issue counts rather than story points or velocity unless the user explicitly requests otherwise.
