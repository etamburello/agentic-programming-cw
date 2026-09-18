#!/usr/bin/env python3
"""Dump chopsticks.py reference data as JSON for the JS test harness."""
import ast
import json
import sys
import io
import contextlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "chopsticks.py"
src = ROOT.read_text()
mod = ast.parse(src)
keep = ast.Module(
    body=[n for n in mod.body if isinstance(n, ast.FunctionDef)],
    type_ignores=[],
)
ns = {}
exec(compile(keep, str(ROOT), "exec"), ns)
overflow_sum = ns["overflow_sum"]
next_moves = ns["next_moves"]
best_move_dp = ns["best_move_dp"]


def ser(state):
    a, b, h = state
    return [list(a), list(b), h]


def ser_move(move):
    if move == [] or move is None:
        return None
    return ser(move)


STATES = [
    ((1, 1), (1, 1), 0),
    ((1, 1), (1, 1), 1),
    ((0, 2), (1, 1), 0),
    ((0, 2), (1, 1), 1),
    ((1, 1), (0, 2), 0),
    ((4, 0), (1, 0), 0),
    ((1, 0), (4, 0), 1),
    ((0, 1), (0, 1), 0),
    ((0, 0), (1, 1), 3),
    ((1, 1), (0, 0), 2),
    ((0, 0), (0, 0), 4),
    ((2, 3), (1, 0), 0),
    ((1, 4), (3, 0), 8),
    ((1, 1), (1, 1), 20),
    ((1, 1), (2, 1), 1),
    ((2, 1), (2, 1), 2),
]

DEPTH = 20
table = best_move_dp(DEPTH)

overflow = []
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    for a in range(-1, 7):
        for b in range(-1, 7):
            overflow.append([a, b, overflow_sum(a, b)])

packed = []
for state in STATES:
    val, move = table[state]
    successors = next_moves(state)
    packed.append({
        "state": ser(state),
        "moves": [ser(m) for m in successors],
        "value": val,
        "best": ser_move(move),
        "childValues": (
            [table[m][0] for m in successors] if state[2] < DEPTH else []
        ),
    })

print(json.dumps({"depth": DEPTH, "overflow": overflow, "cases": packed}))
sys.stdout.flush()
