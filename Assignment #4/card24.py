"""
Card Game 24.

Deal four cards from a 52-card deck. The player enters an arithmetic
expression that uses each card's value exactly once. Permitted operations
are +, -, *, /, and parentheses. The expression must evaluate to 24.

Player expressions are tokenized and evaluated with two stacks (no eval).
The solver enumerates binary expression trees recursively to decide whether
a hand has a solution, and prints one when it does.
"""

import random
from collections import Counter
from fractions import Fraction
from itertools import permutations

TARGET = 24
LEAF_PREC = 3

# Binary operators used by the solver: symbol, function, precedence (* / bind tighter).
BINARY_OPS = (
    ("+", lambda a, b: a + b, 1),
    ("-", lambda a, b: a - b, 1),
    ("*", lambda a, b: a * b, 2),
    ("/", lambda a, b: a / b, 2),
)

RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
RANK_VALUE = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}
FACE_RANKS = {"A", "J", "Q", "K"}


def deal_cards():
    """Draw four cards from a shuffled 52-card deck (4 suits of each rank)."""
    deck = list(RANKS) * 4
    random.shuffle(deck)
    return deck[:4]


def card_values(ranks):
    """Return the numeric values of the dealt ranks."""
    return [RANK_VALUE[rank] for rank in ranks]


def display_cards(ranks):
    """Print the four cards, and their values when face cards are present."""
    print("Your cards:", " ".join(ranks))
    if any(rank in FACE_RANKS for rank in ranks):
        values = card_values(ranks)
        print("Values:    ", " ".join(str(value) for value in values))


def precedence(operator):
    """Return the precedence of an operator. Highest: unary +/-, then */, then binary +-."""
    levels = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "u+": 3,
        "u-": 3,
    }
    return levels[operator]


def tokenize(expression):
    """Split an expression into numbers and + - * / ( ). Whitespace is ignored."""
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            dotted = ch == "."
            i += 1
            while i < n and (expression[i].isdigit() or (expression[i] == "." and not dotted)):
                if expression[i] == ".":
                    dotted = True
                i += 1
            lexeme = expression[start:i]
            if lexeme == ".":
                raise ValueError("invalid number")
            tokens.append(Fraction(lexeme))
            continue

        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
            continue

        raise ValueError("unsupported character")

    return tokens


def is_unary(tokens, index):
    """A + or - is unary when an operand is expected, not a binary operator."""
    if tokens[index] not in "+-":
        return False
    if index == 0:
        return True
    prev = tokens[index - 1]
    if isinstance(prev, Fraction):
        return False
    return prev in "+-*/("


def apply_operator(numbers, operators):
    """Apply the operator on top of the operators stack."""
    op = operators.pop()

    if op == "u-" or op == "u+":
        if not numbers:
            raise ValueError("missing operand")
        value = numbers.pop()
        numbers.append(-value if op == "u-" else value)
        return

    if len(numbers) < 2:
        raise ValueError("missing operand")

    right = numbers.pop()
    left = numbers.pop()

    if op == "+":
        result = left + right
    elif op == "-":
        result = left - right
    elif op == "*":
        result = left * right
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        result = left / right
    else:
        raise ValueError("unknown operator")

    numbers.append(result)


def evaluate(tokens):
    """Evaluate tokenized arithmetic with two stacks. Returns a Fraction."""
    if not tokens:
        raise ValueError("empty expression")

    numbers = []
    operators = []

    for i, token in enumerate(tokens):
        if isinstance(token, Fraction):
            numbers.append(token)
            continue

        if is_unary(tokens, i):
            operators.append("u+" if token == "+" else "u-")
            continue

        if token == "(":
            operators.append(token)
            continue

        if token == ")":
            while operators and operators[-1] != "(":
                apply_operator(numbers, operators)
            if not operators:
                raise ValueError("missing left parenthesis")
            operators.pop()
            while operators and operators[-1] in ("u+", "u-"):
                apply_operator(numbers, operators)
            continue

        if token in "+-*/":
            while (
                operators
                and operators[-1] != "("
                and precedence(operators[-1]) >= precedence(token)
            ):
                apply_operator(numbers, operators)
            operators.append(token)
            continue

        raise ValueError("unsupported character")

    while operators:
        if operators[-1] == "(":
            raise ValueError("missing right parenthesis")
        apply_operator(numbers, operators)

    if len(numbers) != 1:
        raise ValueError("invalid expression")

    return numbers[0]


def literal_values(tokens):
    """Return the numeric literals that appear in the expression."""
    return [token for token in tokens if isinstance(token, Fraction)]


def uses_cards_exactly_once(literals, values):
    """True iff the literals are exactly the four card values, each once."""
    used = []
    for literal in literals:
        if literal.denominator != 1:
            return False
        used.append(int(literal))
    return Counter(used) == Counter(values)


def format_error(err):
    """Turn an exception into an understandable error message."""
    if isinstance(err, ZeroDivisionError):
        return "Division by zero."
    message = str(err)
    known = {
        "missing right parenthesis": "Missing right parenthesis.",
        "missing left parenthesis": "Missing left parenthesis.",
        "unsupported character": "Unsupported character.",
        "empty expression": "Empty expression.",
        "missing operand": "Missing operand.",
        "invalid number": "Invalid number.",
        "invalid expression": "Invalid expression.",
    }
    if message in known:
        return known[message]
    return message[0].upper() + message[1:] + ("." if not message.endswith(".") else "")


def format_values(values):
    """Format card values for messages, e.g. '3, 3, 8, 8'."""
    return ", ".join(str(value) for value in values)


def format_result(result):
    """Show a Fraction as an integer when possible, otherwise as a mixed/decimal-like string."""
    if result.denominator == 1:
        return str(result.numerator)
    return str(result)


def combine_expressions(left, right):
    """Yield (value, text, precedence) for every operator applied to two subexpressions."""
    left_value, left_text, left_prec = left
    right_value, right_text, right_prec = right
    for op, apply, prec in BINARY_OPS:
        if op == "/" and right_value == 0:
            continue
        value = apply(left_value, right_value)
        left_shown = left_text if left_prec >= prec else f"({left_text})"
        # Left-associative: parenthesize a right child of equal or lower precedence
        # so that a / (b * c) is not printed as a / b * c.
        right_shown = right_text if right_prec > prec else f"({right_text})"
        yield (value, f"{left_shown} {op} {right_shown}", prec)


def all_expressions(values):
    """Every binary expression tree whose leaves are `values` in this order.

    A tree on n leaves is a root operator with a left tree on k leaves and a
    right tree on n-k leaves, for each split k = 1 ... n-1. Recursing on both
    sides enumerates every grouping (the five shapes for four values) without
    listing those shapes by hand. Operator choices are tried at each node.
    """
    if len(values) == 1:
        value = values[0]
        yield (value, format_result(value), LEAF_PREC)
        return

    for split in range(1, len(values)):
        for left in all_expressions(values[:split]):
            for right in all_expressions(values[split:]):
                yield from combine_expressions(left, right)


def find_solution(values):
    """Return one expression that equals 24 using each value once, or None.

    Different arrangements of the cards are the permutations of the four
    values. Combined with all_expressions, that covers every tree shape,
    every operator triple, and every leaf order.
    """
    best = None
    nums = tuple(Fraction(v) for v in values)
    for perm in set(permutations(nums)):
        for value, text, _prec in all_expressions(perm):
            if value == TARGET:
                if best is None or len(text) < len(best):
                    best = text
    return best


def report_solution(solution):
    """Print a found solution, or say that the hand is unsolvable."""
    if solution is None:
        print("No solution exists for these cards.")
    else:
        print(f"Solution: {solution} = 24")


def judge_expression(expression, values):
    """Return (ok, message) for the player's expression and the dealt values."""
    tokens = tokenize(expression)
    result = evaluate(tokens)
    if not uses_cards_exactly_once(literal_values(tokens), values):
        return (
            False,
            f"Incorrect. Use each of {format_values(values)} exactly once.",
        )
    if result == TARGET:
        return True, "Correct! That expression equals 24."
    return False, f"Incorrect. That expression equals {format_result(result)}, not 24."


def play_round():
    """Deal four cards, read one expression, and report whether it is a solution."""
    ranks = deal_cards()
    values = card_values(ranks)
    display_cards(ranks)
    solution = find_solution(values)

    try:
        expression = input("Enter an expression (or 'solve'): ")
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if expression.strip().lower() == "solve":
        report_solution(solution)
        return

    try:
        ok, message = judge_expression(expression, values)
        print(message)
        if not ok:
            report_solution(solution)
    except (ValueError, ZeroDivisionError) as err:
        print(f"Invalid expression: {format_error(err)}")
        report_solution(solution)


def main():
    print("Card Game 24")
    print("Use each card value exactly once with +, -, *, /, and parentheses to make 24.")
    print("Type solve to see a solution if one exists.")
    print()

    while True:
        play_round()
        try:
            again = input("Play again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if again not in ("y", "yes"):
            break
        print()


if __name__ == "__main__":
    main()
