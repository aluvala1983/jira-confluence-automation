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
