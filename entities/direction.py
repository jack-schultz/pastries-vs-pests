from __future__ import annotations
from enum import Enum


# Direction attack came from, for example SugarCubes hit from the left, so are blocked by a shield
# But a shield would not defend an explosion from behind
class Direction(Enum):
    """The directions an entity can face or move in."""
    LEFT = 1
    RIGHT = 2
    ABOVE = 3
    BELOW = 4
    AMBIENT = 5  # like explosions or poison gas
