class StarshipLoadout:
    """
    Attributes
    ----------
    hull : StarshipHull
    weaponry : StarshipWeaponry
    """

    def __init__(self, config) -> None:
        self.hull = StarshipHull(config['starship']['hull'], self)
        self.weaponry = StarshipWeaponry(config['starship']['weaponry'], self)



def load_starship_loadout(config: dict):
    return StarshipLoadout(config)

from .starship_modules import (
    StarshipHull,
    StarshipWeaponry,
)