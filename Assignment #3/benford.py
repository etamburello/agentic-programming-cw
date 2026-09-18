"""
Leading-digit analysis of Fibonacci numbers, powers of two, and factorials
compared with Benford's Law.

After the table, a grouped bar chart of observed vs Benford percentages
is printed in the terminal and saved as HTML (opened in the browser).

If log10(x) = k + f with 0 <= f < 1, then x = 10^k * 10^f and the first
digit is floor(10^f). Sequences yield those log10 values without building
the integers. Counting, Benford percentages, and printing are shared.
"""

import html
import math
import sys
import webbrowser
from pathlib import Path

USAGE = "usage: python benford.py {fibonacci|power2|factorial|primes} <positive integer n>"

# ---------------------------------------------------------------------------
# Sequence-specific computation
# Each generator yields log10 of the first n terms, never the terms themselves.
# ---------------------------------------------------------------------------

LOG10_PHI = math.log10((1 + math.sqrt(5)) / 2)
LOG10_SQRT5 = 0.5 * math.log10(5)
LOG10_2 = math.log10(2)
BINET_SAFE_AFTER = 10


def fibonacci_log10(n):
    """log10(F_1), ..., log10(F_n). Small terms are exact; later terms use Binet."""
    direct = min(n, BINET_SAFE_AFTER)
    prev, curr = 1, 1
    for _ in range(direct):
        yield math.log10(prev)
        prev, curr = curr, prev + curr

    for index in range(direct + 1, n + 1):
        yield index * LOG10_PHI - LOG10_SQRT5


def power2_log10(n):
    """log10(2^0), ..., log10(2^{n-1})."""
    for exponent in range(n):
        yield exponent * LOG10_2


def factorial_log10(n):
    """
    log10(1!), ..., log10(n!).

    log10(k!) = sum_{i=1..k} log10(i). Only the fractional part is kept,
    because the integer part does not affect the leading digit.
    """
    log10_frac = 0.0
    for k in range(1, n + 1):
        log10_frac += math.log10(k)
        log10_frac -= math.floor(log10_frac)
        yield log10_frac


def nth_prime_upper_bound(n):
    """A known upper bound on the nth prime, used as a sieve limit."""
    if n < 6:
        return 15
    return int(n * (math.log(n) + math.log(math.log(n)))) + 3


def first_n_primes(n):
    """First n primes via the sieve of Eratosthenes."""
    limit = nth_prime_upper_bound(n)
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)

    primes = [i for i, flag in enumerate(is_prime) if flag]
    if len(primes) < n:
        raise RuntimeError(f"sieve bound {limit} found only {len(primes)} primes")
    return primes[:n]


def primes_log10(n):
    """log10 of the first n primes. The nth prime is ~ n ln n, so these stay small."""
    for prime in first_n_primes(n):
        yield math.log10(prime)


SEQUENCES = {
    "fibonacci": fibonacci_log10,
    "power2": power2_log10,
    "factorial": factorial_log10,
    "primes": primes_log10,
}


# ---------------------------------------------------------------------------
# Benford analysis
# ---------------------------------------------------------------------------

def leading_digit_from_log10(log10_x):
    """First digit of x given log10(x) = k + f. 10^f in [1, 10) is the significand."""
    fraction = log10_x - math.floor(log10_x)
    significand = 10 ** fraction
    digit = int(significand + 1e-12)
    if digit < 1 or digit > 9:
        return 1
    return digit


def benford_percent(digit):
    """Benford's Law probability of `digit`, as a percentage."""
    return math.log10(1 + 1 / digit) * 100


def count_leading_digits(log10_values):
    """Tally first digits 1-9 from a stream of log10 values."""
    counts = {digit: 0 for digit in range(1, 10)}
    total = 0
    for log10_x in log10_values:
        counts[leading_digit_from_log10(log10_x)] += 1
        total += 1
    return counts, total


def compare_to_benford(counts, n):
    """
    Build one result row per digit: count, observed %, Benford %, difference.
    """
    rows = []
    for digit in range(1, 10):
        count = counts[digit]
        observed = (count / n) * 100
        predicted = benford_percent(digit)
        difference = round(observed - predicted, 2)
        if difference == 0:
            difference = 0.0
        rows.append((digit, count, observed, predicted, difference))
    return rows


# ---------------------------------------------------------------------------
# Result presentation
# ---------------------------------------------------------------------------

SEQUENCE_TITLES = {
    "fibonacci": "Fibonacci numbers",
    "power2": "Powers of 2",
    "factorial": "Factorials",
    "primes": "Prime numbers",
}

BAR_SCALE = 1.0  # terminal bar characters per percentage point
CHART_Y_MAX = 35.0  # HTML chart y-axis upper bound (%)


def print_report(rows):
    header = f"{'Digit':<10} {'Count':<10} {'Observed':<13} {'Benford':<12} {'Difference'}"
    print(header)
    print("-" * len(header))
    for digit, count, observed, predicted, difference in rows:
        print(
            f"{digit:<10} {count:<10} {observed:>6.2f}%      "
            f"{predicted:>6.2f}%     {difference:>7.2f}%"
        )


def _bar(percent):
    width = max(0, round(percent * BAR_SCALE))
    return "#" * width


def print_bar_chart(rows):
    """Grouped horizontal bars: observed vs Benford, one pair per digit."""
    print()
    print("Observed vs Benford's Law")
    print("-" * 52)
    for digit, _count, observed, predicted, _difference in rows:
        print(f"{digit:<6} obs     {_bar(observed):<32} {observed:6.2f}%")
        print(f"{'':<6} Benford {_bar(predicted):<32} {predicted:6.2f}%")
        print()


def write_bar_chart_html(rows, sequence, n, path):
    """Write a grouped vertical bar chart comparing observed and Benford %."""
    title = f"{SEQUENCE_TITLES[sequence]} (n = {n:,})"
    width, height = 840, 480
    left, right, top, bottom = 56, 24, 56, 56
    plot_w = width - left - right
    plot_h = height - top - bottom
    group_w = plot_w / 9
    bar_w = group_w * 0.32

    def y_px(percent):
        return top + plot_h * (1 - percent / CHART_Y_MAX)

    grid = []
    for tick in (0, 10, 20, 30):
        y = y_px(tick)
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" '
            f'stroke="#e2e2e2"/>'
            f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" '
            f'font-size="12" fill="#555">{tick}</text>'
        )

    bars = []
    labels = []
    for i, (digit, _count, observed, predicted, _difference) in enumerate(rows):
        gx = left + i * group_w
        x_obs = gx + group_w * 0.18
        x_ben = gx + group_w * 0.50
        y_obs = y_px(observed)
        y_ben = y_px(predicted)
        bars.append(
            f'<rect x="{x_obs:.1f}" y="{y_obs:.1f}" width="{bar_w:.1f}" '
            f'height="{plot_h - (y_obs - top):.1f}" fill="#2c6eac" rx="2"/>'
            f'<rect x="{x_ben:.1f}" y="{y_ben:.1f}" width="{bar_w:.1f}" '
            f'height="{plot_h - (y_ben - top):.1f}" fill="#c47b2b" rx="2"/>'
        )
        labels.append(
            f'<text x="{gx + group_w / 2:.1f}" y="{height - 28}" '
            f'text-anchor="middle" font-size="13" fill="#222">{digit}</text>'
        )

    path.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Benford — {html.escape(title)}</title>
  <style>
    body {{ font-family: Georgia, serif; margin: 32px; color: #222; background: #fafafa; }}
    h1 {{ font-size: 22px; font-weight: normal; margin-bottom: 8px; }}
    .caption {{ color: #555; margin-bottom: 20px; }}
    .legend span {{ display: inline-block; width: 14px; height: 14px;
      margin: 0 6px 0 16px; vertical-align: -2px; }}
    svg {{ background: #fff; border: 1px solid #ddd; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p class="caption">
    Leading-digit percentages
    <span class="legend">
      <span style="background:#2c6eac"></span> Observed
      <span style="background:#c47b2b"></span> Benford's Law
    </span>
  </p>
  <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
       viewBox="0 0 {width} {height}">
    {''.join(grid)}
    {''.join(bars)}
    {''.join(labels)}
    <text x="{left + plot_w / 2}" y="{height - 8}" text-anchor="middle"
          font-size="13" fill="#333">Digit</text>
    <text x="16" y="{top + plot_h / 2}" text-anchor="middle" font-size="13"
          fill="#333" transform="rotate(-90 16 {top + plot_h / 2})">Percent</text>
  </svg>
</body>
</html>
""",
        encoding="utf-8",
    )


def show_bar_chart(rows, sequence, n):
    """Print a terminal bar chart and open a grouped HTML bar chart."""
    print_bar_chart(rows)
    chart_path = Path(__file__).resolve().parent / f"benford_{sequence}_{n}.html"
    write_bar_chart_html(rows, sequence, n, chart_path)
    print(f"Bar chart written to {chart_path}")
    webbrowser.open(chart_path.resolve().as_uri())


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

def parse_args(argv):
    if len(argv) != 3:
        raise ValueError(USAGE)

    name = argv[1].lower()
    if name not in SEQUENCES:
        choices = ", ".join(SEQUENCES)
        raise ValueError(f"unknown sequence {argv[1]!r}; choose from: {choices}")

    try:
        n = int(argv[2])
    except ValueError as exc:
        raise ValueError("n must be a positive integer") from exc

    if n <= 0:
        raise ValueError("n must be a positive integer")

    return name, n


def main():
    try:
        name, n = parse_args(sys.argv)
    except ValueError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    counts, total = count_leading_digits(SEQUENCES[name](n))
    rows = compare_to_benford(counts, total)
    print_report(rows)
    show_bar_chart(rows, name, n)


if __name__ == "__main__":
    main()
