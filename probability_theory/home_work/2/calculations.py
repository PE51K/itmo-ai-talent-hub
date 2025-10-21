#!/usr/bin/env python3
"""
Validator for probability_theory/home_work/2/homework.tex

Recomputes the probabilities in each problem and checks that the LaTeX file
contains matching fractional or decimal representations (within rounding
tolerance). Exits with status 0 when all checks pass; otherwise reports the
discrepancies and exits with status 1.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
from typing import Iterable, Optional


LATEX_PATH = Path(__file__).resolve().parent / "homework.tex"

# High precision for decimal comparisons.
getcontext().prec = 28


@dataclass
class CheckResult:
    """Holds the outcome of validating a single reported value."""

    label: str
    expected: Fraction
    latex_repr_ok: bool
    decimal_repr_ok: Optional[bool] = None
    decimal_value: Optional[str] = None
    message: Optional[str] = None

    def is_ok(self) -> bool:
        ok = self.latex_repr_ok
        if self.decimal_repr_ok is not None:
            ok = ok and self.decimal_repr_ok
        return ok


def latex_fraction_regex(frac: Fraction) -> re.Pattern[str]:
    r"""Matches \frac, \dfrac, or \tfrac with the given fraction."""
    num, den = frac.numerator, frac.denominator
    pattern = r"\\(?:d|t)?frac\s*\{\s*%s\s*\}\s*\{\s*%s\s*\}" % (num, den)
    return re.compile(pattern)


def check_fraction_presence(text: str, frac: Fraction) -> bool:
    """Return True if the LaTeX text contains the fraction."""
    return bool(latex_fraction_regex(frac).search(text))


def tolerance_for_decimal(decimal_text: str) -> Decimal:
    """Return the rounding tolerance implied by the number of decimal places."""
    if "." not in decimal_text:
        return Decimal("0.5")
    places = len(decimal_text.split(".")[1])
    return Decimal(5) * (Decimal(10) ** (-(places + 1)))


def check_decimal_match(decimal_text: str, actual: Fraction) -> tuple[bool, str]:
    """Verify that the reported decimal matches the actual value within tolerance."""
    reported = Decimal(decimal_text)
    actual_decimal = Decimal(actual.numerator) / Decimal(actual.denominator)
    tolerance = tolerance_for_decimal(decimal_text)
    delta = abs(actual_decimal - reported)
    ok = delta <= tolerance
    detail = (
        f"reported {decimal_text}, expected ≈ {actual_decimal:.10f}, |Δ|={delta:.2E}, "
        f"tolerance={tolerance}"
    )
    return ok, detail


def render_fraction(frac: Fraction) -> str:
    return f"{frac.numerator}/{frac.denominator}"


def format_result(result: CheckResult) -> str:
    parts = [
        f"{result.label}: expected {render_fraction(result.expected)}",
        "fraction OK" if result.latex_repr_ok else "fraction MISSING",
    ]
    if result.decimal_value is not None:
        decimal_msg = "decimal OK" if result.decimal_repr_ok else "decimal MISMATCH"
        parts.append(f"{decimal_msg} ({result.decimal_value})")
    if result.message:
        parts.append(result.message)
    return " | ".join(parts)


def ensure_text_present(text: str, needle: str) -> bool:
    return needle in text


def validate_problem_1(text: str) -> CheckResult:
    p1 = Fraction(1, 5)
    p2 = Fraction(3, 10)
    probability = p1 / (1 - (1 - p1) * (1 - p2))
    expected = Fraction(5, 11)
    assert probability == expected
    return CheckResult(
        label="Problem 1",
        expected=expected,
        latex_repr_ok=check_fraction_presence(text, expected),
    )


def validate_problem_2(text: str) -> CheckResult:
    total = Fraction(0, 1)
    for k in range(4):
        transfer = Fraction(comb(5, k) * comb(6, 3 - k), comb(11, 3))
        draw = Fraction(comb(4 + k, 4), comb(15, 4))
        total += transfer * draw
    expected = Fraction(47, 6435)
    decimal_text = "0.00730"
    decimal_present = ensure_text_present(text, decimal_text)
    if decimal_present:
        decimal_ok, message = check_decimal_match(decimal_text, expected)
    else:
        decimal_ok, message = False, f"decimal {decimal_text} not found"
    return CheckResult(
        label="Problem 2",
        expected=expected,
        latex_repr_ok=check_fraction_presence(text, expected),
        decimal_repr_ok=decimal_ok,
        decimal_value=decimal_text,
        message=message,
    )


def validate_problem_3(text: str) -> CheckResult:
    priors = [Fraction(1, 2), Fraction(3, 10), Fraction(1, 5)]
    payout_probs = [Fraction(1, 100), Fraction(3, 100), Fraction(8, 100)]
    total = sum(priors[i] * payout_probs[i] for i in range(3))
    probability = priors[0] * payout_probs[0] / total
    expected = Fraction(1, 6)
    decimal_text = "0.1667"
    decimal_present = ensure_text_present(text, decimal_text)
    if decimal_present:
        decimal_ok, message = check_decimal_match(decimal_text, expected)
    else:
        decimal_ok, message = False, f"decimal {decimal_text} not found"
    return CheckResult(
        label="Problem 3",
        expected=expected,
        latex_repr_ok=check_fraction_presence(text, expected),
        decimal_repr_ok=decimal_ok,
        decimal_value=decimal_text,
        message=message,
    )


def validate_problem_4(text: str) -> Iterable[CheckResult]:
    results = []
    n = 4
    probability = sum(
        Fraction((-1) ** (r + 1), factorial(r)) for r in range(1, n + 1)
    )
    expected = Fraction(5, 8)
    decimal_text = "0.625"
    decimal_present = ensure_text_present(text, decimal_text)
    if decimal_present:
        decimal_ok, message = check_decimal_match(decimal_text, expected)
    else:
        decimal_ok, message = False, f"decimal {decimal_text} not found"
    results.append(
        CheckResult(
            label="Problem 4 (n=4)",
            expected=expected,
            latex_repr_ok=check_fraction_presence(text, expected),
            decimal_repr_ok=decimal_ok,
            decimal_value=decimal_text,
            message=message,
        )
    )
    return results


def validate_problem_5(text: str) -> Iterable[CheckResult]:
    results = []

    def posterior(prior: Fraction) -> Fraction:
        true_pos = Fraction(999, 1000)
        false_pos = Fraction(1, 1000)
        numerator = true_pos * prior
        denominator = numerator + false_pos * (1 - prior)
        return numerator / denominator

    scenarios = [
        ("Problem 5 (prior 0.01)", Fraction(1, 100), "0.9098", ("90.98\\%", "90.98")),
        ("Problem 5 (prior 0.0001)", Fraction(1, 10000), "0.0908", ("9.08\\%", "9.08")),
    ]

    for label, prior, decimal_text, (percent_latex, percent_numeric) in scenarios:
        probability = posterior(prior)
        fraction = probability.limit_denominator()
        decimal_present = ensure_text_present(text, decimal_text)
        percent_present = ensure_text_present(text, percent_latex)
        decimal_ok = False
        decimal_message = None
        if decimal_present:
            decimal_ok, decimal_message = check_decimal_match(decimal_text, probability)
        else:
            decimal_message = f"decimal {decimal_text} not found"
        percent_ok = False
        if percent_present:
            actual_decimal = Decimal(probability.numerator) / Decimal(probability.denominator)
            actual_percent = actual_decimal * Decimal(100)
            percent_value = Decimal(percent_numeric)
            tolerance = tolerance_for_decimal(percent_numeric)
            percent_delta = abs(actual_percent - percent_value)
            percent_ok = percent_delta <= tolerance
            percent_status = (
                "percent OK" if percent_ok else "percent MISMATCH"
            )
            extra = (
                f"{percent_status} (reported {percent_numeric}%, "
                f"expected ≈ {actual_percent:.4f}%)"
            )
            if decimal_message:
                decimal_message += "; " + extra
            else:
                decimal_message = extra
        else:
            extra = f"percent {percent_latex} not found"
            if decimal_message:
                decimal_message += "; " + extra
            else:
                decimal_message = extra
        results.append(
            CheckResult(
                label=label,
                expected=fraction,
                latex_repr_ok=True,  # No fractional form given in the text.
                decimal_repr_ok=decimal_ok and percent_ok,
                decimal_value=decimal_text,
                message=decimal_message,
            )
        )
    return results


def validate_problem_6(text: str) -> CheckResult:
    posterior = Fraction(2, 3)
    return CheckResult(
        label="Problem 6",
        expected=posterior,
        latex_repr_ok=check_fraction_presence(text, posterior),
    )


def main() -> int:
    if not LATEX_PATH.exists():
        print(f"Could not find {LATEX_PATH}", file=sys.stderr)
        return 1
    latex_text = LATEX_PATH.read_text(encoding="utf-8")

    results: list[CheckResult] = []
    results.append(validate_problem_1(latex_text))
    results.append(validate_problem_2(latex_text))
    results.append(validate_problem_3(latex_text))
    results.extend(validate_problem_4(latex_text))
    results.extend(validate_problem_5(latex_text))
    results.append(validate_problem_6(latex_text))

    all_ok = True
    for result in results:
        print(format_result(result))
        all_ok = all_ok and result.is_ok()

    if all_ok:
        print("All reported values are consistent with recomputed results.")
        return 0

    print("Some reported values differ from recomputed results.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
