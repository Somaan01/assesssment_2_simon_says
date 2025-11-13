"""
Simon Says Game - Base GUI
--------------------------
Creating the Tkinter GridBox with 4 Color Boxes.
"""
import tkinter as tk

class SimonGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simon Says")
        self.master.geometry("400x450")
        self.master.resizable(False, False)

        tk.Label(master, text="Simon Says", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        colors = ["red", "green", "blue", "yellow"]
        self.buttons = {}

        for i, color in enumerate(colors):
            btn = tk.Button(
                self.frame,
                bg=color,
                width=15,
                height=6,
                state="disabled"
            )
            row, col = divmod(i, 2)
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons[color] = btn


if __name__ == "__main__":
    root = tk.Tk()
    SimonGame(root)
    root.mainloop()
