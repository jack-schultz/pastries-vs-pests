from app.states.base_state import BaseState


def test_keeps_its_state_stack_and_window():
    stack, window = object(), object()
    state = BaseState(stack, window)
    assert state.state_stack is stack and state.window is window
