from entities.damage import DamageType, Direction
from armour.base_armour import BaseArmour


class Shield(BaseArmour):
    # Only protects the front (left). Very good against physical hits and fire
    def __init__(self) -> None:
        super().__init__(
            durability=500,
            outline_colour="#5b7fa6",
            covered_directions={
                Direction.LEFT
            },
            absorption={
                DamageType.GAS: 0.0,  # Blocks no gas
                DamageType.EXPLOSIVE: 0.5,  # Blocks half explosions
                DamageType.PIERCING: 0.5  # Blocks half piercing
            },
            wear={
                DamageType.EXPLOSIVE: 2.0,
                DamageType.ACID: 2.0,
                DamageType.FIRE: 0.5,
                DamageType.PIERCING: 1.5
            },
        )
