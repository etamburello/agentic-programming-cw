#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const path = require("path");
const game = require("./game.js");
const ai = require("./ai.js");

const here = __dirname;
const py = spawnSync("python3", [path.join(here, "test_reference.py")], {
  encoding: "utf8",
  timeout: 15000,
});
if (py.status !== 0) {
  process.stderr.write(py.stderr || py.stdout || "python dump failed\n");
  process.exit(1);
}
const ref = JSON.parse(py.stdout);
const table = ai.bestMoveDp(ref.depth);

let passed = 0;
let failed = 0;
const failures = [];

function check(name, cond, detail) {
  if (cond) {
    passed += 1;
    console.log("  PASS  " + name);
  } else {
    failed += 1;
    failures.push(name + (detail ? " — " + detail : ""));
    console.log("  FAIL  " + name + (detail ? " — " + detail : ""));
  }
}

function key(state) {
  return game.stateKey(state);
}

function setEq(a, b) {
  const A = a.map(key).sort();
  const B = b.map(key).sort();
  return A.length === B.length && A.every((k, i) => k === B[i]);
}

function refCase(state) {
  const k = key(state);
  return ref.cases.find((c) => key(c.state) === k);
}

function playout(start, computerPlayer) {
  let cur = game.cloneState(start);
  const path = [key(cur)];
  while (!game.isGameOver(cur, table.depth)) {
    if (game.currentPlayer(cur) !== computerPlayer) break;
    const next = ai.chooseComputerMove(table, cur);
    if (!next) break;
    cur = next;
    path.push(key(cur));
  }
  return { state: cur, path: path };
}

function bothComputers(start) {
  let cur = game.cloneState(start);
  const seen = new Set();
  while (!game.isGameOver(cur, table.depth)) {
    const k = key(cur);
    if (seen.has(k)) return { state: cur, cycle: true };
    seen.add(k);
    const next = ai.chooseComputerMove(table, cur);
    if (!next) break;
    cur = next;
  }
  return { state: cur, cycle: false };
}

console.log("\n=== Algorithm tests (JS vs chopsticks.py) ===\n");

console.log("overflowSum grid");
ref.overflow.forEach(([a, b, py]) => {
  check(
    "overflowSum(" + a + "," + b + ")",
    game.overflowSum(a, b) === py,
    "js=" + game.overflowSum(a, b) + " py=" + py
  );
});

console.log("\ninitial state");
{
  const s = game.initialState();
  const r = refCase(s);
  check("start is ((1,1),(1,1),0)", key(s) === "1,1|1,1|0");
  check("start is not terminal", game.isTerminal(s) === false);
  check("start is A's turn", game.currentPlayer(s) === 0);
  check("start nextMoves match Python", setEq(game.nextMoves(s), r.moves));
  check("start DP value matches Python", ai.evaluate(table, s).value === r.value);
}

console.log("\nstate containing a zero hand");
{
  const s = [[0, 2], [1, 1], 0];
  const r = refCase(s);
  check("zero-hand is not fully terminal", game.isTerminal(s) === false);
  check("dead hand cannot attack", game.attackMove(s, 0, 0) === null);
  check("live hand can attack", game.attackMove(s, 1, 0) !== null);
  check("zero-hand nextMoves match Python", setEq(game.nextMoves(s), r.moves));
  check("zero-hand DP value matches Python", ai.evaluate(table, s).value === r.value);
}

console.log("\nattack causing a hand to become zero");
{
  const s = [[4, 0], [1, 0], 0];
  const kill = game.attackMove(s, 0, 0);
  const r = refCase(s);
  check("4+1 overflow attack exists", kill !== null);
  check("target becomes (0,0)", kill && key(kill) === "4,0|0,0|1");
  check("result is terminal", game.isTerminal(kill));
  check("B loses / A wins", game.terminalValue(kill) === 1);
  check("kill position nextMoves match Python", setEq(game.nextMoves(s), r.moves));
  check("Python also stores the win", r.value === 1);
}

console.log("\nlegal redistribution");
{
  const s = game.initialState();
  const left = game.transferMoves(s, 0);
  const right = game.transferMoves(s, 1);
  check("left-to-right amount 1", left.length === 1 && left[0].amount === 1);
  check("becomes (0,2)", key(left[0].successor) === "0,2|1,1|1");
  check("right-to-left becomes (2,0)", key(right[0].successor) === "2,0|1,1|1");
  check("transfer is in Python next_moves", refCase(s).moves.some((m) => key(m) === "0,2|1,1|1"));
}

console.log("\nattempts at illegal moves");
{
  const start = game.initialState();
  const zero = [[0, 2], [1, 1], 0];
  const swap = [[0, 1], [0, 1], 0];
  check("illegal successor rejected", game.applySuccessor(start, [[4, 4], [4, 4], 1]) === null);
  check("out of range index rejected", game.applyMoveIndex(start, 99) === null);
  check("negative index rejected", game.applyMoveIndex(start, -1) === null);
  check("terminal rejects moves", game.applyMoveIndex([[0, 0], [1, 1], 0], 0) === null);
  check("dead hand cannot attack", game.attackMove(zero, 0, 1) === null);
  check("swap-rejection has no transfer", game.transferMoves(swap, 1).length === 0);
  check("overflowSum invalid returns null", game.overflowSum(-1, 2) === null);
  check("Python next_moves empty on terminal", refCase([[0, 0], [1, 1], 3]).moves.length === 0);
}

console.log("\nterminal state where A loses");
{
  const s = [[0, 0], [1, 1], 3];
  const r = refCase(s);
  check("isTerminal", game.isTerminal(s));
  check("terminalValue -1", game.terminalValue(s) === -1);
  check("winner B", game.winnerLabel(s, 20) === "B");
  check("human A result is loss", game.humanResult(s, 20, 0) === "loss");
  check("human B result is win", game.humanResult(s, 20, 1) === "win");
  check("Python value -1", r.value === -1);
  check("no legal moves", game.nextMoves(s).length === 0);
}

console.log("\nterminal state where B loses");
{
  const s = [[1, 1], [0, 0], 2];
  const r = refCase(s);
  check("isTerminal", game.isTerminal(s));
  check("terminalValue 1", game.terminalValue(s) === 1);
  check("winner A", game.winnerLabel(s, 20) === "A");
  check("Python value 1", r.value === 1);
}

console.log("\nmaximum-depth tie");
{
  const s = [[1, 1], [1, 1], 20];
  const r = refCase(s);
  check("horizon is game over", game.isGameOver(s, 20));
  check("not a player-elimination terminal", game.isTerminal(s) === false);
  check("gameResult 0", game.gameResult(s, 20) === 0);
  check("winnerLabel tie", game.winnerLabel(s, 20) === "tie");
  check("Python horizon value 0", r.value === 0);
}

console.log("\n=== Complete-game tests ===\n");

console.log("Player A as computer");
{
  const start = game.initialState();
  const move = ai.chooseComputerMove(table, start);
  const r = refCase(start);
  const expl = ai.explainMove(table, start);
  check("A to move is MAX", expl.policy === "MAX" && expl.player === "A");
  check("A computer move is legal", game.isLegalSuccessor(start, move));
  check("A computer value matches Python", expl.selectedValue === r.value);
  check("selected child is optimal for MAX", expl.moves.find((m) => m.selected).value === Math.max(...expl.moves.map((m) => m.value)));
  const rest = playout(move, 1);
  check("after A moves it is B's turn or over", game.currentPlayer(rest.path.length ? move : start) === 1 || game.isGameOver(move, 20));
}

console.log("Player B as computer");
{
  const afterA = [[1, 1], [2, 1], 1];
  const r = refCase(afterA) || { value: ai.evaluate(table, afterA).value, moves: game.nextMoves(afterA) };
  const expl = ai.explainMove(table, afterA);
  const move = ai.chooseComputerMove(table, afterA);
  check("B to move is MIN", expl.policy === "MIN" && expl.player === "B");
  check("B computer move is legal", game.isLegalSuccessor(afterA, move));
  check("B computer value matches table", expl.selectedValue === ai.evaluate(table, afterA).value);
  check("selected child is optimal for MIN", expl.moves.find((m) => m.selected).value === Math.min(...expl.moves.map((m) => m.value)));
  if (r.moves) check("B position successors match Python", setEq(game.nextMoves(afterA), r.moves));
}

console.log("restart / new game");
{
  const a = game.initialState();
  const b = game.applySuccessor(a, game.nextMoves(a)[0]);
  const restarted = game.initialState();
  check("new game returns to start", key(restarted) === key(a));
  check("mid-game state differs from start", key(b) !== key(a));
}

console.log("AI move selection when successor values differ");
{
  const start = game.initialState();
  const explS = ai.explainMove(table, start);
  const valuesS = new Set(explS.moves.map((m) => m.value));
  check("start has mixed child values", valuesS.size > 1);
  check("MAX avoids the -1 transfers", explS.moves.find((m) => m.selected).value === 0);
  check("Python start value matches", refCase(start).value === explS.selectedValue);

  const aWin = [[4, 0], [1, 0], 0];
  const explA = ai.explainMove(table, aWin);
  check("MAX predicted WIN", explA.predictedOutcome === "WIN");
  check("selected is the overflow kill", key(ai.chooseComputerMove(table, aWin)) === "4,0|0,0|1");
  check("Python agrees on value 1", refCase(aWin).value === 1);

  const bWin = [[1, 0], [4, 0], 1];
  const explB = ai.explainMove(table, bWin);
  check("MIN predicted LOSS for A", explB.predictedOutcome === "LOSS");
  check("selected is the overflow kill of A", key(ai.chooseComputerMove(table, bWin)) === "0,0|4,0|2");
  check("Python agrees on value -1", refCase(bWin).value === -1);

  const mixed = [[1, 4], [3, 0], 8];
  const explM = ai.explainMove(table, mixed);
  const valsM = explM.moves.map((m) => m.value);
  check("example mixed position has more than one value", new Set(valsM).size > 1);
  check("MAX selected value equals max child", explM.selectedValue === Math.max(...valsM));
  check("Python value matches", refCase(mixed).value === explM.selectedValue);
}

console.log("complete both-computers playout");
{
  const start = game.initialState();
  const root = ai.evaluate(table, start);
  const end = bothComputers(start);
  check("no cycle under stored policy", end.cycle === false);
  check("playout reaches a stop", game.isGameOver(end.state, 20));
  const result = game.gameResult(end.state, 20);
  check("playout result matches root value", result === root.value);
  check("Python root value matches JS", refCase(start).value === root.value);
}

console.log("\n=== Summary ===");
console.log("passed " + passed + "  failed " + failed);
if (failures.length) {
  failures.forEach((f) => console.log(" - " + f));
  process.exit(1);
}
console.log("ok");
