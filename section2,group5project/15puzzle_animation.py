import tkinter as tk
import random
import heapq

# -------- CONFIG --------
SIZE = 4
TILE = 80
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

    if r > 0:
        moves.append(swap(idx, idx - SIZE))
    if r < SIZE - 1:
        moves.append(swap(idx, idx + SIZE))
    if c > 0:
        moves.append(swap(idx, idx - 1))
    if c < SIZE - 1:
        moves.append(swap(idx, idx + 1))

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

    while pq:
        _, cost, state, path = heapq.heappop(pq)

        if state == GOAL:
            return path

        if state in visited:
            continue

        visited.add(state)

        for nxt in get_moves(state):
            heapq.heappush(
                pq,
                (cost + 1 + manhattan(nxt), cost + 1, nxt, path + [nxt])
            )


# -------- GUI --------
class PuzzleGUI:
    def __init__(self, start, solution):
        self.root = tk.Tk()
        self.root.title("15 Puzzle – Click to Start")

        self.canvas = tk.Canvas(
            self.root,
            width=SIZE * TILE,
            height=SIZE * TILE,
            bg="white"
        )
        self.canvas.pack()

        self.state = list(start)
        self.solution = solution

        self.draw()
        self.canvas.create_text(
            SIZE * TILE // 2,
            SIZE * TILE // 2,
            text="Click to Start",
            font=("Arial", 24, "bold"),
            fill="red"
        )

        self.canvas.bind("<Button-1>", self.start)
        self.root.mainloop()

    def draw(self):
        self.canvas.delete("all")
        for i, v in enumerate(self.state):
            if v != 0:
                r, c = divmod(i, SIZE)
                self.canvas.create_rectangle(
                    c * TILE, r * TILE,
                    c * TILE + TILE, r * TILE + TILE,
                    fill="lightblue",
                    outline="black"
                )
                self.canvas.create_text(
                    c * TILE + TILE // 2,
                    r * TILE + TILE // 2,
                    text=str(v),
                    font=("Arial", 20, "bold")
                )

    def start(self, event):
        self.canvas.unbind("<Button-1>")
        self.animate()

    def animate(self):
        if self.solution:
            self.state = list(self.solution.pop(0))
            self.draw()
            self.root.after(600, self.animate)


# -------- RUN --------
START = scramble()
solution = astar(START)
PuzzleGUI(START, solution)
