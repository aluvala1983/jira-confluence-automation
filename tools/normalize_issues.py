"""Filter and normalize Jira issues from JSON into a metrics-ready data model."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


_INCLUDED_ISSUE_TYPES = {"story": "Story", "bug": "Bug", "task": "Task"}
_SUBTASK_TYPE_NAMES = {"sub-task", "subtask"}


@dataclass(frozen=True)
class NormalizedIssue:
    """Stable fields retained from Jira for downstream reporting."""

    key: str | None
    summary: str | None
    issue_type: str
    status: str | None
    assignee: str | None
    created: str | None
    updated: str | None
    resolved: str | None
    priority: str | None
    project: str | None
    labels: list[str]


def _text(value: Any) -> str | None:
    """Extract a concise display value from Jira scalars and name objects."""
    if isinstance(value, Mapping):
        value = value.get("displayName", value.get("name", value.get("value", value.get("key"))))
    if value is None:
        return None
    normalized = re.sub(r"\s+", " ", str(value)).strip()
    return normalized or None


def _issue_fields(issue: Mapping[str, Any], index: int) -> Mapping[str, Any]:
    fields = issue.get("fields", {})
    if not isinstance(fields, Mapping):
        raise ValueError(f"Issue at index {index} has invalid 'fields'; expected an object.")
    return fields


def normalize_payload(payload: Any) -> dict[str, Any]:
    """Filter to stories, bugs, and tasks, returning normalized records and counts."""
    if isinstance(payload, list):
        raw_issues = payload
    elif isinstance(payload, Mapping) and isinstance(payload.get("issues"), list):
        raw_issues = payload["issues"]
    elif isinstance(payload, Mapping) and isinstance(payload.get("items"), list):
        raw_issues = payload["items"]
    else:
        raise ValueError("Input JSON must be an issue list or an object containing an 'issues' list.")

    normalized: list[NormalizedIssue] = []
    filtered_subtasks = 0
    filtered_other_types = 0

    for index, raw_issue in enumerate(raw_issues):
        if not isinstance(raw_issue, Mapping):
            raise ValueError(f"Issue at index {index} must be a JSON object.")

        fields = _issue_fields(raw_issue, index)
        issue_type = fields.get("issuetype", raw_issue.get("issuetype", raw_issue.get("issue_type")))
        if not isinstance(issue_type, Mapping):
            issue_type = {"name": issue_type}

        type_name = _text(issue_type.get("name")) or ""
        normalized_type_name = type_name.casefold()
        is_subtask = issue_type.get("subtask") is True or normalized_type_name in _SUBTASK_TYPE_NAMES
        if is_subtask:
            filtered_subtasks += 1
            continue

        issue_type_label = _INCLUDED_ISSUE_TYPES.get(normalized_type_name)
        if issue_type_label is None:
            filtered_other_types += 1
            continue

        status = fields.get("status", raw_issue.get("status"))
        project = fields.get("project", raw_issue.get("project"))
        priority = fields.get("priority", raw_issue.get("priority"))
        labels = fields.get("labels", raw_issue.get("labels", []))
        if labels is None:
            labels = []
        if not isinstance(labels, list):
            raise ValueError(f"Issue at index {index} has invalid 'labels'; expected a list.")

        normalized.append(
            NormalizedIssue(
                key=_text(raw_issue.get("key", raw_issue.get("id"))),
                summary=_text(fields.get("summary", raw_issue.get("summary"))),
                issue_type=issue_type_label,
                status=_text(status),
                assignee=_text(fields.get("assignee", raw_issue.get("assignee"))),
                created=_text(fields.get("created", raw_issue.get("created"))),
                updated=_text(fields.get("updated", raw_issue.get("updated"))),
                resolved=_text(fields.get("resolutiondate", raw_issue.get("resolved"))),
                priority=_text(priority),
                project=_text(project),
                labels=[label for value in labels if (label := _text(value)) is not None],
            )
        )

    type_counts = Counter(issue.issue_type for issue in normalized)
    status_counts = Counter(issue.status or "Unspecified" for issue in normalized)
    return {
        "issues": [asdict(issue) for issue in normalized],
        "metrics": {
            "input_count": len(raw_issues),
            "included_count": len(normalized),
            "filtered_subtask_count": filtered_subtasks,
            "filtered_other_type_count": filtered_other_types,
            "issue_type_counts": dict(sorted(type_counts.items())),
            "status_counts": dict(sorted(status_counts.items())),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filter and normalize Jira issues from a JSON file."
    )
    parser.add_argument("--input-file", required=True, help="JSON file containing Jira issues")
    parser.add_argument("--output-file", required=True, help="JSON output path")
    args = parser.parse_args()

    try:
        with Path(args.input_file).open(encoding="utf-8") as input_file:
            payload = json.load(input_file)
        result = normalize_payload(payload)
        Path(args.output_file).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
