from app.window import Window


def test_window_has_the_game_size():
    window = Window()
    assert (window.width, window.height) == (900, 640)
    window.root.destroy()
