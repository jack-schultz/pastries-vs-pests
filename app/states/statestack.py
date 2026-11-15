from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.states.base_state import BaseState


class StateStack:
    """Keeps a stack of states; the top state is the active one."""

    def __init__(self) -> None:
        self.__stack: list[BaseState] = []

    @property
    def current(self) -> BaseState | None:
        if not self.__stack:
            return None
        return self.__stack[-1]

    @property
    def bottom(self) -> BaseState | None:
        if not self.__stack:
            return None
        return self.__stack[0]

    def push(self, state: BaseState) -> None:
        """Pause current state and push a new state on top (e.g., Pause Menu)."""
        if self.current:
            self.current.exit()
        self.__stack.append(state)
        state.enter()

    def replace_all(self, state: BaseState) -> None:
        """Discard every state and start fresh with a new one (e.g., restart)."""
        self.__stack.clear()
        self.__stack.append(state)
        state.enter()

    def pop(self) -> None:
        """Remove the top state and resume the state underneath."""
        if self.current:
            self.current.exit()
            self.__stack.pop()
        if self.current:
            self.current.enter()
