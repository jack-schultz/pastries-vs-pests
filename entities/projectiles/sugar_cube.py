from __future__ import annotations
from entities.projectiles.projectile import Projectile


class SugarCube(Projectile):
    # The projectile fired by SugarShooter and SugarBlaster
    def __init__(self, canvas, centre_x, centre_y) -> None:
        super().__init__(
            canvas, centre_x, centre_y,
            size=14,
            colour="#ff8fab",
            damage=60,
            speed=6,  # pixels per frame
            piercing=1
        )
        # White cube with a pink edge
        self.rect.set_colour("#ffffff")
        self.rect.set_outline("#ff8fab", width=2)
        x1, y1 = self.rect.left, self.rect.top
