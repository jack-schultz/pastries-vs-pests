import pytest
from app.rectangle import Rectangle


@pytest.fixture
def rect(canvas):
    return Rectangle(canvas, 10, 20, 100, 50, "red")


def test_rect_is_created_at_given_position_and_size(rect):
    assert rect.left == 10
    assert rect.top == 20
    assert rect.right == 110
    assert rect.bottom == 70
    assert rect.width == 100
    assert rect.height == 50


def test_rect_is_filled_with_colour(canvas, rect):
    assert canvas.itemcget(rect._Rectangle__rect, "fill") == "red"


def test_rect_exposes_its_canvas(canvas, rect):
    assert rect.canvas is canvas


def test_set_colour_changes_fill(canvas, rect):
    rect.set_colour("blue")
    assert canvas.itemcget(rect._Rectangle__rect, "fill") == "blue"


def test_set_outline_changes_outline_and_width(canvas, rect):
    rect.set_outline("black", width=3)
    assert canvas.itemcget(rect._Rectangle__rect, "outline") == "black"
    assert canvas.itemcget(rect._Rectangle__rect, "width") == "3.0"


def test_set_outline_defaults_to_width_one(canvas, rect):
    rect.set_outline("black")
    assert canvas.itemcget(rect._Rectangle__rect, "width") == "1.0"


def test_set_text_creates_label_at_centre(canvas, rect):
    rect.set_text("Flour")
    text_items = canvas.find_withtag(rect._Rectangle__tag)
    texts = [i for i in text_items if canvas.type(i) == "text"]
    assert len(texts) == 1
    assert canvas.itemcget(texts[0], "text") == "Flour"
    assert canvas.coords(texts[0]) == [60.0, 45.0]


def test_set_text_again_updates_existing_label(canvas, rect):
    rect.set_text("Flour")
    rect.set_text("Sugar", colour="white")
    texts = [i for i in canvas.find_withtag(
        rect._Rectangle__tag) if canvas.type(i) == "text"]
    assert len(texts) == 1
    assert canvas.itemcget(texts[0], "text") == "Sugar"
    assert canvas.itemcget(texts[0], "fill") == "white"


def test_label_follows_rect_when_moved(canvas, rect):
    rect.set_text("Flour")
    rect.move((5, 5))
    text = [i for i in canvas.find_withtag(
        rect._Rectangle__tag) if canvas.type(i) == "text"][0]
    assert canvas.coords(text) == [65.0, 50.0]


def test_label_recentres_when_width_changes(canvas, rect):
    rect.set_text("Flour")
    rect.width = 200
    text = [i for i in canvas.find_withtag(
        rect._Rectangle__tag) if canvas.type(i) == "text"][0]
    assert canvas.coords(text) == [110.0, 45.0]


def test_hide_hitbox_keeps_rect_but_removes_visuals(canvas, rect):
    rect.hide_hitbox()
    assert canvas.itemcget(rect._Rectangle__rect, "fill") == ""
    assert canvas.itemcget(rect._Rectangle__rect, "outline") == ""
    assert rect.width == 100
    assert rect.collide_point((50, 50))


def test_draw_adds_shape_sharing_the_rect_tag(canvas, rect):
    oval = rect.draw("oval", 0, 0, 10, 10, fill="green")
    assert oval in canvas.find_withtag(rect._Rectangle__tag)
    assert canvas.itemcget(oval, "fill") == "green"


def test_draw_rejects_unknown_shape(rect):
    with pytest.raises(ValueError, match="Unknown shape kind 'hexagon'"):
        rect.draw("hexagon", 0, 0)


def test_drawn_shape_moves_with_rect(canvas, rect):
    oval = rect.draw("oval", 0, 0, 10, 10)
    rect.move((7, 3))
    assert canvas.coords(oval) == [7.0, 3.0, 17.0, 13.0]


def test_move_shifts_position(rect):
    rect.move((5, -4))
    assert rect.left == 15
    assert rect.top == 16
    assert rect.width == 100
    assert rect.height == 50


def test_setting_left_moves_rect_keeping_size(rect):
    rect.left = 30
    assert rect.left == 30
    assert rect.right == 130
    assert rect.top == 20


def test_setting_right_moves_rect_keeping_size(rect):
    rect.right = 200
    assert rect.right == 200
    assert rect.left == 100
    assert rect.width == 100


def test_setting_r_alias_moves_right(rect):
    rect.r = 300
    assert rect.right == 300
    assert rect.r == 300


def test_setting_top_moves_rect_keeping_size(rect):
    rect.top = 0
    assert rect.top == 0
    assert rect.bottom == 50
    assert rect.height == 50


def test_setting_t_alias_moves_top(rect):
    rect.t = 90
    assert rect.top == 90
    assert rect.t == 90


def test_setting_bottom_moves_rect_keeping_size(rect):
    rect.bottom = 200
    assert rect.bottom == 200
    assert rect.top == 150
    assert rect.height == 50


def test_setting_b_alias_moves_bottom(rect):
    rect.b = 180
    assert rect.bottom == 180
    assert rect.b == 180


def test_setting_width_resizes_from_top_left(rect):
    rect.width = 250
    assert rect.width == 250
    assert rect.left == 10
    assert rect.right == 260


def test_setting_w_alias_resizes_width(rect):
    rect.w = 60
    assert rect.w == 60
    assert rect.width == 60


def test_setting_height_resizes_from_top_left(rect):
    rect.height = 80
    assert rect.height == 80
    assert rect.top == 20
    assert rect.bottom == 100


def test_setting_h_alias_resizes_height(rect):
    rect.h = 30
    assert rect.h == 30
    assert rect.height == 30


def test_centre_is_middle_of_rect(rect):
    assert rect.centre == (60, 45)
    assert rect.c == (60, 45)
    assert rect.centre_x == 60
    assert rect.cx == 60
    assert rect.centre_y == 45
    assert rect.cy == 45


def test_setting_centre_moves_rect_keeping_size(rect):
    rect.centre = (200, 200)
    assert rect.centre == (200, 200)
    assert rect.width == 100
    assert rect.height == 50


def test_setting_c_alias_moves_centre(rect):
    rect.c = (0, 0)
    assert rect.c == (0, 0)


def test_centre_right_is_middle_of_right_edge(rect):
    assert rect.centre_right == (110, 45)
    assert rect.cr == (110, 45)
