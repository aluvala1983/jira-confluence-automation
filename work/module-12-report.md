# Module 12 Completion Report

## Instruction File
- Filename: `instructions/use-calculate-velocity.agent.md`

```markdown
# Calculating Sprint Velocity

Use `tools/calculate_velocity.py` when explicitly asked to calculate sprint velocity from supplied completed story point values. The script sums values from local JSON; it does not connect to Jira, select completed issues, or verify sprint scope.

## Input and Command

- Accept a JSON array of numeric story-point values or an object with a `story_points` array.
- Provide completed issue story points only. The script does not filter incomplete work or infer completion from Jira issue records.
- Run from the repository root:

  ```bash
  python tools/calculate_velocity.py --input-file path/to/story-points.json --output-file path/to/velocity.json
  ```

- Both command-line arguments are required. Use paths supplied or approved by the user. The output file is overwritten if it already exists; check the destination and confirm before replacing it.
- Values must be finite, non-negative JSON numbers. Booleans and numeric strings are invalid. An empty list produces zero velocity.

## Output and Interpretation

- The output JSON contains `velocity` (the sum), `issue_count` (the number of provided values), and `story_points` (the supplied values).
- This is a single-sprint total, not an average across sprints or a forecast.
- Do not claim the values were fetched from Jira, are complete, or are comparable across teams unless that was independently verified.
- If the command fails or data is invalid, report the error and do not claim the output was generated successfully.
```

## Script File
- Filename: `tools/calculate_velocity.py`
- Language: Python

```python
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
```

## Script Execution Output
```
usage: calculate_velocity.py [-h] --input-file INPUT_FILE --output-file
                             OUTPUT_FILE

Calculate sprint velocity by summing completed story point values from a JSON
file.

options:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        JSON story point values file
  --output-file OUTPUT_FILE
                        JSON output path
```
