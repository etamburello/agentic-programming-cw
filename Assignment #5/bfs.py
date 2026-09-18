from collections import deque
from typing import Optional


State = tuple[int, ...]

INITIAL_STATE: State = (
    8, 7, 6,
    5, 4, 3,
    2, 1, 0,
)

GOAL_STATE: State = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0,
)


def get_neighbors(state: State) -> list[State]:
    """Return all states reachable from state by one legal move."""
    blank = state.index(0)
    row, column = divmod(blank, 3)
    neighbors = []

    for row_change, column_change in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        new_row = row + row_change
        new_column = column + column_change

        if 0 <= new_row < 3 and 0 <= new_column < 3:
            tile = new_row * 3 + new_column
            new_state = list(state)
            new_state[blank], new_state[tile] = new_state[tile], new_state[blank]
            neighbors.append(tuple(new_state))

    return neighbors


def reconstruct_path(
    parents: dict[State, Optional[State]], goal: State
) -> list[State]:
    """Follow parent links backward, then return the path start-to-goal."""
    path = []
    current: Optional[State] = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def breadth_first_search(
    initial: State, goal: State
) -> tuple[Optional[list[State]], int, int]:
    """Find an optimal path and return it with BFS search statistics."""
    queue = deque([initial])
    discovered = {initial}
    parents: dict[State, Optional[State]] = {initial: None}
    states_expanded = 0

    while queue:
        current = queue.popleft()
        states_expanded += 1

        if current == goal:
            path = reconstruct_path(parents, current)
            return path, states_expanded, len(discovered)

        for neighbor in get_neighbors(current):
            if neighbor not in discovered:
                # Mark the state when it enters the queue, so it is queued once.
                discovered.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)

    return None, states_expanded, len(discovered)


def display_state(state: State) -> None:
    """Print one state as a 3-by-3 board."""
    print("*" * 10)
    for row_start in range(0, 9, 3):
        print(*state[row_start:row_start + 3])
    print("*" * 10)


def main() -> None:
    path, states_expanded, states_discovered = breadth_first_search(
        INITIAL_STATE, GOAL_STATE
    )

    if path is None:
        print("No solution exists.")
    else:
        for step, state in enumerate(path):
            print(f"Step {step}")
            display_state(state)
            print()

        print(f"Total number of moves: {len(path) - 1}")

    print(f"Number of states expanded: {states_expanded}")
    print(f"Number of states discovered: {states_discovered}")


if __name__ == "__main__":
    main()
