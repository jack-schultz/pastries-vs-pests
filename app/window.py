from __future__ import annotations
import tkinter as tk
from app.states.mainmenu_state import MainMenuState
from app.states.statestack import StateStack


class Window:
    """Holds the Tk window and the canvas everything is drawn on"""
    def __init__(self) -> None:
        self.__root = tk.Tk()
        self.__root.title("Pastries vs. Pests")
        self.__root.resizable(False, False)

        self.__width, self.__height = (900, 640)

        # Create the world canvas to store our rects coordinates
        self.__canvas = tk.Canvas(self.__root, width=self.__width, height=self.__height, bg="#fdf3e1", highlightthickness=0)
        # Places canvas widget inside parent window as tk is designed for menus so it needs this
        self.__canvas.pack()

        self.__state_stack = StateStack()
        self.__state_stack.push(MainMenuState(self.__state_stack, self))

        # Bind inputs once globally and route to the active state
        self.__canvas.bind("<Button-1>", self.__on_click)
        self.__canvas.bind("<Motion>", self.__on_motion)
        self.__root.bind("<Key>", self.__on_key)

    @property
    def root(self) -> tk.Tk:
        return self.__root

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def canvas(self) -> tk.Canvas:
        return self.__canvas

    def __on_click(self, event: tk.Event) -> None:
        if self.__state_stack.current:
            self.__state_stack.current.handle_click(event)

    def __on_motion(self, event: tk.Event) -> None:
        if self.__state_stack.current:
            self.__state_stack.current.handle_motion(event)

    def __on_key(self, event: tk.Event) -> None:
        if self.__state_stack.current:
            self.__state_stack.current.handle_key(event)

    def _tick(self) -> None:
        if self.__state_stack.current:
            self.__state_stack.current.tick()
        self.__root.after(16, self._tick)  # ~60 FPS

    def run(self) -> None:
        self._tick()
        self.__root.mainloop()
