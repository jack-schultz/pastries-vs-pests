from entities.damage import DamageType
from armour.base_armour import BaseArmour


class Chainmail(BaseArmour):
    # Covers all sides. Strong against physical hits, weak to fire/gas, and acid eats it
    def __init__(self, durability: float = 80) -> None:
        super().__init__(
            durability,
            outline_colour="#9a9a9a",
            absorption={
                DamageType.EXPLOSIVE: 0.5,  # Blocks half damage
                DamageType.FIRE: 0.0,  # Blocks no fire
                DamageType.GAS: 0.0,  # Blocks no gas
            },
            wear={
                DamageType.ACID: 3.0
            },
        )
