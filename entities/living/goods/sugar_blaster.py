from __future__ import annotations
from entities.living.goods.sugar_shooter import SugarShooter


class SugarBlaster(SugarShooter):
    """An upgraded SugarShooter."""

    def __init__(self, canvas, x, y) -> None:
        super().__init__(
            canvas, x, y,
            # waits 1.4, fires, waits .25, fires repeat
            delay_pattern=(1.4, 0.25),
        )
        self.rect.set_text("Sugar Blaster")
