# Automated Unit Testing and Coverage Execution

Run the project's existing unit tests and, when requested or configured, report measured coverage.

## Input Format

Accept a request containing any available subset of:
- Test file paths, test names, or a feature/change scope.
- A requested coverage target or threshold.
- A preferred test or coverage command.

Use the repository's test configuration and dependency manifests when the request omits details.

## Processing Steps

1. Inspect the relevant test files and project test configuration to identify the established runner and coverage setup.
2. Select the smallest existing test command that covers the requested scope. Use the configured coverage command if coverage was requested or the project defines one.
3. Execute the tests and coverage measurement; capture the actual command, exit status, test counts, failures, and coverage figures reported by the tools.
4. Compare coverage to a threshold only when the user or project configuration specifies one.
5. Report test failures, missing tools, and environment errors explicitly. Do not treat an interrupted or failed run as a pass.

## Output Format

Return a concise Markdown report with:
- **Scope** — tests or files covered.
- **Commands** — exact commands executed.
- **Results** — pass/fail and test counts, if reported.
- **Coverage** — measured percentage and covered/missed counts when available; otherwise state why it was not measured.
- **Failures or notes** — relevant failures, environment blockers, or an explicit “None”.

## Constraints

- Do not claim tests or coverage were run unless the corresponding command completed and its output supports the claim.
- Do not invent coverage percentages, thresholds, test counts, or results.
- Do not broaden a targeted run into the full suite unless the scoped tests reveal a reason or the user requests it.
- Do not change application code, tests, dependencies, or configuration as part of execution unless the user asks for fixes.
- Do not install dependencies merely to get a green result; report missing tooling or dependencies.
- Preserve existing test and coverage conventions, and avoid leaving unnecessary generated artifacts.
