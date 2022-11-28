from typing import Any

from dataclasses import dataclass, field

from alien_invasion.constants import DIR_EQUIPMENT

from alien_invasion.entities.items.item import ItemArmor, ItemHull


@dataclass
class StarshipStats:
    armor: int = field(default=0)

class StarshipHull(ItemHull):
    def __init__(self, hull_dict: dict[str, Any]) -> None:
        super().__init__(hull_dict['model'])
        self.armor_models = hull_dict['armor']


class StarshipLoadout:
    """
    Attributes
    ----------
    hull: StarshipHull
    """

    stats: StarshipStats

    def __init__(self, config) -> None:
        self.stats = StarshipStats()
        self.hull = StarshipHull(config['starship']['hull'])


def load_starship_loadout(config: dict):
    return StarshipLoadout(config)