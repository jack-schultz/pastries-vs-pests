from abc import ABC, abstractmethod
import tkinter as tk


class BaseState(ABC):
    """Base class for all game states (menu, game, pause)."""

    def __init__(self, state_stack, window):
        self.__state_stack = state_stack
        self.__window = window

    @property
    def state_stack(self):
        return self.__state_stack

    @property
    def window(self):
        return self.__window

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

    def handle_motion(self, event: tk.Event) -> None:
        """Called when the mouse moves over the canvas."""
        pass

    def handle_key(self, event: tk.Event) -> None:
        """Called when a key is pressed."""
        pass
