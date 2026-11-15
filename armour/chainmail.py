from entities.damage_type import DamageType
from armour.base_armour import BaseArmour


class Chainmail(BaseArmour):
    """Covers all sides. Strong against physical hits, weak to
    fire/gas/piercing, and acid eats it
    """

    def __init__(self) -> None:
        super().__init__(
            durability=350,
            outline_colour="#9a9a9a",
            absorption={
                DamageType.EXPLOSIVE: 0.5,  # It blocks half damage.
                DamageType.FIRE: 0.0,  # It blocks no fire.
                DamageType.GAS: 0.0,  # It blocks no gas
                # It blocks only a quarter of piercing
                DamageType.PIERCING: 0.25,
            },
            wear={
                DamageType.ACID: 3.0,
                # Piercing hits punch through the rings.
                DamageType.PIERCING: 2.0
            },
        )
