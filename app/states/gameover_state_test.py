from types import SimpleNamespace
from app.states.game_state import GameState
from app.states.gameover_state import GameOverState
from app.states.statestack import StateStack


def test_return_key_restarts_the_level_the_player_lost_on(canvas):
    stack, window = StateStack(), SimpleNamespace(
        canvas=canvas, width=900, height=640)
    stack.push(GameState(stack, window, 3))
    stack.push(GameOverState(stack, window))
    stack.current.handle_key(SimpleNamespace(keysym="Return"))
    assert isinstance(
        stack.current, GameState) and stack.current.world.level_number == 3
