import tkinter as tk
from tkinter import messagebox

# --- Window setup ---
root = tk.Tk()
root.title("Tic Tac Toe Multiplayer")

# --- Player name inputs ---
p1 = tk.StringVar()
p2 = tk.StringVar()

tk.Label(root, text="Player 1 (X):", font=("Times", 16, "bold")).grid(row=0, column=0, sticky="e", padx=6, pady=6)
tk.Entry(root, textvariable=p1, bd=3, width=20).grid(row=0, column=1, columnspan=2, sticky="w", padx=6)

tk.Label(root, text="Player 2 (O):", font=("Times", 16, "bold")).grid(row=1, column=0, sticky="e", padx=6, pady=6)
tk.Entry(root, textvariable=p2, bd=3, width=20).grid(row=1, column=1, columnspan=2, sticky="w", padx=6)

# --- Game state ---
board_buttons = []
turn = tk.StringVar(value="X")  # current player mark ("X" or "O")
moves = tk.IntVar(value=0)      # number of moves played

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def name_for_mark(mark: str) -> str:
    """Return display name for the given mark."""
    name = p1.get().strip() if mark == "X" else p2.get().strip()
    if not name:
        name = f"Player {mark}"
    return name

def set_board_enabled(enabled: bool):
    state = tk.NORMAL if enabled else tk.DISABLED
    for b in board_buttons:
        b.configure(state=state)

def reset_game():
    """Reset the board and state for a new game."""
    for b in board_buttons:
        b.configure(text="", state=tk.NORMAL)
    turn.set("X")
    moves.set(0)

def check_winner():
    """Return 'X' or 'O' if there is a winner, 'Tie' if tie, or None if game continues."""
    # Check wins
    for a, b, c in WIN_COMBOS:
        t1, t2, t3 = board_buttons[a]["text"], board_buttons[b]["text"], board_buttons[c]["text"]
        if t1 and t1 == t2 == t3:
            return t1
    # Check tie
    if moves.get() == 9:
        return "Tie"
    return None

def on_click(i: int):
    """Handle a square click."""
    # Ignore if already filled or disabled
    if board_buttons[i]["text"] or board_buttons[i]["state"] == tk.DISABLED:
        messagebox.showinfo("Tic Tac Toe", "That square is already taken.")
        return

    current = turn.get()
    board_buttons[i].configure(text=current)

    # Update move count BEFORE checking for tie
    moves.set(moves.get() + 1)

    # Check for result
    result = check_winner()
    if result == "X" or result == "O":
        set_board_enabled(False)
        messagebox.showinfo("Tic Tac Toe", f"{name_for_mark(result)} wins!")
        return
    elif result == "Tie":
        set_board_enabled(False)
        messagebox.showinfo("Tic Tac Toe", "It's a Tie!")
        return

    # Toggle turn
    turn.set("O" if current == "X" else "X")

# --- Board buttons (3x3) ---
for r in range(3):
    for c in range(3):
        idx = r * 3 + c
        btn = tk.Button(
            root,
            text="",
            font=("Times", 20, "bold"),
            bg="gray",
            fg="white",
            width=6,
            height=2,
            command=lambda i=idx: on_click(i)
        )
        btn.grid(row=r + 3, column=c, padx=3, pady=3)
        board_buttons.append(btn)

# --- Restart button ---
restart_btn = tk.Button(
    root,
    text="Restart Game",
    font=("Times", 14, "bold"),
    bg="green",
    fg="white",
    width=18,
    command=reset_game
)
restart_btn.grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
