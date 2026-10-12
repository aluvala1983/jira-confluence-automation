"""Small helpers to fetch report data and render a markdown status report."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from data_fetcher import fetch_json
from formatting import normalize_report, render_markdown


def build_report(data: Any) -> str:
    """Normalize a payload and convert it into Markdown output."""
    return render_markdown(normalize_report(data))


def generate_report(url: str, *, output_path: str = "reports/weekly-status-report.md", timeout: int = 10, headers: Mapping[str, str] | None = None, params: Mapping[str, Any] | None = None) -> str:
    """Fetch JSON from a URL, render a report, and save it to disk."""
    payload = fetch_json(url, timeout=timeout, headers=headers, params=params)
    markdown = build_report(payload)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(markdown, encoding="utf-8")
    return str(destination)


if __name__ == "__main__":
    sample = {
        "project": "Aurora Customer Portal",
        "team": "Delivery Team",
        "week_start": "2026-10-05",
        "issues": [
            {"key": "PORT-101", "summary": "Account recovery improvements", "status": "Done"},
            {"key": "PORT-102", "summary": "Billing validation", "status": "In Progress"},
        ],
    }
    print(build_report(sample))
