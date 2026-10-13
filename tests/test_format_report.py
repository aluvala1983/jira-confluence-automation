"""Tests for the Jira Markdown report command."""

import json

from tools.format_report import _load_issues, format_report, main


def test_format_report_groups_completed_upcoming_and_blocked_issues(tmp_path):
    issues = [
        {
            "key": "APP-1",
            "fields": {
                "summary": "Ship search",
                "status": {
                    "name": "Closed",
                    "statusCategory": {"key": "done", "name": "Done"},
                },
            },
        },
        {"key": "APP-2", "summary": "Improve filters", "status": "In Progress"},
        {"key": "APP-3", "summary": "Resolve dependency", "status": "Blocked"},
    ]
    source = tmp_path / "issues.json"
    source.write_text(json.dumps({"issues": issues}), encoding="utf-8")

    report = format_report(_load_issues(source))

    assert "- Processed 3 Jira issue(s): 1 completed, 2 remaining." in report
    assert "## Completed Work\n- **APP-1**: Ship search (Closed)" in report
    assert "## Upcoming Plans\n- Carry forward these non-completed issues:" in report
    assert "- **APP-2**: Improve filters (In Progress)" in report
    assert "## Blockers\n- **APP-3**: Resolve dependency (Blocked)" in report


def test_load_issues_accepts_jira_response_and_empty_list(tmp_path):
    source = tmp_path / "issues.json"
    source.write_text(json.dumps({"issues": []}), encoding="utf-8")

    assert _load_issues(source) == []


def test_main_reads_json_and_writes_markdown(tmp_path, monkeypatch):
    source = tmp_path / "issues.json"
    destination = tmp_path / "report.md"
    source.write_text(
        json.dumps([{"key": "APP-7", "summary": "Document release", "status": "Done"}]),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        ["format_report.py", "--input-file", str(source), "--output-file", str(destination)],
    )

    main()

    assert "Document release" in destination.read_text(encoding="utf-8")
