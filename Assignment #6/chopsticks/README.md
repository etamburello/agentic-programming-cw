# Project Overview
A two-player Chopsticks page with a JavaScript game engine, a bottom-up minimax AI, and a Python reference implementation. The page is static, and rules live in `game.js`, AI lives in `ai.js`, and the HTML and CSS only present state and collect clicks.

## How to run the game
1. Open `index.html`
2. Visit `http://127.0.0.1:8765/`.
3. The You first selection seats you as Player A. The You second selection seats you as Player B (meaning the computer plays first).
4. Tap one of your live hands, then an opponent hand to attack or your other hand to redistribute.
5. Analysis shows the last computer decision (minimax values and the stored move). Play hides that panel.
6. Restart starts over with the same seating.


## Game rules
Each player has two hands. A live hand shows 1–4 fingers. A hand with 0 is dead and cannot attack or donate fingers.
- Start: each player has one finger on each hand.
- Attack: on your turn, tap one of your live hands against one of the opponent’s live hands. The target becomes `overflowSum(yours, theirs)`: if the sum is at least 5, that hand becomes 0; otherwise it holds the sum.
- Redistribute: move one or more fingers from one of your hands onto the other, without bringing a hand to 5 or more. A pure left/right swap of the same two counts is rejected (the Python check `(r, l) != (l0, r0)`).
- Loss: you lose when both of your hands are 0.
- Horizon: the game lasts at most 10 full turns (20 moves). If nobody has lost by then, it is a tie.
- Even-numbered move = Player A. Odd-numbered move = Player B.

## State representation
A position is a triple, matching the Python tuple. An example would be start shown as `[[1,1],[1,1],0]`, written in the Analysis panel as `((1,1),(1,1),0)`. Hands are integers in `0–4`. `level` is the move counter and the index into the DP table.

## Explanation of nextMoves(state)
The `nextMoves` function is a direct port of the `next_moves` function in `chopsticks.py`.
1. If either player is `(0,0)`, return `[]`.
2. Generate up to four attacks (each live hand of the mover against each live hand of the opponent).
3. Generate transfers by moving `i = 1, 2, …` fingers from left to right and from right to left, skipping overflows and the swap-rejection case.
4. Deduplicate with a set (same as Python).
Branching is at most about eight successors, so move generation is O(1) per position. Duplicate attacks (both of your hands have the same count) collapse to one successor. The UI never re-implements these rules. Clicks call `attackMove` / `transferMoves`, which filter `nextMoves` rather than inventing new positions.

## Explanation of Minimax
Every stored value is from Player A’s point of view, which +1 meaning player A wins with perfect play, 0 meaning there's a tie, and -1 meaning player A loses.
- Even `level`: MAX (A chooses the child with the largest value).
- Odd `level`: MIN (B chooses the child with the smallest value — best for B, worst for A).
The AI Analysis panel prints this rule (`Player A — MAX` or `Player B — MIN`), each successor’s value, and `<- selected` on the move stored in the table. If several children share the optimal value, the table keeps the first one encountered (Python’s `set` iteration order can pick a different equally good child; the value still matches).

## Explanation of Dynamic-programming table
The best_move_dp(depth) function fills the game bottom-up.
- `depth` is even (`2 × 10 = 20` by default).
- There are `5⁴ = 625` hand configurations and `depth + 1` moves, so 13,125 entries at the real horizon.
- The horizon row: A dead → `-1`, B dead → `+1`, both dead → `0`, otherwise unfinished → `0`.
- For `h = depth-1, …, 0`, each nonterminal is the max or min of its already-computed children at `h+1`.
JavaScript then stores the table as packed typed arrays (`Int8Array` values, `Int16Array` successor configs) so lookup is O(n). Fill time is O(depth * 625 * branching). The computer does not search at click time, it simply reads `d[state]`.

## Software organization
- index.html handles layout, clicks, and view toggle. There is no overflow or DP logic present here.
- style.css handles hands, selection, attack flash, thinking, and the AI analysis panel.
- game.js handles state, the overflowSum and nextMoves functions, terminals, and applying moves.
- ai.js handles the dynamic-programming table, the chooseComputerMove and explainMove functions(later is for the Analysis view).
- chopsticks.py is simply a reference for the game, with functions like overflow_sum, next_moves, best_move_dp, CLI

## Testing performed

Engine (`node test.js`), compared to `chopsticks.py`: 136 checks, 0 failures, including:
- initial state
- a position with a zero hand
- attack that zeros a hand (`4+1 → 0`)
- legal redistribution
- illegal indexes, dead-hand attacks, swap rejection, illegal successors
- A-loss and B-loss terminals
- move-20 horizon tie
- computer as A (MAX) and as B (MIN)
- restart / `initialState()`
- AI choice when child values differ (start: `0` vs `-1`; `((1,4),(3,0),8)` mixed MAX)
- computer-vs-computer playout: no cycle, result equals both JS and Python root values

Browser: initial seating, illegal first click, redistribute to a zero hand, restart, You second (A as computer), You first then computer reply (B as computer), Analysis show/hide, a full autoplay to You lose, layout at a wide window and at 390px wide.

## Known limitations
- Play is horizon-limited (10 turns). “Perfect play” means perfect within 20 moves, not an infinite Chopsticks endgame.
- Move indexes in Python’s CLI follow `set` hash order; the page uses insertion order (attacks, then transfers). Successor sets and DP values match.
- The Python swap check forbids some one-handed transfers such as `(0,1) → (1,0)`.
- overflow_sum accepts `5` as an input bound; live hands in play stay `0–4`.
- Equal-value ties keep only one stored successor (first max/min).
- There is no undo, no loop detection beyond the move cap, and no sound.

## Possible extensions
- Undo / move history.
- Detect repeated positions as draws without waiting for move 20.
- Let the AI Analysis view highlight the matching hands on the board when you hover a successor.
- Variable horizon or “solve until a forced win.”
- Keyboard controls and a higher-contrast theme.

## Reflection questions
1. Why does Player A maximize while Player B minimizes?  
Values are always A’s score. A wants `+1`, so on even-numbered moves we take the maximum child. B wants A to get `-1`, so on odd-numbered moves we take the minimum child. That is standard zero-sum minimax with a single number, not two separate scores.

2. Why is the DP table built from the deepest level toward level 0?  
A position’s value is defined from its successors at `level + 1`. The horizon (`level = depth`) has known base cases. Filling `depth-1, depth-2, …, 0` guarantees every child is already computed. Level 0 is the real start of the game, so it must be filled last.

3. Why can dynamic programming be substantially faster than recursively exploring the complete game tree?
The same hand configuration appears under many move sequences. A recursive tree recomputes those overlapping subgames. The table computes each `(hands A, hands B, move number)` once and reuses it. With 625 hand pairs and 21 move numbers, that is thousands of constant-time updates instead of a branching-8 tree 20 moves deep.

4. Why should the UI obtain legal moves from the game engine rather than independently implementing the rules?  
Attack, overflow, transfer caps, and swap rejection would drift from next_moves if copied into click handlers. The page only names a source and target; game.js accepts the click only when that successor is already in nextMoves. One implementation stays in sync with Python and with the DP.

5. What part of the project did your AI assistant help with most?
Porting the engine and DP faithfully (overflowSum, nextMoves, bestMoveDp), wiring the click UI to those APIs, and building the comparison tests against chopsticks.py. The assistant also drafted the Analysis panel from the same table the computer uses to move.

6. What AI-generated suggestion did you have to verify, modify, or reject? 
Assuming Python’s numbered choices would match JavaScript indexes was wrong: Python iterates a `set`. We compare sets of successors and DP values, not print order. Kill positions at depth 20 also do not always have mixed child values (every child can be `+1`); mixed-value checks use the start position and `((1,4),(3,0),8)` instead. UI bugs (swapped You/Computer labels, leftover duplicate start() after an HTML edit, a second `playComputer` timeout stealing the human’s turn) were caught by playing the page and then fixed with seating from humanIndex / computerPlayer() and a single thinkTimer.
