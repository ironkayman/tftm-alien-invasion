from typing import Any, Optional

from pydantic import (
    BaseModel,
    Field,
)

from ..item_categories.weapon import ItemWeapon


class Weaponry(BaseModel):
    """
    Attributes
    ----------
    primary : ItemWeapon
        Primary starship's weapon.
    secondaries : list[ItemWeapon]
        List of secondary weapons.
    """

    primary: Optional[ItemWeapon] = None
    secondaries: list[ItemWeapon] = Field(default_factory=list)

    def __init__(self,
        weapons_dict: dict[str, Any],
    ) -> None:
        """
        Paramters
        ---------
        weapons_dict : dict
        loadout : 'StarshipLoadout'
        """
        super().__init__()
        # self.loadout = loadout

        self.primary = ItemWeapon(weapons_dict['primary']['model'])  # type: ignore
        self.secondaries = [ItemWeapon(n['model']) for n in weapons_dict['secondary']]

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True
        arbitrary_types_allowed = True
