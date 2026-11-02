from __future__ import annotations
import tkinter as tk


class Window:
    # Holds the Tk window and the canvas everything is drawn on
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bakery vs. Pests")
        self.root.resizable(False, False)

        self.width, self.height = (900, 600)

        # Create the world canvas to store our rects coordinates
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#fdf3e1", highlightthickness=0)
        # Places canvas widget inside parent window as tk is designed for menus so it needs this
        self.canvas.pack()

    def run(self) -> None:
        self.root.mainloop()
