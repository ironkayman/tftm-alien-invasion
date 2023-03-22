from abc import ABC

from enum import IntEnum, auto

from pydantic import (
    BaseModel,
    Extra,
)

from alien_invasion.utils.loaders.item import load_item_as_dict


class ItemType(IntEnum):
    ABC = auto()
    ARMOR = auto()
    ENGINE = auto()
    HULL = auto()
    THRUSTER = auto()
    WEAPON = auto()


class Item(BaseModel, ABC):
    item_type: ItemType = ItemType.ABC
    item_name: str
    display_name: str
    description: str

    def __init__(self, model_name: str) -> None:
        super().__init__(
            **load_item_as_dict(model_name),  # type: ignore
            item_name=model_name
        )

    class Config:
        extra = Extra.forbid
        underscore_attrs_are_private = True
        validate_assignment = True
