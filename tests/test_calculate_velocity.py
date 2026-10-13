"""Tests for calculating sprint velocity."""

import json

import pytest

from tools.calculate_velocity import calculate_velocity, main


@pytest.mark.parametrize("payload", [[3, 5, 8], {"story_points": [3, 5, 8]}])
def test_calculate_velocity_sums_story_point_values(payload):
    result = calculate_velocity(payload)

    assert result == {"velocity": 16, "issue_count": 3, "story_points": [3, 5, 8]}


def test_calculate_velocity_accepts_empty_and_fractional_values():
    assert calculate_velocity({"story_points": []}) == {
        "velocity": 0,
        "issue_count": 0,
        "story_points": [],
    }
    assert calculate_velocity([1.5, 2.5])["velocity"] == 4.0


@pytest.mark.parametrize(
    "payload",
    [
        {"story_points": "5"},
        {"story_points": [1, "2"]},
        {"story_points": [True]},
        {"story_points": [-1]},
        {"story_points": [float("inf")]},
    ],
)
def test_calculate_velocity_rejects_invalid_values(payload):
    with pytest.raises(ValueError):
        calculate_velocity(payload)


def test_main_reads_json_and_writes_velocity(tmp_path, monkeypatch):
    source = tmp_path / "points.json"
    destination = tmp_path / "velocity.json"
    source.write_text(json.dumps({"story_points": [2, 3, 5]}), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "calculate_velocity.py",
            "--input-file",
            str(source),
            "--output-file",
            str(destination),
        ],
    )

    main()

    assert json.loads(destination.read_text(encoding="utf-8"))["velocity"] == 10
