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

The API binds only to `127.0.0.1`. It serves a clearly labeled synthetic
dataset at `GET /api/report-data`; the health endpoint identifies this as
`local-fixture` mode. Jira integration is disabled, and the prototype does not
connect to Jira or use live project data.

### Run with Podman Compose

The compose setup runs only the web and API services; the prototype does not
need a database. Build and start both services with:

```sh
podman compose up --build
```

Open <http://127.0.0.1:5173>. The frontend is published on loopback only; the
API is reachable by the frontend inside the Compose network and is not
published to the host. Use `podman compose down` to stop the services.
