from types import SimpleNamespace
from app.states.levelselect_state import LevelSelectState
from app.states.mainmenu_state import MainMenuState
from app.states.statestack import StateStack


def test_return_key_opens_level_select(canvas):
    stack = StateStack()
    stack.push(MainMenuState(stack, SimpleNamespace(canvas=canvas, width=900, height=640)))
    stack.current.handle_key(SimpleNamespace(keysym="Return"))
    assert isinstance(stack.current, LevelSelectState)
