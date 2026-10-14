import assert from "node:assert/strict";
import { once } from "node:events";
import test, { after, before } from "node:test";
import { app, parsePort } from "../src/server.js";

let server;
let baseUrl;

before(async () => {
  server = app.listen(0, "127.0.0.1");
  await once(server, "listening");
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  await new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
});

test("health reports that Jira is disabled and local fixture data is active", async () => {
  const response = await fetch(`${baseUrl}/api/health`);

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), {
    status: "ok",
    dataSource: "local-fixture",
    jiraIntegration: "disabled",
  });
});

test("report data comes from the synthetic local fixture", async () => {
  const response = await fetch(`${baseUrl}/api/report-data`);
  const report = await response.json();

  assert.equal(response.status, 200);
  assert.equal(report.source, "local-fixture");
  assert.equal(report.synthetic, true);
  assert.equal(report.project.key, "DEMO");
  assert.ok(report.issues.length > 0);
  assert.ok(report.issues.every((issue) => issue.key.startsWith("DEMO-")));
});

test("PORT must be a valid TCP port", () => {
  assert.equal(parsePort(undefined), 3001);
  assert.equal(parsePort("5174"), 5174);
  assert.throws(() => parsePort(""), /PORT must be an integer/);
  assert.throws(() => parsePort("0"), /PORT must be an integer/);
  assert.throws(() => parsePort("65536"), /PORT must be an integer/);
  assert.throws(() => parsePort("not-a-port"), /PORT must be an integer/);
});
