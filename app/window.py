from __future__ import annotations
import tkinter as tk
from app.states.mainmenu_state import MainMenuState
from app.states.statestack import StateStack


class Window:
    # Holds the Tk window and the canvas everything is drawn on
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Pastries vs. Pests")
        self.root.resizable(False, False)

        self.width, self.height = (900, 600)

        # Create the world canvas to store our rects coordinates
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#fdf3e1", highlightthickness=0)
        # Places canvas widget inside parent window as tk is designed for menus so it needs this
        self.canvas.pack()

        self.state_stack = StateStack()
        self.state_stack.push(MainMenuState(self.state_stack, self))

        # Bind inputs once globally and route to the active state
        self.canvas.bind("<Button-1>", self.__on_click)
        self.canvas.bind("<Motion>", self.__on_motion)
        self.root.bind("<Key>", self.__on_key)

    def __on_click(self, event: tk.Event) -> None:
        if self.state_stack.current:
            self.state_stack.current.handle_click(event)

    def __on_motion(self, event: tk.Event) -> None:
        if self.state_stack.current:
            self.state_stack.current.handle_motion(event)

    def __on_key(self, event: tk.Event) -> None:
        if self.state_stack.current:
            self.state_stack.current.handle_key(event)

    def _tick(self) -> None:
        if self.state_stack.current:
            self.state_stack.current.tick()
        self.root.after(16, self._tick)  # ~60 FPS

    def run(self) -> None:
        self._tick()
        self.root.mainloop()
