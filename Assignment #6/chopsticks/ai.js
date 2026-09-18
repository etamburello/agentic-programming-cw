/**
 * Bottom-up minimax for Chopsticks.
 *
 * Table key is packed (level, A-left, A-right, B-left, B-right).
 * Values are from player A's point of view: -1 loss, 0 tie, 1 win.
 * Even level MAX (A); odd level MIN (B).
 */
(function (root, factory) {
  function loadGame() {
    if (typeof module === "object" && module.exports) {
      return require("./game.js");
    }
    if (!root.ChopsticksGame) {
      throw new Error("Load game.js before ai.js");
    }
    return root.ChopsticksGame;
  }
  const api = factory(loadGame());
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.ChopsticksAI = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (game) {
  "use strict";

  const HANDS = 5;
  const CONFIGS = HANDS * HANDS * HANDS * HANDS;

  function configIndex(i, j, k, l) {
    return ((i * HANDS + j) * HANDS + k) * HANDS + l;
  }

  function unpackConfig(index) {
    const l = index % HANDS;
    index = (index / HANDS) | 0;
    const k = index % HANDS;
    index = (index / HANDS) | 0;
    const j = index % HANDS;
    const i = (index / HANDS) | 0;
    return [i, j, k, l];
  }

  function tableIndex(i, j, k, l, h) {
    return h * CONFIGS + configIndex(i, j, k, l);
  }

  function stateIndex(state) {
    return tableIndex(
      state[0][0],
      state[0][1],
      state[1][0],
      state[1][1],
      state[2]
    );
  }

  function terminalEntry(i, j, k, l) {
    if (i === 0 && j === 0 && k === 0 && l === 0) return 0;
    if (i === 0 && j === 0) return -1;
    if (k === 0 && l === 0) return 1;
    return null;
  }

  /**
   * best_move_dp(depth): dense table, O(depth * 5^4 * branching).
   * Branching is at most 8, so this is a few tens of thousands of updates
   * at the default depth of 20.
   */
  function bestMoveDp(depth) {
    if (depth % 2 !== 0) {
      throw new Error("depth must be even");
    }

    const size = (depth + 1) * CONFIGS;
    const values = new Int8Array(size);
    const moves = new Int16Array(size);
    moves.fill(-1);

    for (let i = 0; i < HANDS; i++) {
      for (let j = 0; j < HANDS; j++) {
        for (let k = 0; k < HANDS; k++) {
          for (let l = 0; l < HANDS; l++) {
            const idx = tableIndex(i, j, k, l, depth);
            const term = terminalEntry(i, j, k, l);
            values[idx] = term === null ? 0 : term;
          }
        }
      }
    }

    const state = [[0, 0], [0, 0], 0];
    for (let h = depth - 1; h >= 0; h--) {
      for (let i = 0; i < HANDS; i++) {
        for (let j = 0; j < HANDS; j++) {
          for (let k = 0; k < HANDS; k++) {
            for (let l = 0; l < HANDS; l++) {
              const idx = tableIndex(i, j, k, l, h);
              const term = terminalEntry(i, j, k, l);
              if (term !== null) {
                values[idx] = term;
                moves[idx] = -1;
                continue;
              }

              state[0][0] = i;
              state[0][1] = j;
              state[1][0] = k;
              state[1][1] = l;
              state[2] = h;

              const successors = game.nextMoves(state);
              const maximize = h % 2 === 0;
              let bestVal = maximize ? -2 : 2;
              let bestMove = -1;
              for (let s = 0; s < successors.length; s++) {
                const succ = successors[s];
                const child = tableIndex(
                  succ[0][0],
                  succ[0][1],
                  succ[1][0],
                  succ[1][1],
                  h + 1
                );
                const val = values[child];
                if (maximize ? val > bestVal : val < bestVal) {
                  bestVal = val;
                  bestMove = configIndex(
                    succ[0][0],
                    succ[0][1],
                    succ[1][0],
                    succ[1][1]
                  );
                }
              }

              if (bestMove < 0) {
                values[idx] = 0;
                moves[idx] = -1;
              } else {
                values[idx] = bestVal;
                moves[idx] = bestMove;
              }
            }
          }
        }
      }
    }

    return { depth, values, moves };
  }

  function decodeMove(table, state) {
    const idx = stateIndex(state);
    const packed = table.moves[idx];
    if (packed < 0) return null;
    const hands = unpackConfig(packed);
    return [
      [hands[0], hands[1]],
      [hands[2], hands[3]],
      state[2] + 1,
    ];
  }

  function evaluate(table, state) {
    const idx = stateIndex(state);
    return {
      value: table.values[idx],
      move: decodeMove(table, state),
    };
  }

  function chooseComputerMove(table, state) {
    if (game.isGameOver(state, table.depth)) return null;
    const entry = evaluate(table, state);
    return entry.move ? game.cloneState(entry.move) : null;
  }

  /**
   * Matches chopsticks_game: humanIndex 0 means the human is A (computer is B),
   * humanIndex 1 means the human is B (computer is A).
   */
  function computerWillWin(value, humanIndex) {
    return (value === 1 && humanIndex === 1) || (value === -1 && humanIndex === 0);
  }

  function formatState(state) {
    return "((" + state[0][0] + "," + state[0][1] + "),(" +
      state[1][0] + "," + state[1][1] + ")," + state[2] + ")";
  }

  function formatValue(value) {
    if (value > 0) return "+1";
    if (value < 0) return "-1";
    return "0";
  }

  function outcomeFromA(value) {
    if (value > 0) return "WIN";
    if (value < 0) return "LOSS";
    return "TIE";
  }

  /**
   * Educational snapshot of one computer decision.
   * Child values are O(1) table lookups; branching is at most 8.
   */
  function explainMove(table, state) {
    const player = game.currentPlayer(state);
    const maximize = player === 0;
    const chosen = decodeMove(table, state);
    const chosenKey = chosen ? game.stateKey(chosen) : "";
    const legal = game.nextMoves(state);
    const moves = [];
    for (let i = 0; i < legal.length; i++) {
      const succ = legal[i];
      moves.push({
        index: i + 1,
        state: game.cloneState(succ),
        formattedState: formatState(succ),
        value: evaluate(table, succ).value,
        selected: chosenKey !== "" && game.stateKey(succ) === chosenKey,
      });
    }
    const root = evaluate(table, state);
    return {
      formattedState: formatState(state),
      player: player === 0 ? "A" : "B",
      policy: maximize ? "MAX" : "MIN",
      moves: moves,
      selectedValue: root.value,
      predictedOutcome: outcomeFromA(root.value),
    };
  }

  let cached = null;

  function tableFor(depth) {
    if (cached && cached.depth === depth) return cached;
    cached = bestMoveDp(depth);
    return cached;
  }

  return {
    CONFIGS,
    configIndex,
    tableIndex,
    unpackConfig,
    bestMoveDp,
    evaluate,
    chooseComputerMove,
    computerWillWin,
    formatState,
    formatValue,
    outcomeFromA,
    explainMove,
    tableFor,
  };
});
