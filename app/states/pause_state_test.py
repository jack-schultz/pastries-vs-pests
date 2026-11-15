from types import SimpleNamespace
from app.states.game_state import GameState
from app.states.pause_state import PauseState
from app.states.statestack import StateStack


def test_escape_resumes_the_game(canvas):
    stack, window = StateStack(), SimpleNamespace(canvas=canvas, width=900, height=640)
    game = GameState(stack, window)
    stack.push(game)
    stack.push(PauseState(stack, window))
    stack.current.handle_key(SimpleNamespace(keysym="Escape"))
    assert stack.current is game
