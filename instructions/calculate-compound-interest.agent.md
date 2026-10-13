# Calculating Compound Interest

Use this workflow when the user asks to calculate compound interest from a principal, annual interest rate, compounding frequency, and investment duration.

## Run the Calculator

- Invoke `tools/compound_interest.py` with four positional arguments, in this order: principal, annual rate as a percentage, compounds per year, and total years.
- Use the project's Python interpreter when available. For example:

  ```sh
  python tools/compound_interest.py 1000 5 12 10
  ```

- Pass the annual rate as a percentage number: use `5` for 5%, not `0.05`.
- Principal, annual rate, and years must be non-negative numbers. Compounds per year must be a positive integer.
- If any required input is missing or ambiguous, ask the user for it. Do not guess financial inputs.
- If the command reports invalid input, explain which input needs correction; do not present calculated results.

## Present Results

- Report both values printed by the script: **Final amount** and **Interest earned**.
- Preserve the script's two-decimal precision and labels.
- State the inputs used, including the annual rate as a percentage and the compounding frequency, so the calculation is clear.
- Do not assume or add a currency symbol; use one only if the user specified the currency.
- Keep the result concise and do not imply financial advice.
