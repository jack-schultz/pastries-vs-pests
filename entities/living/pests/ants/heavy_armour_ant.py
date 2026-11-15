from __future__ import annotations
from armour.platemail import Platemail
from entities.living.pests.ants.ant import Ant


class HeavyArmourAnt(Ant):
    """An ant that wears heavy armour."""
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            armour=Platemail(),
        )
