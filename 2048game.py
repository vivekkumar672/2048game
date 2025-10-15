import tkinter as tk
import random

# ---------- Configurable Board Size ----------
BOARD_SIZE = 4

# ---------- Colors and Styling ----------
COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2")
}

# ---------- Functional Game Logic ----------
def init_board(size):
    board = [[0] * size for _ in range(size)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_cells = [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = random.choice([2, 4])

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (len(row) - len(new_row))
    return new_row

def merge(row):
    score = 0
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return row, score

def move_left(board):
    new_board = []
    total_score = 0
    for row in board:
        compressed = compress(row)
        merged, score = merge(compressed)
        final = compress(merged)
        new_board.append(final)
        total_score += score
    return new_board, total_score

def reverse(board):
    return [row[::-1] for row in board]

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_right(board):
    reversed_board = reverse(board)
    new_board, score = move_left(reversed_board)
    return reverse(new_board), score

def move_up(board):
    transposed = transpose(board)
    new_board, score = move_left(transposed)
    return transpose(new_board), score

def move_down(board):
    transposed = transpose(board)
    new_board, score = move_right(transposed)
    return transpose(new_board), score

def can_move(board):
    # Any empty cell or mergeable neighbor?
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                return True
            if c < len(board)-1 and board[r][c] == board[r][c+1]:
                return True
            if r < len(board)-1 and board[r][c] == board[r+1][c]:
                return True
    return False

# ---------- GUI Implementation ----------
class Game2048(tk.Frame):
    def __init__(self, master=None, size=BOARD_SIZE):
        super().__init__(master)
        self.master = master
        self.size = size
        self.grid()
        self.master.title("2048 Game - Vivek Kumar Mahto")
        self.master.resizable(False, False)

        self.board = init_board(self.size)
        self.score = 0

        self.cells = []
        self.init_GUI()
        self.update_GUI()

        self.master.bind("<Key>", self.key_handler)

    def init_GUI(self):
        # Score label
        self.score_label = tk.Label(self, text="Score: 0", font=("Helvetica", 18, "bold"))
        self.score_label.grid(row=0, column=0, columnspan=self.size, pady=10)

        # Game grid
        background = tk.Frame(self, bg="#bbada0", bd=3)
        background.grid(row=1, column=0, columnspan=self.size)

        for r in range(self.size):
            row = []
            for c in range(self.size):
                cell = tk.Label(
                    background,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    width=4,
                    height=2,
                    bg=COLORS[0][0],
                    fg=COLORS[0][1],
                    borderwidth=4,
                    relief="ridge",
                )
                cell.grid(row=r, column=c, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

        # Restart button
        restart_btn = tk.Button(self, text="Restart", command=self.restart, font=("Helvetica", 14, "bold"), bg="#8f7a66", fg="white")
        restart_btn.grid(row=2, column=0, columnspan=self.size, pady=10)

    def update_GUI(self):
        for r in range(self.size):
            for c in range(self.size):
                value = self.board[r][c]
                color_bg, color_fg = COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                self.cells[r][c].config(
                    text=str(value) if value != 0 else "",
                    bg=color_bg,
                    fg=color_fg,
                )
        self.score_label.config(text=f"Score: {self.score}")
        self.update_idletasks()

    def key_handler(self, event):
        key = event.keysym
        moves = {
            "Up": move_up,
            "Down": move_down,
            "Left": move_left,
            "Right": move_right
        }

        if key in moves:
            new_board, gained_score = moves[key](self.board)
            if new_board != self.board:
                self.board = new_board
                self.score += gained_score
                add_random_tile(self.board)
                self.update_GUI()
                if any(2048 in row for row in self.board):
                    self.game_over("🎉 You reached 2048! You win!")
                elif not can_move(self.board):
                    self.game_over("💀 Game Over! No moves left.")

    def game_over(self, message):
        popup = tk.Toplevel(self)
        popup.title("Game Over")
        tk.Label(popup, text=message, font=("Helvetica", 14, "bold")).pack(padx=20, pady=10)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    def restart(self):
        self.board = init_board(self.size)
        self.score = 0
        self.update_GUI()

# ---------- Run Game ----------
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    game.mainloop()
