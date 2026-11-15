from entities.direction import Direction


def test_has_five_distinct_directions():
    assert len({direction.value for direction in Direction}) == 5


def test_ambient_is_not_a_side():
    assert Direction.AMBIENT not in (Direction.LEFT, Direction.RIGHT, Direction.ABOVE, Direction.BELOW)
