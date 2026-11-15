from app.states.base_state import BaseState
from app.states.statestack import StateStack


def test_pop_resumes_the_state_underneath():
    stack = StateStack()
    first, second = BaseState(None, None), BaseState(None, None)
    stack.push(first)
    stack.push(second)
    assert stack.current is second
    stack.pop()
    assert stack.current is first
