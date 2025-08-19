import tkinter as tk
import numpy as np
from typing import Optional, Tuple

# Symbols
HUMAN = 1   # X
AI = -1     # O
EMPTY = 0

SYMBOL = {HUMAN: 'X', AI: 'O', EMPTY: ' '}


def new_board() -> np.ndarray:
    return np.zeros((3, 3), dtype=int)


def winner(board: np.ndarray) -> Optional[int]:
    # Row/col sums
    sums = np.concatenate([board.sum(axis=0), board.sum(axis=1)])
    if 3 in sums:
        return HUMAN
    if -3 in sums:
        return AI
    # Diagonals
    diag1 = np.trace(board)
    diag2 = np.trace(np.fliplr(board))
    if diag1 == 3 or diag2 == 3:
        return HUMAN
    if diag1 == -3 or diag2 == -3:
        return AI
    return None


def moves(board: np.ndarray):
    return list(zip(*np.where(board == EMPTY)))


def is_full(board: np.ndarray) -> bool:
    return not (board == EMPTY).any()


def game_over(board: np.ndarray) -> bool:
    return winner(board) is not None or is_full(board)


def score(board: np.ndarray, depth: int) -> int:
    w = winner(board)
    if w == AI:
        return 10 - depth
    if w == HUMAN:
        return depth - 10
    return 0


def minimax(board: np.ndarray, player: int, depth: int, alpha: int, beta: int):
    if game_over(board):
        return score(board, depth), None

    best_move = None

    if player == AI:
        best_val = -999
        for r, c in moves(board):
            board[r, c] = AI
            val, _ = minimax(board, HUMAN, depth + 1, alpha, beta)
            board[r, c] = EMPTY
            if val > best_val:
                best_val, best_move = val, (r, c)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = 999
        for r, c in moves(board):
            board[r, c] = HUMAN
            val, _ = minimax(board, AI, depth + 1, alpha, beta)
            board[r, c] = EMPTY
            if val < best_val:
                best_val, best_move = val, (r, c)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best_val, best_move


def ai_move(board: np.ndarray) -> Tuple[int, int]:
    if board.sum() == 0 and board[1, 1] == EMPTY:
        return (1, 1)  # pick center first move
    _, move = minimax(board, AI, 0, -999, 999)
    assert move is not None
    return move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - NumPy + Tkinter")
        self.board = new_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.turn = HUMAN
        self.status = tk.Label(self.root, text="You are X. AI is O.", font=("Arial", 14))
        self.status.grid(row=3, column=0, columnspan=3, pady=10)
        self.play_again_btn = tk.Button(self.root, text="Play Again", font=("Arial", 12),
                                        command=self.reset_game)
        self.play_again_btn.grid(row=4, column=0, columnspan=3, pady=10)
        self.play_again_btn.grid_remove()  # hidden until game ends
        self.build_grid()

    def build_grid(self):
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.root, text=" ", font=("Arial", 24),
                                 width=5, height=2,
                                 command=lambda r=r, c=c: self.human_move(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def update_ui(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = SYMBOL[self.board[r, c]]

    def human_move(self, r, c):
        if self.board[r, c] == EMPTY and not game_over(self.board) and self.turn == HUMAN:
            self.board[r, c] = HUMAN
            self.update_ui()
            if not game_over(self.board):
                self.turn = AI
                self.root.after(500, self.ai_turn)
            else:
                self.show_result()

    def ai_turn(self):
        if not game_over(self.board):
            r, c = ai_move(self.board)
            self.board[r, c] = AI
            self.update_ui()
            self.turn = HUMAN
        if game_over(self.board):
            self.show_result()

    def show_result(self):
        w = winner(self.board)
        if w == HUMAN:
            self.status.config(text="🎉 You win!")
        elif w == AI:
            self.status.config(text="🤖 AI wins!")
        else:
            self.status.config(text="🤝 It's a draw.")
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["state"] = "disabled"
        self.play_again_btn.grid()  # show button

    def reset_game(self):
        self.board = new_board()
        self.turn = HUMAN
        self.status.config(text="You are X. AI is O.")
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = " "
                self.buttons[r][c]["state"] = "normal"
        self.play_again_btn.grid_remove()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
