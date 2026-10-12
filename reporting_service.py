"""Utilities for reporting period calculations and local report generation."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


def calculate_reporting_window(reference_date: date | None = None, timezone_name: str = "UTC") -> tuple[date, date]:
    """Return the previous Monday-Sunday reporting period for the supplied date."""
    tz = ZoneInfo(timezone_name) if timezone_name else ZoneInfo("UTC")
    current_day = reference_date or datetime.now(tz).date()
    current_monday = current_day - timedelta(days=current_day.weekday())
    previous_monday = current_monday - timedelta(days=7)
    previous_sunday = previous_monday + timedelta(days=6)
    return previous_monday, previous_sunday


def validate_config(config: dict[str, str]) -> list[str]:
    """Return validation errors for missing or unusable configuration."""
    errors: list[str] = []
    labels = {
        "base_url": "Base URL",
        "project_key": "Project Key",
        "timezone": "Timezone",
    }
    for field in ("base_url", "project_key", "timezone"):
        if not config.get(field, "").strip():
            errors.append(f"{labels[field]} is required.")
    if config.get("base_url", "").strip() and not config["base_url"].startswith(("http://", "https://")):
        errors.append("Base URL must start with http:// or https://")
    try:
        ZoneInfo(config["timezone"]) if config.get("timezone") else None
    except Exception:
        errors.append("Timezone must be a valid IANA timezone name, such as UTC or America/New_York.")
    return errors


def build_demo_snapshot(config: dict[str, str], period_start: date, period_end: date) -> dict[str, object]:
    """Create a consistent in-memory snapshot for local preview and testing."""
    done_statuses = [status.strip() for status in config.get("done_statuses", "Done, Closed").split(",") if status.strip()]
    if not done_statuses:
        done_statuses = ["Done", "Closed"]

    sample_issues = [
        {"key": "PORT-101", "summary": "Account recovery improvements", "status": "Done"},
        {"key": "PORT-102", "summary": "Billing validation", "status": "In Progress"},
        {"key": "PORT-103", "summary": "Customer notification updates", "status": "Blocked"},
        {"key": "PORT-104", "summary": "Single sign-on setup", "status": "Done"},
    ]

    completed = [issue for issue in sample_issues if issue["status"] in done_statuses]
    remaining = [issue for issue in sample_issues if issue["status"] not in done_statuses]
    blockers = [issue for issue in sample_issues if issue["status"] == "Blocked"]

    return {
        "project": config.get("project_key", "UNKNOWN"),
        "base_url": config.get("base_url", "https://jira.example.com"),
        "timezone": config.get("timezone", "UTC"),
        "reporting_start": period_start.isoformat(),
        "reporting_end": period_end.isoformat(),
        "completed_count": len(completed),
        "remaining_open_count": len(remaining),
        "next_week_count": 3,
        "completed_issues": completed,
        "remaining_issues": remaining,
        "blockers": blockers,
        "health": "Amber",
        "summary": "Delivery is stable with one dependency awaiting customer confirmation.",
    }


def render_markdown(report: dict[str, object], audience: str = "customer") -> str:
    """Render a simple Markdown draft for the selected audience."""
    project = str(report.get("project", "Project"))
    start = str(report.get("reporting_start", "YYYY-MM-DD"))
    end = str(report.get("reporting_end", "YYYY-MM-DD"))
    summary = str(report.get("summary", "Delivery is progressing as planned."))
    completed_count = int(report.get("completed_count", 0))
    remaining_count = int(report.get("remaining_open_count", 0))
    next_week_count = int(report.get("next_week_count", 0))
    health = str(report.get("health", "Green"))

    lines = [
        "# Weekly Project Status Report",
        "",
        f"- **Audience:** {audience.title()}",
        f"- **Project:** {project}",
        f"- **Reporting period:** {start} to {end}",
        "",
        "## Overall Delivery Health",
        "",
        f"**Status:** {health}",
        f"**Rationale:** {summary}",
        "",
        "## Executive Summary",
        summary,
        "",
        "## Completed This Week",
        f"**Issues completed:** {completed_count}",
    ]

    completed_issues = report.get("completed_issues", [])
    if isinstance(completed_issues, list) and completed_issues:
        for issue in completed_issues:
            keys = issue.get("key", "N/A") if isinstance(issue, dict) else "N/A"
            summary_value = issue.get("summary", "N/A") if isinstance(issue, dict) else "N/A"
            lines.append(f"- {summary_value} ({keys})")
    else:
        lines.append("- No issues were completed during this period.")

    lines.extend([
        "",
        "## Remaining Open Work",
        f"**Open issues:** {remaining_count}",
        "- Material work remains focused on the highest-priority delivery items.",
        "",
        "## Next Week's Plan",
        f"**Planned issues:** {next_week_count}",
        "- Continue delivery work and complete the next priority items for the customer-facing milestone.",
        "",
        "## Blockers and Risks",
        "- No material blockers or risks to report.",
        "",
        "## Decisions or Support Needed",
        "- None this week.",
    ])
    return "\n".join(lines) + "\n"
