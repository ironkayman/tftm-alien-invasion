from typing import Any

from pydantic import Field

from alien_invasion.constants import DIR_EQUIPMENT

from alien_invasion.entities.items.item import (
    ItemArmor,
    ItemHull,
    ItemWeapon,
)

from .starship import StarshipLoadout

# from functools import wraps
# def include_starship_loadout(starship_subclass) -> object:
#     starship_subclass.Config.arbitrary_types_allowed = True
#     starship_subclass.loadout = Field(default_factory=object, exclude=True)
#     # breakpoint()
#     def modify_init(*args):
#         breakpoint()
#         return starship_subclass(*args)
#     return modify_init

class StarshipHull(ItemHull):

    # additional attrs are required by pydantic
    loadout: StarshipLoadout = Field(default_factory=object, exclude=True)

    def __init__(self,
        hull_dict: dict[str, Any],
        loadout: 'StarshipLoadout',
    ) -> None:
        """
        Parameters
        ----------
        hull_dict : dict[str, Any]
        loadout: StarshipLoadout
            state
        """
        super().__init__(hull_dict['model'])
        # since config should contain armor models
        self.armor = [ItemArmor(a) for a in hull_dict['armor']]

        self.loadout = loadout

    class Config:
        # fix loadout type since its imported later cyclically
        arbitrary_types_allowed = True


class StarshipWeaponry:
    """
    Attributes
    ----------
    primary : ItemWeapon
        Primary starship's weapon.
    secondaries : list[ItemWeapon]
        List of secondary weapons.
    """

    primary: ItemWeapon
    secondaries: list[ItemWeapon] = []

    # additional attrs are required by pydantic
    loadout: StarshipLoadout = Field(default_factory=object, exclude=True)

    def __init__(self,
        weapons_dict: dict[str, Any],
        loadout: 'StarshipLoadout'
    ) -> None:
        """
        Paramters
        ---------
        weapons_dict : dict
        loadout : 'StarshipLoadout'
        """
        self.primary = ItemWeapon(weapons_dict['primary']['model'])
        # TODO: count checks
        self.secondaries = [ItemWeapon(n['model']) for n in weapons_dict['secondary']]
        self.loadout = loadout

    class Config:
        # fix loadout type since its imported later cyclically
        arbitrary_types_allowed = True
