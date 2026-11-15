from entities.flour import Flour


def test_keeps_its_amount_and_is_not_moving_yet(canvas):
    flour = Flour(canvas, 100, 100, 25)
    assert flour.amount == 25
    assert not flour.finished_move()


def test_clicked_flour_flies_to_its_destination(canvas):
    flour = Flour(canvas, 100, 100, 25)
    flour.click((0, 0))
    for _ in range(300):
        flour.move()
    assert flour.finished_move()
