"""
Analyze the leading digits of the first n Fibonacci numbers
and compare the distribution to Benford's Law.

Usage: python benford_fibonacci.py 1000

The first digit of x is recovered from log10(x) = k + f, where k is an
integer and 0 <= f < 1. Then x = 10^k * 10^f with 10^f in [1, 10), so
the leading digit is floor(10^f). For F_i (i >= a few terms) this uses
Binet's formula, log10(F_i) ≈ i*log10(φ) - log10(√5), and never builds
the full integer.
"""

import math
import sys

# log10(φ) and log10(√5) for Binet: F_i ≈ φ^i / √5
LOG10_PHI = math.log10((1 + math.sqrt(5)) / 2)
LOG10_SQRT5 = 0.5 * math.log10(5)

# Binet is not close enough for a correct leading digit until after these.
BINET_SAFE_AFTER = 10


def benford_percent(digit):
    """Return Benford's Law probability of `digit` as a percentage."""
    return math.log10(1 + 1 / digit) * 100


def leading_digit_from_log10(log10_x):
    """
    If log10(x) = k + f with 0 <= f < 1, then x = 10^k * 10^f.
    10^k only places the decimal point; 10^f in [1, 10) is the significand.
    The first digit is floor(10^f).

    A tiny epsilon counters cases where 10^f lands just below an integer
    (for example 7.999... instead of 8) because log10 is irrational.
    """
    fraction = log10_x - math.floor(log10_x)
    significand = 10 ** fraction
    digit = int(significand + 1e-12)
    if digit < 1 or digit > 9:
        return 1
    return digit


def leading_digit_small(value):
    """First digit of a small positive integer, with no string conversion."""
    while value >= 10:
        value //= 10
    return value


def count_fibonacci_leading_digits(n):
    """
    Count leading digits of F_1, F_2, ..., F_n.
    Early terms are walked with two small integers. After that only logs
    of the index are stored — never F_n itself.
    """
    counts = {digit: 0 for digit in range(1, 10)}

    direct = min(n, BINET_SAFE_AFTER)
    prev, curr = 1, 1
    for _ in range(direct):
        counts[leading_digit_small(prev)] += 1
        prev, curr = curr, prev + curr

    for index in range(direct + 1, n + 1):
        log10_f = index * LOG10_PHI - LOG10_SQRT5
        counts[leading_digit_from_log10(log10_f)] += 1

    return counts


def print_report(n, counts):
    """Print leading-digit counts against Benford's Law percentages."""
    header = f"{'Digit':<10} {'Count':<10} {'Observed':<13} {'Benford':<12} {'Difference'}"
    print(header)
    print("-" * len(header))

    for digit in range(1, 10):
        count = counts[digit]
        observed = (count / n) * 100
        benford = benford_percent(digit)
        difference = round(observed - benford, 2)
        if difference == 0:
            difference = 0.0
        print(
            f"{digit:<10} {count:<10} {observed:>6.2f}%      "
            f"{benford:>6.2f}%     {difference:>7.2f}%"
        )


def parse_n(argv):
    if len(argv) != 2:
        raise ValueError("usage: python benford_fibonacci.py <positive integer n>")

    try:
        n = int(argv[1])
    except ValueError as exc:
        raise ValueError("n must be a positive integer") from exc

    if n <= 0:
        raise ValueError("n must be a positive integer")

    return n


def main():
    try:
        n = parse_n(sys.argv)
    except ValueError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    counts = count_fibonacci_leading_digits(n)
    print_report(n, counts)


if __name__ == "__main__":
    main()
