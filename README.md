# jira-confluence-automation
Jira/Confluence automation toolkit built with AI assistance

## Weekly report prototype

The React and Node.js prototype lives in `apps/web` and `apps/api`. It is a
local-only starting point; Jira integration and report generation are not
implemented yet.

### Run locally

Install dependencies from the repository root:

```sh
npm install
```

Start the API and frontend in separate terminals:

```sh
npm run dev:api
npm run dev:web
```

Open the frontend at <http://127.0.0.1:5173>. Its API health indicator checks
the backend at <http://127.0.0.1:3001/api/health>.

The API binds only to `127.0.0.1`. Do not persist Jira personal access tokens
in files, browser storage, or logs; future Jira requests should submit the
token only for the active generation request.
