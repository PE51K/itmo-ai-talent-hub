"""Numerically verify the solutions in homework.tex for Homework 2."""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial


def _assert_equal(value: Fraction, expected: Fraction, label: str) -> None:
    """Raise if value and expected differ; keeps the script honest."""
    if value != expected:
        raise AssertionError(f"{label}: expected {expected}, got {value}")


def _format_fraction(frac: Fraction) -> str:
    """Format a Fraction as numerator/denominator."""
    return f"{frac.numerator}/{frac.denominator}"


def problem_1() -> Fraction:
    """Shooter 1 vs Shooter 2 alternating shots until the first hit."""
    p1 = Fraction(1, 5)
    p2 = Fraction(3, 10)
    result = p1 / (1 - (1 - p1) * (1 - p2))
    expected = Fraction(5, 11)
    _assert_equal(result, expected, "Problem 1")
    print("Problem 1:")
    print(f"  P(shooter 1 fires more) = {result} ≈ {float(result):.6f}")
    return result


def problem_2() -> Fraction:
    """Urn transfer followed by drawing four white balls."""
    total = Fraction(0, 1)
    print("\nProblem 2:")
    for k in range(4):
        moved = Fraction(comb(5, k) * comb(6, 3 - k), comb(11, 3))
        draw = Fraction(comb(4 + k, 4), comb(15, 4))
        contribution = moved * draw
        total += contribution
        print(
            f"  k={k}: P(move)={_format_fraction(moved)}, "
            f"P(draw|k)={_format_fraction(draw)}, "
            f"contribution={_format_fraction(contribution)}"
        )
    expected = Fraction(47, 6435)
    _assert_equal(total, expected, "Problem 2")
    print(f"  Total probability = {total} ≈ {float(total):.6f}")
    return total


def problem_3() -> Fraction:
    """Posterior probability of a low-risk policyholder given a payout."""
    priors = {
        "low": Fraction(1, 2),
        "medium": Fraction(3, 10),
        "high": Fraction(1, 5),
    }
    claim_probs = {
        "low": Fraction(1, 100),
        "medium": Fraction(3, 100),
        "high": Fraction(8, 100),
    }
    numerator = claim_probs["low"] * priors["low"]
    denominator = sum(claim_probs[risk] * priors[risk] for risk in priors)
    result = numerator / denominator
    expected = Fraction(1, 6)
    _assert_equal(result, expected, "Problem 3")
    print("\nProblem 3:")
    print(f"  P(low | payout) = {result} ≈ {float(result):.6f}")
    return result


def derangements(n: int) -> int:
    """Count derangements via the standard recursion."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    d_prev2, d_prev1 = 1, 0  # D_0, D_1
    for k in range(2, n + 1):
        d_prev2, d_prev1 = d_prev1, (k - 1) * (d_prev1 + d_prev2)
    return d_prev1


def problem_4(n: int = 4) -> Fraction:
    """Probability at least one visitor receives the correct hat."""
    inclusion_sum = sum(Fraction((-1) ** k, factorial(k)) for k in range(n + 1))
    prob = Fraction(1, 1) - inclusion_sum
    derangement_term = Fraction(derangements(n), factorial(n))
    expected = Fraction(5, 8)
    _assert_equal(prob, expected, "Problem 4")
    print("\nProblem 4:")
    print(
        "  Inclusion-Exclusion: "
        f"1 - Σ (-1)^k/k! = {prob} ≈ {float(prob):.6f}"
    )
    print(
        f"  Derangements: D_{n} = {derangements(n)}, "
        f"so 1 - D_n/n! = {Fraction(1, 1) - derangement_term}"
    )
    return prob


def posterior_positive(prior: Fraction) -> Fraction:
    """Posterior probability of disease given a positive test."""
    true_positive = Fraction(999, 1000)
    false_positive = Fraction(1, 1000)
    numerator = true_positive * prior
    denominator = numerator + false_positive * (1 - prior)
    return numerator / denominator


def problem_5() -> tuple[Fraction, Fraction]:
    """Posterior probabilities for two prevalence scenarios."""
    scenarios = {
        Fraction(1, 100): Fraction(999, 1098),
        Fraction(1, 10000): Fraction(999, 10998),
    }
    results = []
    print("\nProblem 5:")
    for prior, expected in scenarios.items():
        posterior = posterior_positive(prior)
        _assert_equal(posterior, expected, f"Problem 5 (prior={prior})")
        print(
            f"  Prior={_format_fraction(prior)} → "
            f"P(disease|+)={posterior} ≈ {float(posterior):.6f}"
        )
        results.append(posterior)
    return tuple(results)


def problem_6() -> Fraction:
    """Two baskets; compute P(white on second draw | first white)."""
    p_b1 = Fraction(1, 2)
    p_b2 = Fraction(1, 2)
    p_white_given_b1 = Fraction(1, 1)
    p_white_given_b2 = Fraction(1, 2)

    denominator = p_white_given_b1 * p_b1 + p_white_given_b2 * p_b2
    p_b1_given_white = p_white_given_b1 * p_b1 / denominator
    result = p_b1_given_white * Fraction(1, 1)  # second draw white if B1
    expected = Fraction(2, 3)
    _assert_equal(result, expected, "Problem 6")
    print("\nProblem 6:")
    print(f"  P(B1 | first white) = {p_b1_given_white} ≈ {float(p_b1_given_white):.6f}")
    print(f"  P(second white | first white) = {result} ≈ {float(result):.6f}")
    return result


def main() -> None:
    """Run all problem checks."""
    print("=" * 60)
    print("Probability Theory Homework 2 - Calculations")
    print("=" * 60)

    problem_1()
    problem_2()
    problem_3()
    problem_4()
    problem_5()
    problem_6()

    print("\n" + "=" * 60)
    print("All calculations verified successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
