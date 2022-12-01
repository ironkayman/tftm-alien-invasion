from typing import Any
from abc import ABC

from enum import IntEnum, auto

from pydantic import (
    BaseModel,
    Field,
    Extra,
    root_validator,
    validator,
    ValidationError,
)

from alien_invasion.utils.loaders.item import load_item_as_dict


class ItemType(IntEnum):
    ABC = auto()
    ARMOR = auto()
    ENGINE = auto()
    HULL = auto()
    THRUSTERS = auto()
    WEAPON = auto()

# move to pydadantic for field validation
class Item(BaseModel, ABC):
    item_type: ItemType = ItemType.ABC
    item_name: str
    display_name: str
    description: str

    def __init__(self, model_name: str) -> None:
        super().__init__(
            **load_item_as_dict(model_name),
            item_name=model_name
        )

    class Config:
        extra = Extra.forbid
        underscore_attrs_are_private = True
        validate_assignment = True


class ItemArmor(Item):
    item_type: ItemType = ItemType.ARMOR

    armor: int


class ItemWeapon(Item):
    """
    Attributes
    ----------
    energy_per_bullet : int
        Enegry of ship's reactor consumed for a single bullet.
    reload_speed : float
        Time between bullet launches in `ms`.
    """

    item_type: ItemType = ItemType.WEAPON

    bullet_damage: int
    energy_per_bullet: int
    reload_speed: int

class ItemHull(Item):
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

    # @validator('armor', always=True, each_item=True)
    # def repopulate_armor(cls, val):
    #     breakpoint()
    #     return val

    # @validator('weapons', always=True, each_item=True)
    # def repopulate_weapons(cls, val):
    #     return val


    @property
    def total_armor(self) -> int:
        return sum([
            m.armor for m in self.armor
        ])


