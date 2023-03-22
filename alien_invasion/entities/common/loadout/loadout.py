"""
"""


class Loadout:
    """
    Attributes
    ----------
    hull : ItemHull
    weaponry : Weaponry
    engine : ItemEngine
    thrusters : ItemThruster
    """

    def __init__(self, loadout_config: dict) -> None:
        """
        Examples
        --------
        >>> config = {
            'engine': {'model': '...'},
            'hull': {
                'armor': [
                    '...',
                    '...'
                ],
                'model': '...'
            },
            'thrusters': {'model': '...'},
            'weaponry': {
                'primary': {'model': '...'},
                'secondary': [
                    {'model': '...'},
                    {'model': '...'}
                ]
            }
        }
        """
        self.__loadout_config = loadout_config
        self.hull = ItemHull(self.__loadout_config['hull']['model'])
        self.weaponry = Weaponry(self.__loadout_config['weaponry'])
        self.engine = ItemEngine(self.__loadout_config['engine']['model'])
        self.thrusters = ItemThruster(self.__loadout_config['thrusters']['model'])

        self.__process_compatibilities()
        self.__cross_item_fill()

    def __process_compatibilities(self) -> None:
        """Store all cross-item logic checkers"""
        if len(self.weaponry.secondaries) > self.hull.secondary_weapon_mount_slots:
            raise NotImplementedError
        if len(self.hull.armor) > self.hull.armor_mount_slots:
            raise NotImplementedError

    def __cross_item_fill(self) -> None:
        self.hull.armor = [ItemArmor(name) for name in self.__loadout_config['hull']['armor']]

    def __repr__(self) -> str:
        return str({
            'hull': self.hull,
            'weaponry': self.weaponry,
            'engine': self.engine,
            'thrusters': self.thrusters,
        })

    def __str__(self) -> str:
        from pprint import pformat
        return pformat(object={
            'hull': self.hull,
            'weaponry': self.weaponry,
            'engine': self.engine,
            'thrusters': self.thrusters,
        }, indent=2, width=79)


from .components import (
    Weaponry,
)
from .item_categories import (
    ItemHull,
    ItemThruster,
    ItemEngine,
    ItemArmor,
    ItemWeapon,
)
