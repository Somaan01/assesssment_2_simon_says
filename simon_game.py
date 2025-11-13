"""
Simon Says Game - Base GUI
--------------------------
Adding loop and player implementation click and round progression
"""

import tkinter as tk
import random
from tkinter import messagebox

COLORS = ["red", "green", "blue", "yellow"]
FLASH_DELAY = 500


class SimonGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simon Says")
        self.master.geometry("400x450")

        tk.Label(master, text="Simon Says", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.sequence = []
        self.user_sequence = []

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

        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        self.sequence.clear()
        self.user_sequence.clear()
        self.next_round()

    def next_round(self):
        self.user_sequence.clear()
        self.sequence.append(random.choice(COLORS))
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
        self.master.after(300, lambda: btn.config(bg=original))

    def enable_buttons(self):
        for b in self.buttons.values():
            b.config(state="normal")

    def disable_buttons(self):
        for b in self.buttons.values():
            b.config(state="disabled")

    def user_click(self, color):
        self.user_sequence.append(color)
        self.flash_button(color)

        index = len(self.user_sequence) - 1
        if self.user_sequence[index] != self.sequence[index]:
            messagebox.showinfo("Game Over", f"You reached Round {len(self.sequence)}!")
            self.disable_buttons()
            return

        if len(self.user_sequence) == len(self.sequence):
            self.disable_buttons()
            self.master.after(1000, self.next_round)


if __name__ == "__main__":
    root = tk.Tk()
    SimonGame(root)
    root.mainloop()

