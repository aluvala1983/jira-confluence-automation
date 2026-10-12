"""Tests for the report-fetching and formatting helpers."""

from __future__ import annotations

from formatting import normalize_issue, render_markdown
from report_generator import build_report


def test_normalize_issue_cleans_values():
    issue = {"key": "  ABC-1 ", "summary": "  Fix billing issue  ", "status": " Done ", "assignee": "  Ada "}

    normalized = normalize_issue(issue)

    assert normalized["key"] == "ABC-1"
    assert normalized["summary"] == "Fix billing issue"
    assert normalized["status"] == "Done"
    assert normalized["assignee"] == "Ada"


def test_render_markdown_contains_required_sections():
    report = {
        "project": "Aurora",
        "team": "Platform",
        "week_start": "2026-10-05",
        "issues": [{"key": "AUR-7", "summary": "Improve dashboards", "status": "Done"}],
    }

    markdown = render_markdown(report)

    assert "# Weekly Engineering Status Report" in markdown
    assert "## Accomplishments" in markdown
    assert "## Blockers" in markdown
    assert "## Next Week's Plan" in markdown
    assert "Improve dashboards (AUR-7)" in markdown


def test_build_report_handles_plain_issue_list():
    payload = [{"key": "AUR-8", "summary": "Customer portal refresh", "status": "Done"}]

    markdown = build_report(payload)

    assert "Customer portal refresh (AUR-8)" in markdown
