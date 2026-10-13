"""Tests for filtering and normalizing Jira issue payloads."""

import json

import pytest

from tools.normalize_issues import main, normalize_payload


def test_normalize_payload_keeps_stories_bugs_and_tasks_and_excludes_subtasks():
    result = normalize_payload(
        {
            "issues": [
                {
                    "key": "APP-1",
                    "fields": {
                        "summary": "  Ship search  ",
                        "issuetype": {"name": "Story", "subtask": False},
                        "status": {"name": " In Progress "},
                        "assignee": {"displayName": " Ada Lovelace "},
                        "created": "2026-10-01T10:00:00.000+0000",
                        "resolutiondate": None,
                        "labels": [" search ", "", None],
                    },
                },
                {"key": "APP-2", "fields": {"issuetype": {"name": "Bug"}}},
                {"key": "APP-3", "issuetype": {"name": "Task"}},
                {"key": "APP-4", "fields": {"issuetype": {"name": "Task", "subtask": True}}},
                {"key": "APP-5", "fields": {"issuetype": {"name": "Sub-task"}}},
                {"key": "APP-6", "fields": {"issuetype": {"name": "Epic"}}},
            ]
        }
    )

    assert [issue["key"] for issue in result["issues"]] == ["APP-1", "APP-2", "APP-3"]
    assert result["issues"][0] == {
        "key": "APP-1",
        "summary": "Ship search",
        "issue_type": "Story",
        "status": "In Progress",
        "assignee": "Ada Lovelace",
        "created": "2026-10-01T10:00:00.000+0000",
        "updated": None,
        "resolved": None,
        "priority": None,
        "project": None,
        "labels": ["search"],
    }
    assert result["metrics"] == {
        "input_count": 6,
        "included_count": 3,
        "filtered_subtask_count": 2,
        "filtered_other_type_count": 1,
        "issue_type_counts": {"Bug": 1, "Story": 1, "Task": 1},
        "status_counts": {"In Progress": 1, "Unspecified": 2},
    }


def test_normalize_payload_supports_empty_issue_list():
    result = normalize_payload({"issues": []})

    assert result == {
        "issues": [],
        "metrics": {
            "input_count": 0,
            "included_count": 0,
            "filtered_subtask_count": 0,
            "filtered_other_type_count": 0,
            "issue_type_counts": {},
            "status_counts": {},
        },
    }


@pytest.mark.parametrize(
    "payload",
    [
        {"issues": [None]},
        {"issues": [{"fields": []}]},
        {"issues": [{"fields": {"issuetype": {"name": "Task"}, "labels": "wrong"}}]},
        {"items": "not a list"},
    ],
)
def test_normalize_payload_rejects_invalid_input(payload):
    with pytest.raises(ValueError):
        normalize_payload(payload)


def test_main_reads_payload_and_writes_normalized_json(tmp_path, monkeypatch):
    source = tmp_path / "issues.json"
    destination = tmp_path / "normalized.json"
    source.write_text(
        json.dumps([{"key": "APP-7", "summary": "Add export", "issuetype": {"name": "Task"}}]),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "normalize_issues.py",
            "--input-file",
            str(source),
            "--output-file",
            str(destination),
        ],
    )

    main()

    result = json.loads(destination.read_text(encoding="utf-8"))
    assert result["issues"][0]["key"] == "APP-7"
    assert result["metrics"]["included_count"] == 1
