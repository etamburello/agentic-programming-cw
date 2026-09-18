"""
Arithmetic expression evaluation using two stacks (no eval).

Numbers stack: operands and intermediate results.
Operators stack: + - * / ( and internal unary operators u+ / u-.
"""


def precedence(operator):
    """Return the precedence of an operator. Highest: unary +/-, then */ , then binary +-."""
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
    """Split an expression into numbers and operator characters. Whitespace is ignored."""
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
            tokens.append(float(lexeme))
            continue

        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
            continue

        raise ValueError("unsupported character")

    return tokens


def is_unary(tokens, index):
    """A + or - is unary when an operand is expected, not a binary operator.

    That includes: start of the expression, immediately after another operator,
    and immediately after a left parenthesis.
    """
    if tokens[index] not in "+-":
        return False
    if index == 0:
        return True
    prev = tokens[index - 1]
    # After a number (a complete operand), + and - are binary.
    if isinstance(prev, float):
        return False
    return prev in "+-*/("


def apply_operator(numbers, operators):
    """Apply the operator on top of the operators stack.

    Binary: pop operator, pop right operand, pop left operand, compute, push result.
    Unary: pop operator, pop one operand, compute, push result.
    """
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


def evaluate(expression):
    """Scan the expression left to right and evaluate it with two stacks."""
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("empty expression")

    numbers = []
    operators = []

    for i, token in enumerate(tokens):
        # Rule 1: Number — push onto the numbers stack.
        if isinstance(token, float):
            numbers.append(token)
            continue

        # Unary + or - (highest precedence): store as u+ / u- and push.
        if is_unary(tokens, i):
            operators.append("u+" if token == "+" else "u-")
            continue

        # Rule 2: Left parenthesis — push onto the operators stack.
        # It is a boundary: operators below it are not applied until ')'.
        if token == "(":
            operators.append(token)
            continue

        # Right parenthesis: apply until '(' is on top, then discard '('.
        # Do not push ')' onto either stack.
        if token == ")":
            while operators and operators[-1] != "(":
                apply_operator(numbers, operators)
            if not operators:
                raise ValueError("missing left parenthesis")
            operators.pop()
            # A unary operator may apply to the whole parenthesized expression,
            # e.g. -(2+3).
            while operators and operators[-1] in ("u+", "u-"):
                apply_operator(numbers, operators)
            continue

        # Rule 3: Binary operator +, -, *, or /.
        # Apply the top operator while the stack is not empty, the top is not
        # '(', and the top has precedence >= the current operator (left to right
        # for equal precedence). Then push the current operator.
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

    # End of the expression: apply remaining operators.
    while operators:
        if operators[-1] == "(":
            raise ValueError("missing right parenthesis")
        apply_operator(numbers, operators)

    if len(numbers) != 1:
        raise ValueError("invalid expression")

    return numbers[0]


def format_error(err):
    """Turn an exception into an understandable error message."""
    if isinstance(err, ZeroDivisionError):
        return "Division by zero."
    message = str(err)
    if message == "missing right parenthesis":
        return "Missing right parenthesis."
    if message == "missing left parenthesis":
        return "Missing left parenthesis."
    if message == "unsupported character":
        return "Unsupported character."
    if message == "empty expression":
        return "Empty expression."
    if message == "missing operand":
        return "Missing operand."
    if message == "invalid number":
        return "Invalid number."
    return message[0].upper() + message[1:] + ("." if not message.endswith(".") else "")


def main():
    try:
        expression = input("Enter an arithmetic expression: ")
        result = evaluate(expression)
        print(f"Result: {result}")
    except (ValueError, ZeroDivisionError) as err:
        print(format_error(err))
    except EOFError:
        print()


if __name__ == "__main__":
    main()
