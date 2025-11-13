"""
Simon Says Game - Base GUI
--------------------------
Adding Random Color Sequence generator and animation
"""
import tkinter as tk
import random

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

        self.buttons = {}
        for i, color in enumerate(COLORS):
            btn = tk.Button(
                self.frame,
                bg=color,
                width=15,
                height=6
            )
            row, col = divmod(i, 2)
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons[color] = btn

        self.sequence = []
        self.start_button = tk.Button(master, text="Start", command=self.next_round)
        self.start_button.pack(pady=10)

    def next_round(self):
        self.sequence.append(random.choice(COLORS))
        self.play_sequence()

    def play_sequence(self):
        for i, color in enumerate(self.sequence):
            self.master.after(i * FLASH_DELAY, lambda c=color: self.flash_button(c))

    def flash_button(self, color):
        btn = self.buttons[color]
        original = btn["bg"]
        btn.config(bg="white")
        self.master.after(300, lambda: btn.config(bg=original))


if __name__ == "__main__":
    root = tk.Tk()
    SimonGame(root)
    root.mainloop()
