"""Format Jira issues from JSON into a Markdown status report."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any


_DONE_STATUSES = {"closed", "complete", "completed", "done", "resolved"}
_BLOCKED_STATUSES = {"blocked", "impeded", "on hold"}


def _field_text(value: Any, default: str) -> str:
    """Extract readable text from scalar values or Jira name objects."""
    if isinstance(value, Mapping):
        value = value.get("name", value.get("value", value.get("key")))
    if value is None:
        return default
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or default


def _markdown_text(value: str) -> str:
    """Escape Markdown punctuation in text originating from issue data."""
    return re.sub(r"([\\`*_{}\[\]()<>!|])", r"\\\1", value)


def _normalize_issue(issue: Mapping[str, Any], index: int) -> dict[str, str]:
    """Normalize Jira REST API issues and simple flattened issue objects."""
    fields = issue.get("fields", {})
    if not isinstance(fields, Mapping):
        raise ValueError(f"Issue at index {index} has invalid 'fields'; expected an object.")

    summary = fields.get("summary", issue.get("summary", issue.get("title")))
    status = fields.get("status", issue.get("status", issue.get("state")))
    category = status.get("statusCategory", {}) if isinstance(status, Mapping) else {}
    if not isinstance(category, Mapping):
        category = {}

    status_name = _field_text(status, "Unknown")
    category_key = _field_text(category.get("key"), "").casefold()
    category_name = _field_text(category.get("name"), "").casefold()
    return {
        "key": _field_text(issue.get("key", issue.get("id")), f"Issue {index + 1}"),
        "summary": _field_text(summary, "Summary unavailable"),
        "status": status_name,
        "status_key": category_key or status_name.casefold(),
        "status_category": category_name,
    }


def _load_issues(input_path: Path) -> list[dict[str, str]]:
    """Load and normalize an issue list or a Jira REST API response."""
    with input_path.open(encoding="utf-8") as input_file:
        payload = json.load(input_file)

    if isinstance(payload, list):
        issues = payload
    elif isinstance(payload, Mapping) and isinstance(payload.get("issues"), list):
        issues = payload["issues"]
    elif isinstance(payload, Mapping) and isinstance(payload.get("items"), list):
        issues = payload["items"]
    else:
        raise ValueError("Input JSON must be an issue list or an object containing an 'issues' list.")

    normalized = []
    for index, issue in enumerate(issues):
        if not isinstance(issue, Mapping):
            raise ValueError(f"Issue at index {index} must be a JSON object.")
        normalized.append(_normalize_issue(issue, index))
    return normalized


def _is_completed(issue: Mapping[str, str]) -> bool:
    """Identify completed issues from Jira status categories or common statuses."""
    return issue["status_key"] == "done" or issue["status_category"] == "done" or (
        issue["status_key"] in _DONE_STATUSES
    )


def _is_blocked(issue: Mapping[str, str]) -> bool:
    """Identify blocked issues by their Jira status or status category."""
    return issue["status_key"] in _BLOCKED_STATUSES or issue["status_category"] in _BLOCKED_STATUSES


def format_report(issues: list[dict[str, str]]) -> str:
    """Render a compact Jira status report in Markdown."""
    completed = [issue for issue in issues if _is_completed(issue)]
    upcoming = [issue for issue in issues if not _is_completed(issue)]
    blockers = [issue for issue in upcoming if _is_blocked(issue)]

    if issues:
        executive_summary = (
            f"Processed {len(issues)} Jira issue(s): {len(completed)} completed, "
            f"{len(upcoming)} remaining."
        )
    else:
        executive_summary = "No Jira issues were provided."

    def issue_bullets(items: list[dict[str, str]]) -> list[str]:
        return [
            f"- **{_markdown_text(issue['key'])}**: {_markdown_text(issue['summary'])} "
            f"({_markdown_text(issue['status'])})"
            for issue in items
        ]

    lines = [
        "# Jira Status Report",
        "",
        "## Executive Summary",
        f"- {executive_summary}",
        "",
        "## Completed Work",
        *(issue_bullets(completed) or ["- None reported."]),
        "",
        "## Upcoming Plans",
        "- Carry forward these non-completed issues:",
        *(issue_bullets(upcoming) or ["- None reported."]),
        "",
        "## Blockers",
        *(issue_bullets(blockers) or ["- None reported."]),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format Jira issues from a JSON file as a Markdown status report."
    )
    parser.add_argument("--input-file", required=True, help="JSON file containing Jira issues")
    parser.add_argument("--output-file", required=True, help="Markdown report output path")
    args = parser.parse_args()

    try:
        issues = _load_issues(Path(args.input_file))
        report = format_report(issues)
        Path(args.output_file).write_text(report, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
