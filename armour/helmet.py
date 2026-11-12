from entities.damage import DamageType, Direction
from armour.base_armour import BaseArmour


class Helmet(BaseArmour):
    def __init__(self) -> None:
        super().__init__(
            durability=130,
            outline_colour="#5b7fa6",
            covered_directions={
                Direction.ABOVE
            },
            absorption={
                DamageType.GAS: 0.0,
                DamageType.FIRE: 0.0,
                DamageType.EXPLOSIVE: 0.5,
            },
            wear={
                DamageType.EXPLOSIVE: 2.0,
                DamageType.ACID: 2.0,
                DamageType.FIRE: 0.5,
            },
        )
