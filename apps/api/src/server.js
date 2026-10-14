import express from "express";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const app = express();
const port = parsePort(process.env.PORT);
const host = process.env.HOST ?? "127.0.0.1";
const fixturePath = new URL("./data/demo-report.json", import.meta.url);
const reportData = JSON.parse(await readFile(fixturePath, "utf8"));

app.disable("x-powered-by");
app.get("/api/health", (_request, response) => {
  response.json({
    status: "ok",
    dataSource: "local-fixture",
    jiraIntegration: "disabled",
  });
});

app.get("/api/report-data", (_request, response) => {
  response.json(reportData);
});

export { app, parsePort };

const isDirectRun =
  process.argv[1] &&
  import.meta.url === pathToFileURL(resolve(process.argv[1])).href;

if (isDirectRun) {
  app.listen(port, host, () => {
    console.log(`API listening at http://${host}:${port}`);
  });
}

function parsePort(value) {
  if (value === undefined) {
    return 3001;
  }

  if (!/^\d+$/.test(value)) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }

  const parsedPort = Number(value);
  if (!Number.isInteger(parsedPort) || parsedPort < 1 || parsedPort > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }

  return parsedPort;
}
