from math import fsum
from abc import ABC

from enum import IntEnum, auto

from alien_invasion.utils.loaders.item import load_item_as_dict

class ItemType(IntEnum):
    ABC = auto()
    ARMOR = auto()
    ENGINE = auto()
    HULL = auto()
    THRUSTERS = auto()
    WEAPONRY = auto()

# move to pydadantic for field validation
class Item(ABC):
    item_type: ItemType = ItemType.ABC

    def __init__(self, model_name) -> None:
        self.model_name = model_name
        for k, v in load_item_as_dict(model_name).items():
            self.__setattr__(k, v)


# def load_equipment_from_categories():
#     WEAPONRY = DIR_EQUIPMENT / 'weaponry'
#     WEAPONRY.glob('*.json')

class ItemArmor(Item):
    item_type: ItemType = ItemType.ARMOR

    armor: int

class ItemHull(Item):
    item_type: ItemType = ItemType.HULL

    armor_mount_slots: int
    secondary_weapon_mount_slots: int
    
    __armor_models: list[ItemArmor] = []

    def total_armor(self) -> int:
        return round(fsum(
            [m.armor for m in self.armor_models]
        ))

    @property
    def armor_models(self) -> list[ItemArmor]:
        return self.__armor_models

    # todo move to pydantic for validation?
    @armor_models.setter
    def armor_models(self, model_names) -> None:
        # check if too many given
        if len(model_names) > self.armor_mount_slots:
            raise Exception

        for name in model_names:
            model = ItemArmor(name)
            self.__armor_models.append(model)
