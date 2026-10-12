"""Minimal local Flask app for generating weekly Jira status drafts."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from reporting_service import build_demo_snapshot, calculate_reporting_window, render_markdown, validate_config

app = Flask(__name__)
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

DEFAULT_CONFIG = {
    "base_url": "https://jira.example.com",
    "project_key": "PROJ",
    "timezone": "UTC",
    "issue_type_mapping": "Story, Bug, Task",
    "done_statuses": "Done, Closed",
    "blocked_signals": "Blocked, Flagged",
    "planning_source": "Next sprint",
    "health": "Amber",
}


@app.get("/")
def index():
    context = {
        "config": DEFAULT_CONFIG,
        "errors": [],
        "preview": "",
        "leadership_preview": "",
        "saved_report": "",
    }
    return render_template("index.html", **context)


@app.post("/generate")
def generate_report():
    config = {key: request.form.get(key, "") for key in DEFAULT_CONFIG}
    errors = validate_config(config)
    if errors:
        return render_template("index.html", config=config, errors=errors, preview="", leadership_preview="", saved_report="")

    period_start, period_end = calculate_reporting_window(timezone_name=config["timezone"])
    snapshot = build_demo_snapshot(config, period_start, period_end)
    customer_preview = render_markdown(snapshot, audience="customer")
    leadership_preview = render_markdown(snapshot, audience="leadership")

    return render_template(
        "index.html",
        config=config,
        errors=[],
        preview=customer_preview,
        leadership_preview=leadership_preview,
        saved_report="",
        reporting_start=period_start.isoformat(),
        reporting_end=period_end.isoformat(),
    )


@app.post("/save")
def save_report():
    config = {key: request.form.get(key, "") for key in DEFAULT_CONFIG}
    audience = request.form.get("audience", "customer")
    report_text = request.form.get("report_text", "")

    if not report_text.strip():
        return redirect(url_for("index"))

    now = request.form.get("report_date") or "2026-10-12"
    filename = f"weekly-status-{now}-{audience}.md"
    candidate = REPORTS_DIR / filename
    counter = 1
    while candidate.exists():
        candidate = REPORTS_DIR / f"weekly-status-{now}-{audience}-{counter}.md"
        counter += 1

    candidate.write_text(report_text, encoding="utf-8")
    return render_template(
        "index.html",
        config=config,
        errors=[],
        preview=report_text,
        leadership_preview="",
        saved_report=f"Saved report to {candidate}",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
