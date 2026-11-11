from abc import ABC, abstractmethod
import tkinter as tk


class BaseState(ABC):
    def __init__(self, state_stack, window):
        self.state_stack = state_stack
        self.window = window

    def tick(self) -> None:
        """Called every frame by the main window loop."""
        pass

    def enter(self) -> None:
        """Called when this state becomes the active state on top of the stack."""
        pass

    def exit(self) -> None:
        """Called when this state is popped or covered by another state."""
        pass

    def handle_click(self, event: tk.Event) -> None:
        """Called when the mouse is clicked."""
        pass

    def handle_key(self, event: tk.Event) -> None:
        """Called when a key is pressed."""
        pass
