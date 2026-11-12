from __future__ import annotations
import tkinter as tk
from app.states.base_state import BaseState
from app.rectangle import Rectangle


class GameOverState(BaseState):
    def __init__(self, state_stack, window) -> None:
        super().__init__(state_stack, window)
        self.restart_button: Rectangle | None = None
        self.title = None

    def enter(self) -> None:
        canvas = self.window.canvas
        self.title = canvas.create_text(
            self.window.width // 2, 220, text="GAME OVER\nThe pests got in!",
            font=("Arial", 32, "bold"), fill="#b00020",
        )
        self.restart_button = Rectangle(canvas, 350, 300, 200, 70, "#3d405b")
        self.restart_button.set_text("Restart", colour="#ffffff", size=16)

    def handle_click(self, event: tk.Event) -> None:
        if self.restart_button and self.restart_button.collide_point((event.x, event.y)):
            self.restart()

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Return":
            self.restart()

    def restart(self) -> None:
        # Imported here to avoid a circular import with GameState
        from app.states.game_state import GameState
        # Restart on the level the player lost on
        level = self.state_stack._stack[0].world.level_number
        self.window.canvas.delete("all")
        self.state_stack.replace_all(GameState(self.state_stack, self.window, level))
