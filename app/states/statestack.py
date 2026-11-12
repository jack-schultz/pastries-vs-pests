from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.states.base_state import BaseState


class StateStack:
    def __init__(self) -> None:
        self._stack: list[BaseState] = []

    @property
    def current(self) -> BaseState | None:
        if not self._stack:
            return None
        return self._stack[-1]

    def push(self, state: BaseState) -> None:
        """Pause current state and push a new state on top (e.g., Pause Menu)."""
        if self.current:
            self.current.exit()
        self._stack.append(state)
        state.enter()

    def replace_all(self, state: BaseState) -> None:
        """Discard every state and start fresh with a new one (e.g., restart)."""
        self._stack.clear()
        self._stack.append(state)
        state.enter()

    def pop(self) -> None:
        """Remove the top state and resume the state underneath."""
        if self.current:
            self.current.exit()
            self._stack.pop()
        if self.current:
            self.current.enter()
