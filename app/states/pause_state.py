from __future__ import annotations
from app.states.base_state import BaseState
from app.rectangle import Rectangle
import tkinter as tk


class PauseState(BaseState):
    def __init__(self, state_stack, window):
        super().__init__(state_stack, window)
        self.buttons: dict[str, Rectangle] = {}

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
                [("resume", "Resume"), ("level_select", "Level Select"), ("main_menu", "Main Menu")]):
            button = Rectangle(canvas, 350, 240 + i * 90, 200, 70, "#3d405b")
            button.set_text(label, colour="#ffffff", size=16)
            self.buttons[name] = button

    def handle_click(self, event: tk.Event) -> None:
        pos = (event.x, event.y)
        if self.buttons["resume"].collide_point(pos):
            self.state_stack.pop()
        elif self.buttons["level_select"].collide_point(pos):
            # Imported here to avoid circular imports between states
            from app.states.levelselect_state import LevelSelectState
            self.state_stack.replace_all(LevelSelectState(self.state_stack, self.window))
        elif self.buttons["main_menu"].collide_point(pos):
            from app.states.mainmenu_state import MainMenuState
            self.state_stack.replace_all(MainMenuState(self.state_stack, self.window))

    def exit(self):
        self.window.canvas.delete("pause_ui")
        for button in self.buttons.values():
            button.delete()
        self.buttons.clear()
