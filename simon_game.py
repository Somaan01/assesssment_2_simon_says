"""
Simon Says Game - Base GUI
--------------------------
Adding rounds, scores buttons
"""

import tkinter as tk
import random
from tkinter import messagebox

COLORS = ["red", "green", "blue", "yellow"]
FLASH_DELAY = 500
ROUND_DELAY = 1000


class SimonGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simon Says")
        self.master.geometry("420x500")

        tk.Label(master, text="Simon Says", font=("Segoe UI", 20, "bold")).pack(pady=10)
        self.score_label = tk.Label(master, text="Round: 0", font=("Segoe UI", 14))
        self.score_label.pack(pady=5)

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.sequence = []
        self.user_sequence = []
        self.round = 0

        self.buttons = {}
        for i, color in enumerate(COLORS):
            btn = tk.Button(
                self.frame,
                bg=color,
                width=15,
                height=6,
                command=lambda c=color: self.user_click(c),
                state="disabled"
            )
            row, col = divmod(i, 2)
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons[color] = btn

        control = tk.Frame(master)
        control.pack(pady=10)
        self.start_button = tk.Button(control, text="Start", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=10)
        self.reset_button = tk.Button(control, text="Reset", command=self.reset_game, state="disabled")
        self.reset_button.grid(row=0, column=1, padx=10)

        self.message_label = tk.Label(master, text="Press Start to Begin!", font=("Segoe UI", 12))
        self.message_label.pack(pady=10)

    def start_game(self):
        self.sequence.clear()
        self.user_sequence.clear()
        self.round = 0
        self.start_button.config(state="disabled")
        self.reset_button.config(state="normal")
        self.next_round()

    def reset_game(self):
        self.sequence.clear()
        self.user_sequence.clear()
        self.round = 0
        self.score_label.config(text="Round: 0")
        self.message_label.config(text="Game Reset. Press Start.")
        self.start_button.config(state="normal")
        self.reset_button.config(state="disabled")
        self.disable_buttons()

    def next_round(self):
        self.round += 1
        self.user_sequence.clear()
        self.sequence.append(random.choice(COLORS))
        self.score_label.config(text=f"Round: {self.round}")
        self.message_label.config(text="Watch the sequence...")
        self.disable_buttons()
        self.play_sequence()

    def play_sequence(self):
        for i, color in enumerate(self.sequence):
            self.master.after(i * FLASH_DELAY, lambda c=color: self.flash_button(c))
        total_time = len(self.sequence) * FLASH_DELAY
        self.master.after(total_time + 400, self.enable_buttons)

    def flash_button(self, color):
        btn = self.buttons[color]
        original = btn["bg"]
        btn.config(bg="white")
        self.master.after(250, lambda: btn.config(bg=original))

    def enable_buttons(self):
        for b in self.buttons.values():
            b.config(state="normal")
        self.message_label.config(text="Your turn!")

    def disable_buttons(self):
        for b in self.buttons.values():
            b.config(state="disabled")

    def user_click(self, color):
        self.user_sequence.append(color)
        self.flash_button(color)

        index = len(self.user_sequence) - 1
        if self.user_sequence[index] != self.sequence[index]:
            self.game_over()
            return

        if len(self.user_sequence) == len(self.sequence):
            self.disable_buttons()
            self.message_label.config(text="Good job!")
            self.master.after(ROUND_DELAY, self.next_round)

    def game_over(self):
        messagebox.showinfo("Game Over", f"You reached Round {self.round}!")
        self.disable_buttons()
        self.message_label.config(text="Game Over! Press Start.")
        self.start_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    SimonGame(root)
    root.mainloop()

