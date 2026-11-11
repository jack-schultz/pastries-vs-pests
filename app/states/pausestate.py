from app.states.basestate import BaseState
import tkinter as tk


class PauseState(BaseState):
    def __init__(self, state_stack, window):
        super().__init__(state_stack, window)

    def handle_key(self, event: tk.Event) -> None:
        if event.keysym == "Escape":
            self.state_stack.pop()

    def enter(self) -> None:
        # Draw pause text with a tag for deletion on exit
        self.window.canvas.create_text(
            400, 300, text="PAUSED (Press Esc to Resume)",
            font=("Arial", 24), fill="white", tags="pause_ui"
        )

    def exit(self):
        self.window.canvas.delete("pause_ui")
