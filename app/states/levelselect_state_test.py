from types import SimpleNamespace
import pytest
from app.states.game_state import GameState
from app.states.levelselect_state import LevelSelectState
from app.states.mainmenu_state import MainMenuState
from app.states.statestack import StateStack


@pytest.fixture
def state(canvas):
    stack = StateStack()
    level_select = LevelSelectState(
        stack, SimpleNamespace(canvas=canvas, width=900, height=640))
    stack.push(level_select)
    return level_select


def test_clicking_a_level_starts_it(state):
    x, y = state._LevelSelectState__level_buttons[3].centre
    state.handle_click(SimpleNamespace(x=x, y=y))
    assert isinstance(state.state_stack.current, GameState)
    assert state.state_stack.current.world.level_number == 3


@pytest.mark.parametrize("handler, event", [
    ("handle_click", SimpleNamespace(x=70, y=40)),
    ("handle_key", SimpleNamespace(keysym="Escape")),
])
def test_back_button_and_escape_return_to_menu(state, handler, event):
    getattr(state, handler)(event)
    assert isinstance(state.state_stack.current, MainMenuState)
