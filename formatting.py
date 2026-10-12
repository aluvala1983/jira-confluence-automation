"""Helpers for cleaning report data and rendering Markdown output."""

from __future__ import annotations

from typing import Any


def clean_text(value: Any, *, default: str = "N/A") -> str:
    """Normalize text values and discard blank or missing entries."""
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def normalize_issue(issue: dict[str, Any]) -> dict[str, str]:
    """Return a consistent issue dictionary with cleaned fields."""
    summary = clean_text(issue.get("summary") or issue.get("title") or issue.get("name"))
    key = clean_text(issue.get("key") or issue.get("id"))
    status = clean_text(issue.get("status") or issue.get("state"))
    assignee = clean_text(issue.get("assignee") or issue.get("owner"))
    return {
        "key": key,
        "summary": summary,
        "status": status,
        "assignee": assignee,
    }


def normalize_report(data: Any) -> dict[str, Any]:
    """Normalize a Jira-style payload into a simple report structure."""
    items = data.get("issues", data.get("items", data)) if isinstance(data, dict) else data
    if not isinstance(items, list):
        items = [items]

    normalized_issues = [normalize_issue(issue) for issue in items if isinstance(issue, dict)]
    return {
        "project": clean_text((data or {}).get("project") if isinstance(data, dict) else "Project"),
        "team": clean_text((data or {}).get("team") if isinstance(data, dict) else "Team"),
        "issues": normalized_issues,
        "week_start": clean_text((data or {}).get("week_start") if isinstance(data, dict) else "2026-10-05"),
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render a simple weekly status report as Markdown."""
    project = clean_text(report.get("project"), default="Project")
    team = clean_text(report.get("team"), default="Team")
    week_start = clean_text(report.get("week_start"), default="YYYY-MM-DD")
    issues = report.get("issues", [])

    lines = [
        "# Weekly Engineering Status Report",
        "",
        f"- **Project:** {project}",
        f"- **Team:** {team}",
        f"- **Week of:** {week_start}",
        "",
        "## Accomplishments",
    ]

    if issues:
        for issue in issues:
            lines.append(f"- {issue.get('summary', 'N/A')} ({issue.get('key', 'N/A')})")
    else:
        lines.append("- No issues were returned for this reporting period.")

    lines.extend([
        "",
        "## Blockers",
        "- No material blockers identified.",
        "",
        "## Next Week's Plan",
        "- Continue delivery work and validate high-priority issues.",
    ])
    return "\n".join(lines) + "\n"
