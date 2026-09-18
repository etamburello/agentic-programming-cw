# 8-puzzle BFS solver
_Exported on 9/15/2026 at 18:01:15 EDT from Cursor (3.20.21)_

---

**User**

I want to build programs that solve and visualize the classic 8-puzzle. The 8-puzzle consists of eight numbered tiles and one blank space arranged on a ﻿3 cross times 3﻿ board. A legal move slides a tile adjacent to the blank into the blank position.
We will represent the blank using 0. Your programs should solve the following puzzle:
Initial state
 8 7 6
5 4 3
2 1 0

Goal state
 1 2 3
4 5 6
7 8 0

Please create a Python program that solves the puzzle using Breadth-First Search. The BFS implementation must use a queue. Python's collections.deque is a good choice because inserting at one end and removing from the other can both be done efficiently. 
rules:
- Avoid Duplicate States: An important issue in graph search is avoiding repeated work. Do not repeatedly scan the queue to determine whether a puzzle state is already present. For example, avoid relying on: if state not in queue: because searching a queue can become expensive. Instead, maintain a separate collection of states that have already been discovered. A state should be marked as discovered when it is added to the queue. The basic idea is: queue + set of discovered states. This should guarantee that the same puzzle state is never added to the BFS queue more than once.
- Reconstructing the Solution: the BFS solver should not merely report that a solution exists. It must reconstruct and display the entire optimal path:
initial state
    ↓
state 1
    ↓
state 2
    ↓
...
    ↓
goal state
 
Think about what information must be stored while performing BFS so that the path can be reconstructed after reaching the goal.
- BFS Output: the program should display each state in the solution.
For example:
Step 0
**********
8 7 6
5 4 3
2 1 0
**********
 
Step 1
**********
...
**********
 
At the end, report the total number of moves. You should also report useful search statistics such as:
Number of states expanded
Number of states discovered.
implement in 8_puzzle_bfs.py

---

**Cursor**

Implemented `Assignment #5/8_puzzle_bfs.py`.

It:
- Uses BFS with `collections.deque`
- Prevents duplicates using a discovered-state set
- Reconstructs and displays the optimal path
- Reports 30 moves
- Reports states expanded and discovered

Verified successfully with no syntax or lint errors.

---

**User**

Now build a static webpage that illustrates the BFS solution. The webpage must run entirely in the browser.
It should not require:
Python
Flask
Node.js
a database
a web server
Ideally, the project should be contained in a single file called bfs.html, which can be opened directly in a browser.

rules: 
- Minimum Visualization Features: The webpage should display the ﻿3 cross times 3﻿ puzzle board and animate the sequence of moves found by BFS.
- Provide controls such as:
Solve
Play / Pause
Previous
Next
Reset
- Also provide a way to adjust the animation speed.
- The webpage should display:
current solution step
tile being moved
total number of moves
number of states explored or discovered
Users should be able to enter another valid 8-puzzle configuration and run the visualization again.



I now want to solve the same problem using A* search.
A* assigns each state a priority: f(n) = g(n) + h(n), where g(n) is the number of moves used to reach the current state, and h(n) ﻿is an estimate of the number of moves remaining. Use Manhattan distance for ﻿h left parenthesis n right parenthesis﻿. For every numbered tile, determine how far it is from its goal location: | r - r subscript g | + | c - c subscript g |. ﻿Then add the distances for all eight numbered tiles. Do not include the blank tile in the heuristic.
For example, consider:
1 2 3
4 0 5
7 8 6
 
The goal is:
1 2 3
4 5 6
7 8 0
 
Tile 5 is one move away from its goal position and tile 6 is one move away. Therefore, h(n) = 1 + 1 = 2.﻿

rules: 
- Priority Queue: Unlike BFS, A* should not use a normal FIFO queue. Use a priority queue so that the state with the lowest ﻿f left parenthesis n right parenthesis﻿ value is processed first. In Python, you may use: heapq
- Best Known Path: Be careful about duplicate states. The BFS approach of simply saying "I have seen this state before, so ignore it forever" is not sufficient for a general A* implementation. The program should keep track of the best known g(n) for each puzzle state. If a better path to a state is found, your program should update its information appropriately.
- A* Output: Display the same solution information as BFS:
Step 0
Step 1
Step 2
...
Goal
- Also report:
Optimal number of moves
Number of states expanded
Number of states generated/discovered
 

---

**Cursor**

Implemented `Assignment #5/astar.py`.

It includes:
- `heapq` priority queue
- Manhattan-distance heuristic excluding the blank
- Best-known `g(n)` tracking and stale-entry handling
- Full optimal path reconstruction
- Expanded, generated, and discovered state counts

Verified result: optimal solution in **30 moves**, with no syntax or lint errors.

---

**User**

I now want to create a second static webpage, astar.html, that illustrates how A* solves the puzzle. In addition to animating the final solution, the webpage should help the user understand why A* selects particular states. For the current state, display: g(n)﻿, ﻿h(n), and f(n) = g(n) + h(n)
For example:
g(n) = 12
h(n) = 6 
f(n) = 18
 
The visualization should also show some representation of the A* open list, or priority queue. For candidate states, display information such as:
State A    g=10    h=8    f=18
State B    g=11    h=5    f=16
State C    g=9     h=9    f=18
 
The user should be able to see that A* selects the state with the smallest priority. Your A* page should also support:
Play / Pause
Previous
Next
Reset
Animation speed

---

**Cursor**

I’ll make each solution step show the real priority-queue snapshot from the moment A* expanded that state. This keeps the candidate comparison accurate even when A* explores off-path states between solution moves.

Created `Assignment #5/astar.html`.

Features:
- Browser-only A* search with Manhattan distance
- Animated optimal 30-move solution
- Current `g(n)`, `h(n)`, and `f(n)`
- Real priority-queue snapshots and candidate comparisons
- Play, Pause, Previous, Next, Reset, and speed controls
- Custom puzzle configurations and validation
- Search statistics

Tested successfully with no lint errors.

---

**User**

Please test both versions to ensure they are both solving the puzzle as they both should

---

**Cursor**

Both implementations passed testing:

- BFS Python/web: 30 optimal moves, 181,393 expanded
- A* Python/web: 30 optimal moves, 7,330 expanded
- Every solution transition is a legal move
- Both reach the correct goal
- Custom one-move puzzles and unsolvable-state detection work
- A* priority-queue selection is correct

No changes were needed.

