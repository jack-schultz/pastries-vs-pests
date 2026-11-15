from __future__ import annotations
from enum import Enum


# The direction an attack came from. For example, sugar cubes hit from
# the left, so a shield blocks them, but a shield would not defend
# against an explosion from behind
class Direction(Enum):
    """The directions an entity can face or move in."""
    LEFT = 1
    RIGHT = 2
    ABOVE = 3
    BELOW = 4
    AMBIENT = 5  # Like explosions or poison gas
