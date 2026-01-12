import random
import heapq
import time

# -------- CONFIG --------
SIZE = 4
SCRAMBLE_MOVES = 60

GOAL = (1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 14, 15, 0)
# ------------------------


def get_moves(state):
    idx = state.index(0)
    r, c = divmod(idx, SIZE)
    moves = []

    def swap(i, j):
        s = list(state)
        s[i], s[j] = s[j], s[i]
        return tuple(s)

    if r > 0: moves.append(swap(idx, idx - SIZE))
    if r < SIZE - 1: moves.append(swap(idx, idx + SIZE))
    if c > 0: moves.append(swap(idx, idx - 1))
    if c < SIZE - 1: moves.append(swap(idx, idx + 1))

    return moves


def scramble():
    state = GOAL
    for _ in range(SCRAMBLE_MOVES):
        state = random.choice(get_moves(state))
    return state


def manhattan(state):
    d = 0
    for i, v in enumerate(state):
        if v == 0:
            continue
        gi = GOAL.index(v)
        r1, c1 = divmod(i, SIZE)
        r2, c2 = divmod(gi, SIZE)
        d += abs(r1 - r2) + abs(c1 - c2)
    return d


def astar(start):
    pq = [(manhattan(start), 0, start, [])]
    visited = set()
    max_states = 0  # Track space usage

    while pq:
        _, cost, state, path = heapq.heappop(pq)

        if state == GOAL:
            return path, max_states

        if state in visited:
            continue

        visited.add(state)
        max_states = max(max_states, len(visited))

        for nxt in get_moves(state):
            heapq.heappush(
                pq,
                (cost + 1 + manhattan(nxt), cost + 1, nxt, path + [nxt])
            )


# -------- RUN ALGORITHM --------
if __name__ == "__main__":
    START = scramble()
    print("Scrambled Start:")
    print(START)

    start_time = time.time()
    solution, space = astar(START)
    end_time = time.time()

    print("\nA* Algorithm Results:")
    print(f"Number of moves to solve: {len(solution)}")
    print(f"States explored (space used): {space}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
