from __future__ import annotations
from armour.chainmail import Chainmail
from entities.living.pests.ants.ant import Ant


class ArmourAnt(Ant):
    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            armour=Chainmail(),
        )
