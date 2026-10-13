# Safe Report Output Validation

Validate a weekly status report and its proposed Markdown destination before it is saved.

## Input Format

Accept:
- The report Markdown content or a path to a report file.
- The report audience (`customer` or `leadership`), if known.
- The reporting period and proposed output path, if available.

If an input is not supplied or cannot be inspected, mark the affected check as not checked instead of assuming it passes.

## Processing Steps

1. Read the report content and, when provided, inspect the destination without writing or overwriting files.
2. Check that the content is valid UTF-8 Markdown and includes the expected report sections: overall delivery health, executive summary, completed work, remaining open work, next week's plan, and blockers/risks or decisions/support needed.
3. Check that the stated audience and reporting period agree with the provided metadata and destination filename.
4. For customer reports, flag internal commentary, staffing details, and content explicitly identified as sensitive. Do not decide that ambiguous content is safe; flag it for Delivery Manager review.
5. Flag apparent credentials or tokens in report content. Do not echo any suspected secret in the result.
6. If a destination is provided, verify it is within the intended `reports/` directory, uses a Markdown extension and the reporting-period/audience naming convention, and does not already exist. Flag path traversal or a destination that resolves outside `reports/`.
7. Return each check's result and the specific remediation needed for failed or unverified checks.

## Output Format

Return a concise Markdown validation report:

- **Overall:** `PASS` only when every applicable check passes; otherwise `FAIL` or `NOT CHECKED`.
- **Checks:** A table with `Check`, `Result` (`PASS`, `FAIL`, or `NOT CHECKED`), and `Details`.
- **Next action:** State whether the report is ready for review/save or identify what needs correction or human review.

## Constraints

- Do not save, rename, overwrite, or edit the report during validation.
- Never repeat suspected credentials or tokens in output; identify only their location or that a secret-like value was detected.
- Do not claim Jira facts, links, counts, or audience safety have been verified against Jira unless that verification actually occurred.
- Do not silently omit, rewrite, or classify ambiguous customer-sensitive content as safe.
- Do not report `PASS` when a required check failed or could not be performed.
