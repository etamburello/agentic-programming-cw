import heapq
from itertools import count
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

# Save each numbered tile's goal row and column for fast heuristic calls.
GOAL_POSITIONS = {
    tile: divmod(index, 3)
    for index, tile in enumerate(GOAL_STATE)
    if tile != 0
}


def manhattan_distance(state: State) -> int:
    """Return the total Manhattan distance of the eight numbered tiles."""
    distance = 0

    for index, tile in enumerate(state):
        if tile == 0:
            continue

        row, column = divmod(index, 3)
        goal_row, goal_column = GOAL_POSITIONS[tile]
        distance += abs(row - goal_row) + abs(column - goal_column)

    return distance


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
    """Follow parent links backward and return the path start-to-goal."""
    path = []
    current: Optional[State] = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def a_star_search(
    initial: State, goal: State
) -> tuple[Optional[list[State]], int, int, int]:
    """Return an optimal path and A* search statistics."""
    tie_breaker = count()
    initial_h = manhattan_distance(initial)

    # Entries are (f, h, insertion order, g, state). The h and insertion
    # order provide deterministic tie-breaking without changing A* priority.
    priority_queue = [
        (initial_h, initial_h, next(tie_breaker), 0, initial)
    ]
    best_g = {initial: 0}
    parents: dict[State, Optional[State]] = {initial: None}
    states_expanded = 0
    states_generated = 1

    while priority_queue:
        _, _, _, current_g, current = heapq.heappop(priority_queue)

        # A better route may have been inserted after this heap entry.
        # Ignore the old entry instead of expanding an outdated path.
        if current_g != best_g[current]:
            continue

        states_expanded += 1

        if current == goal:
            return (
                reconstruct_path(parents, current),
                states_expanded,
                states_generated,
                len(best_g),
            )

        for neighbor in get_neighbors(current):
            tentative_g = current_g + 1

            if tentative_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = tentative_g
                parents[neighbor] = current
                neighbor_h = manhattan_distance(neighbor)
                heapq.heappush(
                    priority_queue,
                    (
                        tentative_g + neighbor_h,
                        neighbor_h,
                        next(tie_breaker),
                        tentative_g,
                        neighbor,
                    ),
                )
                states_generated += 1

    return None, states_expanded, states_generated, len(best_g)


def display_state(state: State) -> None:
    """Print one state as a 3-by-3 board."""
    print("*" * 10)
    for row_start in range(0, 9, 3):
        print(*state[row_start:row_start + 3])
    print("*" * 10)


def main() -> None:
    path, states_expanded, states_generated, states_discovered = a_star_search(
        INITIAL_STATE, GOAL_STATE
    )

    if path is None:
        print("No solution exists.")
    else:
        for step, state in enumerate(path):
            print(f"Step {step}")
            display_state(state)
            print()

        print("Goal reached.")
        print(f"Optimal number of moves: {len(path) - 1}")

    print(f"Number of states expanded: {states_expanded}")
    print(f"Number of states generated: {states_generated}")
    print(f"Number of states discovered: {states_discovered}")


if __name__ == "__main__":
    main()
