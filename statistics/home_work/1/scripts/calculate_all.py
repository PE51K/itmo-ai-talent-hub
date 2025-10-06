#!/usr/bin/env python3
"""Calculate all formulas for statistics homework 1."""

import math
from fractions import Fraction


def binomial(n, k):
    """Calculate binomial coefficient C(n,k) = n!/(k!(n-k)!)"""
    if k > n or k < 0:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def problem_1():
    """Problem 1: Probability of two best teams in different groups."""
    prob = Fraction(8, 15)
    decimal = 8 / 15
    print("Problem 1:")
    print(f"  Probability = {prob} = {decimal:.4f}")
    return prob, decimal


def problem_2():
    """Problem 2: Hypergeometric probability."""
    # P(X >= 2) = P(X=2) + P(X=3)
    # P(X=2) = C(8,2)*C(12,1) / C(20,3)
    # P(X=3) = C(8,3)*C(12,0) / C(20,3)
    
    numerator_2 = binomial(8, 2) * binomial(12, 1)
    numerator_3 = binomial(8, 3) * binomial(12, 0)
    denominator = binomial(20, 3)
    
    total_numerator = numerator_2 + numerator_3
    prob = Fraction(total_numerator, denominator)
    decimal = total_numerator / denominator
    
    print("\nProblem 2:")
    print(f"  C(8,2) = {binomial(8, 2)}")
    print(f"  C(12,1) = {binomial(12, 1)}")
    print(f"  C(8,3) = {binomial(8, 3)}")
    print(f"  C(12,0) = {binomial(12, 0)}")
    print(f"  C(20,3) = {denominator}")
    print(f"  Numerator = {binomial(8, 2)}*{binomial(12, 1)} + {binomial(8, 3)}*{binomial(12, 0)} = {numerator_2} + {numerator_3} = {total_numerator}")
    print(f"  Probability = {total_numerator}/{denominator} = {prob} ≈ {decimal:.4f}")
    return prob, decimal


def problem_3():
    """Problem 3: Number of chess matchings with white/black distinction."""
    # 20! / 10!
    result = math.factorial(20) // math.factorial(10)
    print("\nProblem 3:")
    print(f"  20! / 10! = {result:,}")
    return result


def problem_4():
    """Problem 4: Probability of point in inscribed square."""
    prob = 2 / math.pi
    print("\nProblem 4:")
    print(f"  Probability = 2/π ≈ {prob:.4f}")
    return prob


def problem_5():
    """Problem 5: Train compartment probabilities."""
    total = binomial(36, 7)
    
    # a) Two compartments (3 and 4 passengers)
    prob_a_numerator = binomial(9, 2) * 2 * binomial(4, 4) * binomial(4, 3)
    prob_a = prob_a_numerator / total
    
    # b) Seven compartments (1 passenger each)
    prob_b_numerator = binomial(9, 7) * (4 ** 7)
    prob_b = prob_b_numerator / total
    
    # c) Three compartments
    # Patterns: 4-2-1, 3-3-1, 3-2-2
    ways_421 = 6 * binomial(4, 4) * binomial(4, 2) * binomial(4, 1)
    ways_331 = 3 * binomial(4, 3) * binomial(4, 3) * binomial(4, 1)
    ways_322 = 3 * binomial(4, 3) * binomial(4, 2) * binomial(4, 2)
    ways_total = ways_421 + ways_331 + ways_322
    
    prob_c_numerator = binomial(9, 3) * ways_total
    prob_c = prob_c_numerator / total
    
    print("\nProblem 5:")
    print(f"  C(36,7) = {total:,}")
    print(f"\n  a) Two compartments:")
    print(f"     C(9,2) * 8 = {binomial(9, 2)} * 8 = {binomial(9, 2) * 8}")
    print(f"     Probability = {prob_a_numerator}/{total} ≈ {prob_a:.6f}")
    print(f"\n  b) Seven compartments:")
    print(f"     C(9,7) * 4^7 = {binomial(9, 7)} * {4**7} = {prob_b_numerator:,}")
    print(f"     Probability = {prob_b_numerator}/{total} ≈ {prob_b:.6f}")
    print(f"\n  c) Three compartments:")
    print(f"     Pattern 4-2-1: 6 * C(4,4) * C(4,2) * C(4,1) = 6 * 1 * 6 * 4 = {ways_421}")
    print(f"     Pattern 3-3-1: 3 * C(4,3) * C(4,3) * C(4,1) = 3 * 4 * 4 * 4 = {ways_331}")
    print(f"     Pattern 3-2-2: 3 * C(4,3) * C(4,2) * C(4,2) = 3 * 4 * 6 * 6 = {ways_322}")
    print(f"     Total ways = {ways_421} + {ways_331} + {ways_322} = {ways_total}")
    print(f"     C(9,3) * {ways_total} = {binomial(9, 3)} * {ways_total} = {prob_c_numerator}")
    print(f"     Probability = {prob_c_numerator}/{total} ≈ {prob_c:.6f}")
    
    return (prob_a, prob_b, prob_c)


def problem_6():
    """Problem 6: Bayesian probability for second gold plot."""
    # Prior probabilities
    p_r1 = Fraction(1, 2)
    p_r2 = Fraction(1, 2)
    
    # Likelihoods
    p_success_r1 = Fraction(3, 4)
    p_success_r2 = Fraction(1, 2)
    
    # Posterior probabilities after first success
    p_r1_given_success = (p_r1 * p_success_r1) / (p_r1 * p_success_r1 + p_r2 * p_success_r2)
    p_r2_given_success = (p_r2 * p_success_r2) / (p_r1 * p_success_r1 + p_r2 * p_success_r2)
    
    # Probability of second success (without replacement)
    p_second_r1 = Fraction(2, 3)
    p_second_r2 = Fraction(1, 3)
    
    p_second_success = p_r1_given_success * p_second_r1 + p_r2_given_success * p_second_r2
    decimal = float(p_second_success)
    
    print("\nProblem 6:")
    print(f"  P(R1|success) = {p_r1_given_success}")
    print(f"  P(R2|success) = {p_r2_given_success}")
    print(f"  P(second success|first success) = {p_r1_given_success} * {p_second_r1} + {p_r2_given_success} * {p_second_r2}")
    print(f"  P(second success|first success) = {p_second_success} ≈ {decimal:.4f}")
    return p_second_success, decimal


def main():
    """Run all calculations."""
    print("=" * 60)
    print("Statistics Homework 1 - Calculations")
    print("=" * 60)
    
    problem_1()
    problem_2()
    problem_3()
    problem_4()
    problem_5()
    problem_6()
    
    print("\n" + "=" * 60)
    print("All calculations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()