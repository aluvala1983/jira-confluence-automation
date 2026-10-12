"""Tests for the local report generation utilities."""

from datetime import date

from reporting_service import build_demo_snapshot, calculate_reporting_window, validate_config


def test_calculate_reporting_window_returns_previous_monday_sunday():
    start, end = calculate_reporting_window(date(2026, 10, 12), timezone_name="UTC")

    assert start.isoformat() == "2026-10-05"
    assert end.isoformat() == "2026-10-11"


def test_validate_config_requires_core_settings():
    errors = validate_config({"base_url": "", "project_key": "", "timezone": ""})

    assert any("Base URL" in error for error in errors)
    assert any("Project Key" in error for error in errors)
    assert any("Timezone" in error for error in errors)


def test_build_demo_snapshot_has_expected_sections():
    config = {
        "base_url": "https://jira.example.com",
        "project_key": "PROJ",
        "timezone": "UTC",
        "done_statuses": "Done, Closed",
    }

    snapshot = build_demo_snapshot(config, date(2026, 10, 5), date(2026, 10, 11))

    assert snapshot["project"] == "PROJ"
    assert snapshot["completed_count"] >= 1
    assert snapshot["remaining_open_count"] >= 1
    assert "summary" in snapshot
