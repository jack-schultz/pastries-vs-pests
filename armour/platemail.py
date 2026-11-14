from entities.damage_type import DamageType
from armour.base_armour import BaseArmour


class Platemail(BaseArmour):
    # Covers all sides. Strong against physical hits, weak to fire/gas/piercing, and acid eats it
    def __init__(self) -> None:
        super().__init__(
            durability=450,
            outline_colour="#9a9a9a",
            absorption={
                DamageType.EXPLOSIVE: 0.75,
                DamageType.FIRE: 0.1,
                DamageType.GAS: 0.0,
                DamageType.PIERCING: 0.75,
            },
            wear={
                DamageType.ACID: 3.0,
            },
            layer_count=2
        )
