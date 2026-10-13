"""Calculate sprint velocity from completed story point values in JSON."""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def calculate_velocity(payload: Any) -> dict[str, Any]:
    """Sum a list of non-negative completed story point values."""
    if isinstance(payload, list):
        values = payload
    elif isinstance(payload, Mapping) and isinstance(payload.get("story_points"), list):
        values = payload["story_points"]
    else:
        raise ValueError(
            "Input JSON must be a list of story point values or an object "
            "containing a 'story_points' list."
        )

    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Story point value at index {index} must be a number.")
        if not math.isfinite(value) or value < 0:
            raise ValueError(
                f"Story point value at index {index} must be finite and non-negative."
            )

    velocity = sum(values)
    if not math.isfinite(velocity):
        raise ValueError("The sum of story point values is too large to calculate.")

    return {
        "velocity": velocity,
        "issue_count": len(values),
        "story_points": values,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate sprint velocity by summing completed story point values "
            "from a JSON file."
        )
    )
    parser.add_argument("--input-file", required=True, help="JSON story point values file")
    parser.add_argument("--output-file", required=True, help="JSON output path")
    args = parser.parse_args()

    try:
        with Path(args.input_file).open(encoding="utf-8") as input_file:
            payload = json.load(input_file)
        result = calculate_velocity(payload)
        Path(args.output_file).write_text(
            json.dumps(result, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
