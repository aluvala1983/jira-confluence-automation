import express from "express";

const app = express();
const port = Number(process.env.PORT ?? 3001);
const host = process.env.HOST ?? "127.0.0.1";

app.disable("x-powered-by");
app.get("/api/health", (_request, response) => {
  response.json({ status: "ok" });
});

app.listen(port, host, () => {
  console.log(`API listening at http://${host}:${port}`);
});
