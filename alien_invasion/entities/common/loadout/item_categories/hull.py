from typing import Any, Optional

from pydantic import Field, root_validator

from .base_item import Item, ItemType

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

    @property
    def total_armor(self) -> int:
        return sum([
            m.armor for m in self.armor
        ])
