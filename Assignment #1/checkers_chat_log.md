# Checkerboard arrangement function
_Exported on 9/3/2026 at 17:52:08 EDT from Cursor (3.19.7)_

---

**User**

Consider a row of 2n checkers. Initially, the leftmost n checkers are red, and the rightmost n checkers are black. You can represent the arrangement using a Python list, where 0 represents a red checker and 1 represents a black checker. So for example, when n = 3, the initial configuration is [0, 0, 0, 1, 1, 1]. My goal is to change the initial order into an alternating sequence of red and black checkers, with the leftmost checker always red. The desired final configuration would have the form [0, 1, 0, 1, …, 0, 1], or looking at my example, when n = 3: [0, 0, 0, 1, 1, 1] would become [0, 1, 0, 1, 0 , 1]. Please design a one file recursive Python function that performs a sequence of legal adjacent swaps to transform the initial configuration into the desired alternating configuration.


---

**Cursor**

I'll look at the workspace for any existing checker-swap notes, then write a single recursive Python function that uses only adjacent swaps.

The middle `2(n-1)` checkers are the same problem at a smaller size, so I’ll recurse on that slice, then fix the remaining inverted pairs with adjacent swaps.

The algorithm works. I'll add a trace of each adjacent swap so the sequence is visible, especially for the n = 3 example.

The function is in `checkers.py`. It rearranges `[0]*n + [1]*n` into `[0, 1]*n` using only adjacent swaps.

**The recursive idea:** in a row of `2n` checkers that starts as `n` reds then `n` blacks, the **middle** `2(n-1)` checkers are the same problem one size smaller. Recurse on that slice, then fix what is left with `n-1` adjacent swaps.

For `n = 3`:

```
[0, 0, 0, 1, 1, 1]
      └─ n=2 ─┘          recurse on the middle 4
```

After the recursive call the board is `[0, 0, 1, 0, 1, 1]`. That is `[0]` plus the alternating pattern of size `n-1`, plus `[1]`. Each leftover inversion is an adjacent pair, so two swaps finish it:

```
swap 1 and 2:  [0, 1, 0, 0, 1, 1]
swap 3 and 4:  [0, 1, 0, 1, 0, 1]
```

**Base case:** `n ≤ 1` is already `[0, 1]`.

The whole algorithm is:

```python
def alternate(board, start=0, n=None):
    if n is None:
        n = len(board) // 2
    if n <= 1:
        return
    alternate(board, start + 1, n - 1)
    for k in range(n - 1):
        i = start + 1 + 2 * k
        board[i], board[i + 1] = board[i + 1], board[i]
```

Run it with `python3 checkers.py` to see the swap sequence for `n = 1` through `4`.

---

**User**

Don't include the demostration for now, just simply the recursive function

---

**Cursor**

I'll strip the file down to just the recursive function—no demo, no tracing.

`checkers.py` now contains only `alternate`. It recurses on the middle `2(n-1)` checkers, then swaps the leftover adjacent pairs into the `[0, 1, 0, 1, …]` pattern.

---

**User**

Based on the function of the python script and the example given, please design an animation page using an html file to show the checkers and how the python function works. above the checker animation, record and display the current step, the total number of swaps, and the recurive interval for each input given.

---

**Cursor**

I'll read the recursive function and assignment folder so the animation can match the algorithm and show step, swap count, and recursive interval.

I'll check available browser tools, then build a self-contained HTML page that animates the same recursion and stats.

I'll build a self-contained HTML page that animates the same recursion, with live stats for the current step, total swaps, and the active board interval.

I'll guard against reset-during-play races so the animation can't apply a stale swap to a new board.

The animation is in `Assignment #1/checkers.html`. Open that file in a browser.

Above the board it shows three live values for whatever **n** you enter:

- **Current step** — which recorded action is playing (`k / total events`), plus a short description
- **Total swaps** — `n(n − 1) / 2`, matching the recurrence `T(n) = T(n − 1) + (n − 1)`
- **Recursive interval** — the slice the current call owns, `board[start : start + 2n]`, also drawn as the gold bracket on the felt

The animation follows `alternate()` exactly: it dives into the middle interval, then swaps leftover adjacent pairs. The log on the right records every recursive call, return, and swap with its interval and running swap count. Use **Play**, **Step**, and **n** (1–8) to walk through cases like `[0, 0, 0, 1, 1, 1] → [0, 1, 0, 1, 0, 1]`.

I could not click through it here (no browser tools in this session), so after you open the file, Play with `n = 3` is the quickest check.

---

**User**

Display python list representation directly under the checker animation and within the same box. Also edit selections at the top next to n = ? to be "Start", "Previous", "Play", "Next", and "Reset" with their respective functionality.

---

**Cursor**

I'll update the controls to Start, Previous, Play, Next, and Reset, and add the Python list under the checkers inside the same board box.

I'll put the Python list under the checkers in the felt box, and replace the top controls with Start, Previous, Play, Next, and Reset.

The Python list now sits directly under the checkers in the same felt board, and the controls next to **n =** are **Start**, **Previous**, **Play**, **Next**, and **Reset**.

- **Start** — jump to the initial list for the current `n`, paused  
- **Previous** — undo the last recursive step (reverses a swap when needed)  
- **Play** — run the animation; click again to pause  
- **Next** — one step forward  
- **Reset** — restore `n = 3` and the starting board `[0, 0, 0, 1, 1, 1]`

The list under the pieces updates with each step, for example `[0, 0, 0, 1, 1, 1]` → `[0, 1, 0, 1, 0, 1]`. Reload `checkers.html` to see it.

---

**User**

I want to make my python function faster but remain recursive. Do you have any suggestions?

---

**Cursor**

The recursive structure is already doing the minimum amount of real work. Each adjacent red/black swap removes one inversion, and there are exactly `n(n − 1)/2` of them, so you cannot reduce the swap count without dropping the “legal adjacent swaps” rule.

What you *can* speed up is Python overhead around those swaps.

**1. Stop re-checking defaults on every call.**  
`n is None` is only needed at the top. Recursive calls already pass `n`, so a thin wrapper plus an inner function avoids that branch `n` times:

```python
def alternate(board, start=0, n=None):
    if n is None:
        n = len(board) // 2

    def rec(start, n):
        if n <= 1:
            return
        rec(start + 1, n - 1)
        i = start + 1
        last = start + 2 * n - 1
        while i < last:
            board[i], board[i + 1] = board[i + 1], board[i]
            i += 2

    rec(start, n)
```

**2. Tighten the swap loop.**  
`i = start + 1 + 2 * k` recomputes the index every iteration. Walking `i += 2` does the same adjacent pairs with less arithmetic. Those pairs do not overlap, so the order among them does not matter.

**3. Skip things that will not help here.**  
Memoization does nothing: this mutates a board, it does not recompute overlapping values. Tail-call tricks do nothing: CPython does not optimize them, and the swaps happen *after* the recursive call anyway. An iterative version would only remove `O(n)` call overhead, which is already dominated by `Θ(n²)` swaps.

**4. Recursion depth.**  
Depth is `n`, which is fine for typical assignment sizes. That is not the bottleneck until `n` is thousands.

For this problem, “faster and still recursive” means a wrapper plus a leaner inner `rec`, not a different algorithm. The animation will still show the same sequence of adjacent swaps. I can drop that version into `checkers.py` if you want.

---

**User**

Implement these changes, and make sure my animation displays these changes as well

---

**Cursor**

I'll update the Python function first, then align the animation's code display and swap loop with that version.

The Python function now uses an inner `rec` helper and a tighter `while i += 2` swap loop. The animation matches that version: the code panel shows the new function, highlights `rec(...)`, `while i < last`, and the swap line, and the step log records `rec(start=…, n=…)` instead of `alternate`.

The checker moves are unchanged — same adjacent pairs, just walked with less index arithmetic. Reload `checkers.html` to see it.

---

**User**

Add the speed amount, in miliseconds, next to the adjustable button. Also make the total swaps add up to the final total instead of displaying the final total immediately. 

---

**Cursor**

I'll show the slider delay in milliseconds and make the Total swaps figure count up as each swap happens.

The speed slider now shows its delay in milliseconds, for example **400 ms**, and that value is the time between Play steps.

**Total swaps** starts at 0 and increases only when an adjacent swap actually happens. The final `T(n)` formula appears after the last swap, not at the beginning. Reload `checkers.html` to see both.

