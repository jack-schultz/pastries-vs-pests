from types import SimpleNamespace
from app.states.game_state import GameState
from app.states.gameover_state import GameOverState
from app.states.statestack import StateStack
from app.world import World
from entities.flour import Flour


def make_state(canvas):
    stack = StateStack()
    # Only the parts of the window a state uses.
    state = GameState(stack, SimpleNamespace(
        canvas=canvas, width=900, height=640))
    stack.push(state)
    return state


def event(x=0, y=0, keysym=""):
    return SimpleNamespace(x=x, y=y, keysym=keysym)


def tile_at(state, index):
    return state.world.garden.tiles[index]


def click_on(state, rect_owner):
    x, y = rect_owner.rect.centre
    state.handle_click(event(x, y))


def select(state, name):
    card = next(c for c in state.world.card_holder.cards if c.name == name)
    click_on(state, card)
    return card


def recharge(card):
    while not card.is_ready:
        card.tick_cooldown()


def test_game_over_pushes_game_over_state(canvas, monkeypatch):
    state = make_state(canvas)
    monkeypatch.setattr(World, "game_over", property(lambda self: True))
    state.tick()
    assert isinstance(state.state_stack.current, GameOverState)


def test_escape_again_resumes_the_game(canvas):
    state = make_state(canvas)
    state.handle_key(event(keysym="Escape"))
    state.state_stack.current.handle_key(event(keysym="Escape"))
    assert state.state_stack.current is state


def test_click_selected_card_deselects_it(canvas):
    state = make_state(canvas)
    card = select(state, "Flour Flower")
    click_on(state, card)
    assert state.world.card_holder.selected_card is None


def test_cannot_select_a_card_that_costs_too_much(canvas):
    state = make_state(canvas)
    # It costs 150 but the player has only 75 flour.
    select(state, "Profiterole")
    assert state.world.card_holder.selected_card is None


def test_cannot_place_on_occupied_tile(canvas):
    state = make_state(canvas)
    state.world.flour = 1000
    tile = tile_at(state, 0)
    select(state, "Flour Flower")
    click_on(state, tile)
    original = tile.good

    select(state, "Popping Candy")
    click_on(state, tile)
    assert tile.good is original
    assert state.world.flour == 950
    assert state.world.card_holder.selected_card is None


def test_replacing_costs_the_replace_price(canvas):
    state = make_state(canvas)
    state.world.flour = 1000
    tile = tile_at(state, 0)
    shooter_card = select(state, "Sugar Shooter")
    click_on(state, tile)
    assert state.world.flour == 900

    recharge(shooter_card)
    select(state, "Sugar Shooter")
    click_on(state, tile)
    assert state.world.flour == 700


def test_bin_starts_cooldown_after_removing(canvas):
    state = make_state(canvas)
    tile = tile_at(state, 0)
    select(state, "Flour Flower")
    click_on(state, tile)

    bin_card = select(state, "Bin")
    click_on(state, tile)
    assert not bin_card.is_ready
    assert state.world.card_holder.selected_card is None


def test_glove_drops_good_on_an_empty_tile(canvas):
    state = make_state(canvas)
    state.world.flour = 1000
    origin, target = tile_at(state, 0), tile_at(state, 1)
    select(state, "Flour Flower")
    click_on(state, origin)
    good = origin.good

    select(state, "Glove")
    click_on(state, origin)
    click_on(state, target)
    assert target.good is good
    assert origin.is_empty
    assert not state.world.is_holding


def test_glove_returns_good_to_its_own_tile_for_free(canvas):
    state = make_state(canvas)
    state.world.flour = 1000
    origin = tile_at(state, 0)
    select(state, "Flour Flower")
    click_on(state, origin)
    good = origin.good
    flour_after_placing = state.world.flour

    glove = select(state, "Glove")
    click_on(state, origin)
    click_on(state, origin)
    assert origin.good is good
    assert not state.world.is_holding
    assert state.world.flour == flour_after_placing
    assert glove.is_ready
    assert state.world.card_holder.selected_card is None


def test_click_next_button_does_not_hit_tiles_underneath(canvas, monkeypatch):
    monkeypatch.setattr(World, "clicked_next_button", lambda self, pos: True)
    monkeypatch.setattr(World, "start_next_level", lambda self: None)
    state = make_state(canvas)
    state.world.flour = 1000
    select(state, "Flour Flower")
    tile = tile_at(state, 0)
    click_on(state, tile)
    assert tile.is_empty


def test_hovering_flour_collects_it(canvas):
    state = make_state(canvas)
    flour = Flour(canvas, 300, 300, 25)
    state.world.add_goods([flour])
    state.handle_motion(event(300, 300))
    for _ in range(300):
        state.world.update_flour()
    assert state.world.flour == 100


def test_preview_is_white_when_affordable(canvas):
    state = make_state(canvas)
    select(state, "Flour Flower")
    x, y = tile_at(state, 0).rect.centre
    state.handle_motion(event(x, y))
    item = state._GameState__cost_preview
    assert canvas.itemcget(item, "fill") == "#ffffff"
