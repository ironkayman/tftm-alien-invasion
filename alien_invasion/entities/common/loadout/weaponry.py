from typing import Any

from pydantic import (
    BaseModel,
    Field,
    root_validator,
)

from .item_categories.weapon import ItemWeapon


class Weaponry(BaseModel):
    """
    Attributes
    ----------
    primary : ItemWeapon
        Primary starship's weapon.
    secondaries : list[ItemWeapon]
        List of secondary weapons.
    """

    primary: ItemWeapon|None = None
    secondaries: list[ItemWeapon]|None = Field(default_factory=list)

    # additional attrs are required by pydantic
    loadout = Field(default_factory=object, exclude=True)

    def __init__(self,
        weapons_dict: dict[str, Any],
        loadout,
    ) -> None:
        """
        Paramters
        ---------
        weapons_dict : dict
        loadout : 'StarshipLoadout'
        """
        super().__init__()
        self.loadout = loadout

        self.primary = ItemWeapon(weapons_dict['primary']['model']))  # type: ignore
        self.secondaries = [ItemWeapon(n['model']) for n in weapons_dict['secondary']]

    # runs on each attribute change
    @root_validator(pre=True)
    def check(cls, values: dict[str, Any]):
        # handle presetuped validator firing
        if not values.get('loadout', False):
            return values
        if len(values.get('secondaries', [])) > values.get('loadout').hull.secondary_weapon_mount_slots:
            raise Exception
        return values

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True
        arbitrary_types_allowed = True


from .loadout import Loadout