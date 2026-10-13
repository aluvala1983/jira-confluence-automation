"""Calculate compound interest from command-line inputs."""

import argparse
import math


def non_negative_float(value: str) -> float:
    """Parse a finite, non-negative number."""
    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a number") from error
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite, non-negative number")
    return number


def positive_int(value: str) -> int:
    """Parse a positive integer."""
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate compound interest. Enter the annual rate as a "
            "percentage (for example, 5 for 5%)."
        )
    )
    parser.add_argument("principal", type=non_negative_float, help="initial amount")
    parser.add_argument(
        "annual_rate", type=non_negative_float, help="annual interest rate in percent"
    )
    parser.add_argument(
        "compounds_per_year",
        type=positive_int,
        help="number of compounding periods per year",
    )
    parser.add_argument(
        "years", type=non_negative_float, help="total investment duration in years"
    )
    args = parser.parse_args()

    rate_per_period = args.annual_rate / 100 / args.compounds_per_year
    periods = args.compounds_per_year * args.years
    final_amount = args.principal * (1 + rate_per_period) ** periods
    interest_earned = final_amount - args.principal

    print(f"Final amount: {final_amount:.2f}")
    print(f"Interest earned: {interest_earned:.2f}")


if __name__ == "__main__":
    main()
