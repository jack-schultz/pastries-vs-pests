from __future__ import annotations
import tkinter as tk
from app.states.base_state import BaseState
from app.rectangle import Rectangle
from levels.level_collector import LevelCollector


class LevelSelectState(BaseState):
    """
    Displays a grid of playable levels to select from
    """
    def __init__(self, state_stack, window) -> None:
        super().__init__(state_stack, window)
        self.__level_buttons: dict[int, Rectangle] = {}
        self.__back_button: Rectangle | None = None

        self.__columns = 5
        self.__button_size = 100
        self.__gap = 30

    def enter(self) -> None:
        canvas = self.window.canvas
        canvas.delete("all")
        canvas.create_text(
            self.window.width // 2, 90, text="Select Level",
            font=("Arial", 36, "bold"), fill="#3d405b",
        )

        level_count = LevelCollector().level_count()
        row_width = self.__columns * self.__button_size + (self.__columns - 1) * self.__gap
        start_x = (self.window.width - row_width) // 2
        for i in range(level_count):
            level = i + 1
            col, row = i % self.__columns, i // self.__columns
            x_position = start_x + col * (self.__button_size + self.__gap)
            y_position = 180 + row * (self.__button_size + self.__gap)
            button = Rectangle(canvas, x_position, y_position, self.__button_size, self.__button_size, "#3d405e")
            button.set_text(str(level), colour="#ffffff", size=24)
            self.__level_buttons[level] = button

        self.__back_button = Rectangle(canvas, 20, 20, 100, 45, "#81796d")
        self.__back_button.set_text("Back", colour="#ffffff", size=12)

    def handle_click(self, event: tk.Event) -> None:
        pos = (event.x, event.y)
        if self.__back_button and self.__back_button.collide_point(pos):
            self.back_to_menu()
            return
        for level, button in self.__level_buttons.items():
            if button.collide_point(pos):
                self.start_level(level)
                return

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Escape":
            self.back_to_menu()

    def back_to_menu(self) -> None:
        from app.states.mainmenu_state import MainMenuState
        self.state_stack.replace_all(MainMenuState(self.state_stack, self.window))

    def start_level(self, level: int) -> None:
        from app.states.game_state import GameState
        self.window.canvas.delete("all")
        self.state_stack.replace_all(GameState(self.state_stack, self.window, level))
