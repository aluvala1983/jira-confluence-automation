# Formatting Jira Issues as a Status Report

Use `tools/format_report.py` when supplied Jira issue data needs to be turned into a Markdown status report. It formats local JSON; it does not connect to Jira or verify issue data.

## Input and Command

- Accept a JSON array of issue objects or a JSON object containing an `issues` or `items` array.
- Support Jira REST issue objects with `key` and `fields.summary` / `fields.status`, as well as flattened objects with `key` or `id`, `summary` or `title`, and `status` or `state`.
- Run from the repository root:

  ```bash
  python tools/format_report.py --input-file path/to/issues.json --output-file path/to/report.md
  ```

- Both command-line arguments are required. Use paths supplied or approved by the user. The output file is overwritten if it already exists; check for an existing destination and confirm before replacing it.

## Report Interpretation

- The report contains Executive Summary, Completed Work, Upcoming Plans, and Blockers.
- The script treats statuses in Jira's `done` status category, or common names such as `Done`, `Closed`, `Resolved`, `Complete`, and `Completed`, as completed.
- Other statuses are listed as non-completed work to carry forward. Do not describe these as confirmed future commitments; the script cannot determine a team's plan.
- Blockers are issues whose status/category identifies them as `Blocked`, `Impeded`, or `On Hold`.
- Missing fields are represented with fallback text. Do not infer or invent issue facts from those fallbacks.

## Constraints

- Do not claim issues were fetched from Jira, are current, or are complete unless that was independently verified.
- Do not put credentials, tokens, or other secrets in the input file or report.
- If the input is malformed or the command fails, report the error and do not present an output as successfully generated.
- Review the generated Markdown for correct issue classification and appropriate destination before sharing it.
