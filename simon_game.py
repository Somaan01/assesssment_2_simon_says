# I acknowledge the use of ChatGPT (Free version)
# to review my code files and add improvements features like sound and high score tracking

"""
Simon Says Game
--------------------------
All Features
- Difficulty Levels (Easy, Medium, Hard)
- Countdown timer for each round
- High Score Tracking
- Round Progress small bar
- Feedback sound
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import winsound


COLORS = ["red", "green", "blue", "yellow"]
COLOR_SOUNDS = {"red": 440, "green": 494, "blue": 523, "yellow": 587}
ROUND_DELAY = 1000


class SimonGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simon Says - Memory Game")
        self.master.geometry("520x600")
        self.master.resizable(False, False)

        self.sequence = []
        self.user_sequence = []
        self.round = 0
        self.is_playing = False
        self.countdown_value = 3
        self.highscore = self.load_highscore()

        # ---------- Header of GUI----------
        tk.Label(master, text="🎯 Simon Says", font=("Segoe UI", 22, "bold")).pack(pady=10)
        self.score_label = tk.Label(master, text="Round: 0", font=("Segoe UI", 14))
        self.score_label.pack()
        self.highscore_label = tk.Label(master, text=f"High Score: {self.highscore}", font=("Segoe UI", 12))
        self.highscore_label.pack(pady=2)

        # ---------- Difficulty Levels----------
        diff_frame = tk.Frame(master)
        diff_frame.pack(pady=10)
        tk.Label(diff_frame, text="Difficulty:", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=5)
        self.difficulty = tk.StringVar(value="Medium")
        tk.OptionMenu(diff_frame, self.difficulty, "Easy", "Medium", "Hard").pack(side=tk.LEFT)

        # ---------- Buttons Colors ----------
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)
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

        # ---------- Game Controls ----------
        control = tk.Frame(master)
        control.pack(pady=10)
        self.start_button = tk.Button(control, text="Start", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=10)
        self.reset_button = tk.Button(control, text="Reset", command=self.reset_game, state="disabled")
        self.reset_button.grid(row=0, column=1, padx=10)

        # ---------- Progress bar ----------
        self.progress = ttk.Progressbar(master, length=350, mode="determinate")
        self.progress.pack(pady=10)

        # ---------- Message label ----------
        self.message_label = tk.Label(master, text="Press Start to Begin!", font=("Segoe UI", 12))
        self.message_label.pack(pady=10)

        self.blink_label()

    # ------------------------------------------------------------
    # Utility Functions
    # ------------------------------------------------------------
    def get_delay(self):
        diff = self.difficulty.get()
        if diff == "Easy":
            return 700
        elif diff == "Hard":
            return 300
        return 500  # Medium

    def load_highscore(self):
        try:
            with open("highscore.txt") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_highscore(self):
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))
        except Exception:
            pass

    def blink_label(self):
        if not self.is_playing:
            cur = self.message_label.cget("text")
            new_text = "" if cur else "Press Start to Begin!"
            self.message_label.config(text=new_text)
        self.master.after(600, self.blink_label)

    # ------------------------------------------------------------
    # Game Logic
    # ------------------------------------------------------------
    def start_game(self):
        self.sequence.clear()
        self.user_sequence.clear()
        self.round = 0
        self.is_playing = True
        self.start_button.config(state="disabled")
        self.reset_button.config(state="normal")
        self.next_round()

    def reset_game(self):
        self.sequence.clear()
        self.user_sequence.clear()
        self.round = 0
        self.is_playing = False
        self.score_label.config(text="Round: 0")
        self.message_label.config(text="Game Reset. Press Start to Begin!")
        self.progress["value"] = 0
        self.start_button.config(state="normal")
        self.reset_button.config(state="disabled")
        self.disable_buttons()

    def next_round(self):
        self.round += 1
        self.user_sequence.clear()
        self.sequence.append(random.choice(COLORS))
        self.score_label.config(text=f"Round: {self.round}")
        self.message_label.config(text="Get ready...")
        self.disable_buttons()
        self.progress["maximum"] = len(self.sequence)
        self.progress["value"] = 0
        self.countdown(self.countdown_value)

    def countdown(self, n):
        if n == 0:
            self.message_label.config(text="Watch carefully!")
            self.play_sequence()
        else:
            self.message_label.config(text=f"Get ready... {n}")
            self.master.after(1000, lambda: self.countdown(n - 1))

    def play_sequence(self):
        delay = self.get_delay()
        for i, color in enumerate(self.sequence):
            self.master.after(i * delay, lambda c=color, step=i + 1: self.flash_button(c, step))
        total = len(self.sequence) * delay
        self.master.after(total + 400, self.enable_buttons)

    def flash_button(self, color, step=None):
        btn = self.buttons[color]
        original = btn["bg"]
        btn.config(bg="white")
        try:
            winsound.Beep(COLOR_SOUNDS[color], 200)
        except Exception:
            pass
        self.master.after(250, lambda: btn.config(bg=original))
        if step:
            self.progress["value"] = step
            self.master.update_idletasks()

    def enable_buttons(self):
        for b in self.buttons.values():
            b.config(state="normal")
        self.message_label.config(text="Your turn! Repeat the sequence.")

    def disable_buttons(self):
        for b in self.buttons.values():
            b.config(state="disabled")

    def user_click(self, color):
        if not self.is_playing:
            return
        self.user_sequence.append(color)
        self.flash_button(color)
        index = len(self.user_sequence) - 1
        if self.user_sequence[index] != self.sequence[index]:
            self.game_over()
            return
        if len(self.user_sequence) == len(self.sequence):
            self.disable_buttons()
            self.message_label.config(text="✅ Correct! Get ready for the next round...")
            self.master.after(ROUND_DELAY, self.next_round)

    def game_over(self):
        self.is_playing = False
        self.disable_buttons()
        if self.round > self.highscore:
            self.highscore = self.round
            self.highscore_label.config(text=f"High Score: {self.highscore}")
            self.save_highscore()
        messagebox.showinfo("Game Over", f"You reached Round {self.round}!")
        self.message_label.config(text="❌ Game Over! Press Start to play again.")
        self.start_button.config(state="normal")
        self.reset_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    SimonGame(root)
    root.mainloop()

