from entities.entity import Entity


def test_owns_a_rect_at_the_given_position(canvas):
    entity = Entity(canvas, 10, 20, 30, 40, "#ffffff")
    assert (entity.rect.left, entity.rect.top, entity.rect.w) == (10, 20, 30)
    assert entity.canvas is canvas


def test_destroy_removes_it_from_the_canvas(canvas):
    entity = Entity(canvas, 10, 20, 30, 40, "#ffffff")
    entity.destroy()
    assert not canvas.find_all()
