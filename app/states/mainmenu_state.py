from __future__ import annotations
import tkinter as tk
from app.states.base_state import BaseState
from app.rectangle import Rectangle


class MainMenuState(BaseState):
    def __init__(self, state_stack, window) -> None:
        super().__init__(state_stack, window)
        self.__play_button: Rectangle | None = None
        self.__quit_button: Rectangle | None = None

    def enter(self) -> None:
        canvas = self.window.canvas
        canvas.delete("all")
        canvas.create_text(
            self.window.width // 2, 160, text="Pastries vs. Pests",
            font=("Arial", 48, "bold"), fill="#3d405b",
        )
        self.__play_button = Rectangle(canvas, 350, 280, 200, 70, "#3d405b")
        self.__play_button.set_text("Play", colour="#ffffff", size=18)
        self.__quit_button = Rectangle(canvas, 350, 380, 200, 70, "#b00020")
        self.__quit_button.set_text("Quit", colour="#ffffff", size=18)

    def handle_click(self, event: tk.Event) -> None:
        pos = (event.x, event.y)
        if self.__play_button and self.__play_button.collide_point(pos):
            self.open_level_select()
        elif self.__quit_button and self.__quit_button.collide_point(pos):
            self.window.root.destroy()

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Return":
            self.open_level_select()

    def open_level_select(self) -> None:
        # Imported here to avoid circular imports between states
        from app.states.levelselect_state import LevelSelectState
        self.state_stack.replace_all(LevelSelectState(self.state_stack, self.window))
