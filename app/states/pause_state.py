from __future__ import annotations
from app.states.base_state import BaseState
from app.rectangle import Rectangle
import tkinter as tk


class PauseState(BaseState):
    def __init__(self, state_stack, window):
        super().__init__(state_stack, window)
        self.__buttons: dict[str, Rectangle] = {}

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Escape":
            self.state_stack.pop()

    def enter(self) -> None:
        canvas = self.window.canvas
        # Draw pause text with a tag for deletion on exit
        canvas.create_text(
            self.window.width // 2, 170, text="PAUSED",
            font=("Arial", 36, "bold"), fill="#3d405b", tags="pause_ui"
        )
        for i, (name, label) in enumerate(
            [
                ("resume", "Resume"), ("restart", "Restart"),
                ("level_select", "Level Select"), ("main_menu", "Main Menu")
            ]
        ):
            button = Rectangle(canvas, 350, 230 + i * 85, 200, 70, "#3d405b")
            button.set_text(label, colour="#ffffff", size=16)
            self.__buttons[name] = button

    def handle_click(self, event: tk.Event) -> None:
        pos = (event.x, event.y)
        if self.__buttons["resume"].collide_point(pos):
            self.state_stack.pop()
        elif self.__buttons["restart"].collide_point(pos):
            from app.states.game_state import GameState
            # The game state sits at the bottom of the stack; restart its current level
            level = self.state_stack.bottom.world.level_number
            self.window.canvas.delete("all")
            self.state_stack.replace_all(GameState(self.state_stack, self.window, level))
        elif self.__buttons["level_select"].collide_point(pos):
            # Imported here to avoid circular imports between states
            from app.states.levelselect_state import LevelSelectState
            self.state_stack.replace_all(LevelSelectState(self.state_stack, self.window))
        elif self.__buttons["main_menu"].collide_point(pos):
            from app.states.mainmenu_state import MainMenuState
            self.state_stack.replace_all(MainMenuState(self.state_stack, self.window))

    def exit(self):
        self.window.canvas.delete("pause_ui")
        for button in self.__buttons.values():
            button.delete()
        self.__buttons.clear()
