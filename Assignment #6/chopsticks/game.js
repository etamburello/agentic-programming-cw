/**
 * Chopsticks game mechanics.
 *
 * State representation (mirrors chopsticks.py):
 *   [[aLeft, aRight], [bLeft, bRight], level]
 *
 * Hands hold 0–4 fingers. Even level = player A to move; odd = player B.
 * A player loses when both of their hands are 0.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.ChopsticksGame = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const HAND_LIMIT = 5;
  const DEFAULT_MOVES = 10;

  function initialState() {
    return [[1, 1], [1, 1], 0];
  }

  function cloneState(state) {
    return [
      [state[0][0], state[0][1]],
      [state[1][0], state[1][1]],
      state[2],
    ];
  }

  function stateKey(state) {
    return (
      state[0][0] + "," + state[0][1] + "|" +
      state[1][0] + "," + state[1][1] + "|" +
      state[2]
    );
  }

  function handsEqual(left, right) {
    return left[0] === right[0] && left[1] === right[1];
  }

  function handsDead(hands) {
    return hands[0] === 0 && hands[1] === 0;
  }

  /**
   * overflow_sum(a, b): add fingers; a hand that reaches 5 or more becomes 0.
   * Invalid inputs (outside 0–5) return null, matching Python's None.
   */
  function overflowSum(a, b) {
    if (a > HAND_LIMIT || b > HAND_LIMIT || a < 0 || b < 0) {
      return null;
    }
    if (a + b >= HAND_LIMIT) {
      return 0;
    }
    return a + b;
  }

  /**
   * next_moves(v): legal successors of a state.
   * Uses a set so duplicate resulting positions collapse, matching Python.
   */
  function nextMoves(state) {
    if (handsDead(state[0]) || handsDead(state[1])) {
      return [];
    }

    const l0 = state[0][0];
    const r0 = state[0][1];
    const l1 = state[1][0];
    const r1 = state[1][1];
    const h = state[2];
    const seen = new Set();
    const moves = [];

    function add(item) {
      const key = stateKey(item);
      if (!seen.has(key)) {
        seen.add(key);
        moves.push(item);
      }
    }

    if (h % 2 === 0) {
      if (l0 > 0 && l1 > 0) {
        add([[l0, r0], [overflowSum(l0, l1), r1], h + 1]);
      }
      if (l0 > 0 && r1 > 0) {
        add([[l0, r0], [l1, overflowSum(l0, r1)], h + 1]);
      }
      if (r0 > 0 && l1 > 0) {
        add([[l0, r0], [overflowSum(r0, l1), r1], h + 1]);
      }
      if (r0 > 0 && r1 > 0) {
        add([[l0, r0], [l1, overflowSum(r0, r1)], h + 1]);
      }

      for (let i = 1; i <= l0; i++) {
        const l = l0 - i;
        if (r0 + i < HAND_LIMIT) {
          const r = overflowSum(r0, i);
          if (!(r === l0 && l === r0)) {
            add([[l, r], [l1, r1], h + 1]);
          }
        }
      }
      for (let i = 1; i <= r0; i++) {
        const l = overflowSum(l0, i);
        const r = r0 - i;
        if (l0 + i < HAND_LIMIT) {
          if (!(r === l0 && l === r0)) {
            add([[l, r], [l1, r1], h + 1]);
          }
        }
      }
    } else {
      if (l1 > 0 && l0 > 0) {
        add([[overflowSum(l0, l1), r0], [l1, r1], h + 1]);
      }
      if (l1 > 0 && r0 > 0) {
        add([[l0, overflowSum(r0, l1)], [l1, r1], h + 1]);
      }
      if (r1 > 0 && l0 > 0) {
        add([[overflowSum(l0, r1), r0], [l1, r1], h + 1]);
      }
      if (r1 > 0 && r0 > 0) {
        add([[l0, overflowSum(r0, r1)], [l1, r1], h + 1]);
      }

      for (let i = 1; i <= l1; i++) {
        const l = l1 - i;
        const r = overflowSum(r1, i);
        if (r1 + i < HAND_LIMIT) {
          if (!(r === l1 && l === r1)) {
            add([[l0, r0], [l, r], h + 1]);
          }
        }
      }
      for (let i = 1; i <= r1; i++) {
        const l = overflowSum(l1, i);
        const r = r1 - i;
        if (l1 + i < HAND_LIMIT) {
          if (!(r === l1 && l === r1)) {
            add([[l0, r0], [l, r], h + 1]);
          }
        }
      }
    }

    return moves;
  }

  /** True when a player has already lost: both of their hands are 0. */
  function isTerminal(state) {
    return handsDead(state[0]) || handsDead(state[1]);
  }

  /**
   * Predetermined result for a finished position, matching best_move_dp:
   * -1 A loses, 0 tie, 1 A wins. Null if the position is not terminal.
   */
  function terminalValue(state) {
    const aDead = handsDead(state[0]);
    const bDead = handsDead(state[1]);
    if (aDead && bDead) return 0;
    if (aDead) return -1;
    if (bDead) return 1;
    return null;
  }

  function isHorizon(state, depth) {
    return state[2] >= depth;
  }

  function isGameOver(state, depth) {
    return isTerminal(state) || isHorizon(state, depth);
  }

  /**
   * Full stop condition from chopsticks_game: someone is dead, or the
   * even depth horizon is reached. Horizon with both players alive is a tie.
   * Returns null while the game is still in progress.
   */
  function gameResult(state, depth) {
    const value = terminalValue(state);
    if (value !== null) return value;
    if (isHorizon(state, depth)) return 0;
    return null;
  }

  function winnerLabel(state, depth) {
    const result = gameResult(state, depth);
    if (result === null) return null;
    if (!isTerminal(state) && isHorizon(state, depth)) return "tie";
    if (handsDead(state[0])) return "B";
    return "A";
  }

  /** 0 = A (even level), 1 = B (odd level). */
  function currentPlayer(state) {
    return state[2] % 2;
  }

  function depthFromMoves(moves) {
    return 2 * moves;
  }

  /**
   * Apply a human choice by index into nextMoves(state), matching
   * chopsticks_game's numbered prompt. Returns null if the index is illegal.
   */
  function applyMoveIndex(state, index) {
    if (isTerminal(state)) return null;
    const moves = nextMoves(state);
    if (!Number.isInteger(index) || index < 0 || index >= moves.length) {
      return null;
    }
    return cloneState(moves[index]);
  }

  function isLegalSuccessor(state, successor) {
    const key = stateKey(successor);
    const moves = nextMoves(state);
    for (let i = 0; i < moves.length; i++) {
      if (stateKey(moves[i]) === key) return true;
    }
    return false;
  }

  function applySuccessor(state, successor) {
    if (!isLegalSuccessor(state, successor)) return null;
    return cloneState(successor);
  }

  /**
   * Legal attack using the mover's hand `fromSide` (0 left, 1 right)
   * against the opponent's hand `toSide`. Null if that click is illegal.
   * The successor is taken from nextMoves, not reconstructed by the UI.
   */
  function attackMove(state, fromSide, toSide) {
    const mover = currentPlayer(state);
    const opp = 1 - mover;
    const fromCount = state[mover][fromSide];
    const toCount = state[opp][toSide];
    if (fromCount <= 0 || toCount <= 0) return null;
    const added = overflowSum(fromCount, toCount);
    const legal = nextMoves(state);
    for (let i = 0; i < legal.length; i++) {
      const succ = legal[i];
      if (!handsEqual(succ[mover], state[mover])) continue;
      if (succ[opp][toSide] !== added) continue;
      if (succ[opp][1 - toSide] !== state[opp][1 - toSide]) continue;
      return cloneState(succ);
    }
    return null;
  }

  /**
   * Legal redistributions that move `amount` fingers off `fromSide`
   * onto the mover's other hand. Filtered through nextMoves so overflow
   * and swap-rejection stay in the engine.
   */
  function transferMoves(state, fromSide) {
    const toSide = 1 - fromSide;
    const mover = currentPlayer(state);
    const opp = 1 - mover;
    const fromCount = state[mover][fromSide];
    const options = [];
    const legal = nextMoves(state);
    for (let amount = 1; amount <= fromCount; amount++) {
      const nextMover = [state[mover][0], state[mover][1]];
      nextMover[fromSide] = fromCount - amount;
      nextMover[toSide] = overflowSum(state[mover][toSide], amount);
      for (let i = 0; i < legal.length; i++) {
        const succ = legal[i];
        if (!handsEqual(succ[opp], state[opp])) continue;
        if (!handsEqual(succ[mover], nextMover)) continue;
        options.push({ amount: amount, successor: cloneState(succ) });
        break;
      }
    }
    return options;
  }

  /** "win" | "loss" | "tie" | null from the human's seat (0 = A, 1 = B). */
  function humanResult(state, depth, humanIndex) {
    if (!isGameOver(state, depth)) return null;
    const winner = winnerLabel(state, depth);
    if (winner === "tie") return "tie";
    if (winner === "A") return humanIndex === 0 ? "win" : "loss";
    return humanIndex === 1 ? "win" : "loss";
  }

  return {
    HAND_LIMIT,
    DEFAULT_MOVES,
    initialState,
    cloneState,
    stateKey,
    handsEqual,
    handsDead,
    overflowSum,
    nextMoves,
    isTerminal,
    terminalValue,
    isHorizon,
    isGameOver,
    gameResult,
    winnerLabel,
    currentPlayer,
    depthFromMoves,
    applyMoveIndex,
    isLegalSuccessor,
    applySuccessor,
    attackMove,
    transferMoves,
    humanResult,
  };
});
