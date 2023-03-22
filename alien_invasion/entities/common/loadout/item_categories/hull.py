from typing import Any

from pydantic import Field, root_validator

from base_item import Item, ItemType

from .armor import ItemArmor
from .weapon import ItemWeapon


class ItemHull(Item):
    """
    Parameters
    ----------
    model_name : str
        Model type name
    """

    item_type: ItemType = ItemType.HULL

    armor_mount_slots: int
    secondary_weapon_mount_slots: int

    armor: list[ItemArmor] = Field(default_factory=list, allow_mutation=True)
    weapons: list[ItemWeapon] = Field(default_factory=list, allow_mutation=True)

    # runs on each attribute change
    @root_validator(pre=True)
    def check(cls, values: dict[str, Any]):
        if any ((
            len(values.get('weapons', [])) > values['secondary_weapon_mount_slots'],
            len(values.get('armor', [])) > values['armor_mount_slots'],
        )):
            raise Exception
        return values

    @property
    def total_armor(self) -> int:
        return sum([
            m.armor for m in self.armor
        ])
