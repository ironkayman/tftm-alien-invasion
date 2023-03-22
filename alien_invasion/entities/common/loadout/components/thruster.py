from typing import Any

from pydantic import (
    Field,
    root_validator,
)

from ..item_categories import ItemThruster


class Thruster(ItemThruster):
    """
    """

    # additional attrs are required by pydantic
    loadout: Loadout = Field(default_factory=object, exclude=True)

    def __init__(self,
        thruster_dict: dict[str, Any],
        loadout: Loadout,
    ) -> None:
        """
        Paramters
        ---------
        thruster_dict : dict
        loadout : 'StarshipLoadout'
        """
        super().__init__(thruster_dict['model'])
        self.loadout = loadout


    @root_validator
    def check(cls, values: dict[str, Any]):
        return values

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True
        # fix loadout type since its imported later cyclically
        arbitrary_types_allowed = True

from ...loadout import Loadout