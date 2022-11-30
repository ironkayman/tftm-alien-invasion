from typing import Any

from dataclasses import dataclass, field

from alien_invasion.constants import DIR_EQUIPMENT

from alien_invasion.entities.items.item import ItemArmor, ItemHull, ItemWeapon


@dataclass
class StarshipStats:
    armor: int = field(default=0)
    secondary_weapon_slots: int = field(default=0)
class StarshipHull(ItemHull):
    def __init__(self, hull_dict: dict[str, Any]) -> None:
        super().__init__(hull_dict['model'])
        breakpoint()
        self.armor_models = hull_dict['armor']

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

    def __init__(self, weaponry_dict: dict[str, Any], hull: StarshipHull) -> None:
        self.primary = ItemWeapon(weaponry_dict['primary']['model'])
        if len(weaponry_dict['secondary']) > hull.secondary_weapon_mount_slots:
            raise Exception('more than can be mounted')        
        for sc in weaponry_dict['secondary']:
            self.secondaries.append(ItemWeapon(sc['model']))

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
        self.stats.armor = self.hull.total_armor
        self.stats.secondary_weapon_slots = self.hull.secondary_weapon_mount_slots

        self.weaponry = StarshipWeaponry(config['starship']['weaponry'], self.hull)



def load_starship_loadout(config: dict):
    return StarshipLoadout(config)