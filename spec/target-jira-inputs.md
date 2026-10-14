# Target Jira Input Register

**Purpose:** Record the non-secret target-instance and project inputs required by Task T001 in [tasks.md](./tasks.md).  
**Status:** Inputs provided; target compatibility verification remains pending.  
**Last checked:** 2026-10-14

This register contains no credentials. Do not place a Jira personal access token, password, cookie, or other secret here. Values marked **VERIFY** were provided by the operator but have not been independently checked against the target instance. The Jira URL is environment-specific; do not commit this register if the URL is considered internal.

| Input | Recorded value | Status / evidence |
|---|---|---|
| Jira deployment type | Jira Server | **VERIFY** - provided by operator; see the version compatibility note below. |
| Jira base URL | `https://jiraeu.epam.com` | **VERIFY** - provided by operator; HTTPS URL, not independently contacted or validated. |
| Jira Data Center/Server version | `10.3.26` | **VERIFY** - provided by operator as the exact About Jira version. The reported Server deployment and 10.3.26 version appear inconsistent and require confirmation before implementation relies on them. |
| Project key | `EPM-INBL` | **VERIFY** - provided by operator as the single project in scope; not checked against Jira. |
| Project timezone (IANA) | `Asia/Kolkata` | **VERIFY** - provided by operator; not checked against the Jira project settings. |
| Authentication method | Personal access token using the instance's documented bearer-token mechanism | Operator confirmed this is verified for the target instance. No token is recorded; the verification procedure/evidence has not been added here. |
| Issue type mapping | Story → Story; Bug → Bug; Task → Task | **VERIFY** - operator confirmed these exact names. Subtasks and unrelated issue types remain excluded; exact subtask label was not supplied. |
| Done statuses | `Done`; `done` | **VERIFY** - operator confirmed these are two distinct Jira statuses. |
| Blocker signals | Status = `blocked` | **VERIFY** - operator supplied this exact status; no Jira flag signal was specified. |
| Planning source | Next future sprint | **VERIFY** - operator selected this single source; sprint fields and access have not been checked against Jira. |

## Verification Notes

- The prototype targets Jira Data Center/Server REST API v2 and uses read-only access; operator-provided inputs do not establish API compatibility or permission to read required data.
- Confirm the deployment/version combination from the instance's About Jira page. Do not claim live compatibility until the deployment type/version, API/authentication behavior, TLS certificate chain, required read permissions, and configured fields are verified.
- Verify that the actual Jira project settings use timezone `Asia/Kolkata`, the exact issue types and done statuses listed above, the `blocked` status, and the selected future-sprint planning source.
- The response `Story EPMINBL-32277` was treated as an example issue key, not a project key or additional issue type; the operator subsequently confirmed the exact issue type names as Story, Bug, and Task.
- Keep any environment-specific values local if publishing them would disclose internal infrastructure. Never commit credentials or secret-bearing files.
- Until the verification items above are complete, use fixtures for development and do not claim that target compatibility or the complete live configuration has been verified.
