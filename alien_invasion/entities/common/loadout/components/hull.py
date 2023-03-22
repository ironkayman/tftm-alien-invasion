from typing import Any

from pydantic import (
    Field,
)

from ..item_categories import ItemHull, ItemArmor

class Hull(ItemHull):

    # additional attrs are required by pydantic
    loadout: Loadout = Field(default_factory=object, exclude=True)

    def __init__(self,
        hull_dict: dict[str, Any],
        loadout: Loadout,
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

from ...loadout import Loadout