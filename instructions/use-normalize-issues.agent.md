# Normalizing Jira Issues

Use `tools/normalize_issues.py` when raw Jira issue JSON needs filtering and conversion into a consistent dataset for metrics or summaries. It processes local JSON only; it does not connect to Jira or verify payload completeness.

## Input and Command

- Accept a JSON array of issue objects or a JSON object containing an `issues` or `items` array.
- Support Jira REST issue objects with `fields.issuetype`, and flattened objects with `issuetype` or `issue_type`.
- Run from the repository root:

  ```bash
  python tools/normalize_issues.py --input-file path/to/issues.json --output-file path/to/normalized.json
  ```

- Both command-line arguments are required. Use paths supplied or approved by the user. The output file is overwritten if it already exists; check the destination and confirm before replacing it.

## Filtering and Output

- Include only Story, Bug, and Task issue types (case-insensitive).
- Exclude subtasks, whether the Jira issue type has `subtask: true` or is named `Sub-task` / `Subtask`. Other issue types are excluded too.
- Output JSON with an `issues` array and `metrics` object. Normalized issues retain `key`, `summary`, `issue_type`, `status`, `assignee`, `created`, `updated`, `resolved`, `priority`, `project`, and `labels`.
- Missing scalar fields are `null`; empty/missing labels become an empty list. Jira name/display-name objects are reduced to readable text.
- Metrics report input and included totals, filtered subtask and other-type totals, and counts by issue type and status. Missing statuses are counted as `Unspecified`.

## Constraints

- Do not invent missing issue data or claim the payload is current, complete, or fetched from Jira unless independently verified.
- Do not include credentials, tokens, or other secrets in input or output.
- If input is malformed or the command fails, report the error and do not claim successful normalization.
- Review the normalized records and filter counts before using them for metrics or summaries.
