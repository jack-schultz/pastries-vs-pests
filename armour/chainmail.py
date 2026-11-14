from entities.damage_type import DamageType
from armour.base_armour import BaseArmour


class Chainmail(BaseArmour):
    # Covers all sides. Strong against physical hits, weak to fire/gas/piercing, and acid eats it
    def __init__(self) -> None:
        super().__init__(
            durability=350,
            outline_colour="#9a9a9a",
            absorption={
                DamageType.EXPLOSIVE: 0.5,  # Blocks half damage
                DamageType.FIRE: 0.0,  # Blocks no fire
                DamageType.GAS: 0.0,  # Blocks no gas
                DamageType.PIERCING: 0.25,  # Blocks only a quarter of piercing
            },
            wear={
                DamageType.ACID: 3.0,
                DamageType.PIERCING: 2.0  # Rings get punched through
            },
        )
