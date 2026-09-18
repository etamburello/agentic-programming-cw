"""
Analyze the leading digits of 1!, 2!, ..., n!
and compare the distribution to Benford's Law.

Usage: python benford_factorial.py 1000000

log10(n!) = sum_{k=1..n} log10(k). The integer part of that sum only
shifts the decimal point, so it can be discarded. A running fractional
part in [0, 1) is enough to recover the first digit of each k!, and
k! itself is never constructed.
"""

import math
import sys


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


def count_factorial_leading_digits(n):
    """
    Count leading digits of 1! through n!.
    Keep only the fractional part of the running log10 sum.
    """
    counts = {digit: 0 for digit in range(1, 10)}
    log10_frac = 0.0

    for k in range(1, n + 1):
        log10_frac += math.log10(k)
        log10_frac -= math.floor(log10_frac)
        counts[leading_digit_from_log10(log10_frac)] += 1

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
        raise ValueError("usage: python benford_factorial.py <positive integer n>")

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

    counts = count_factorial_leading_digits(n)
    print_report(n, counts)


if __name__ == "__main__":
    main()
