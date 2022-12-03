class StarshipLoadout:
    """
    Attributes
    ----------
    hull : StarshipHull
    weaponry : StarshipWeaponry
    engine : StarshipEngine
    thruster : StarshipThruster
    """

    def __init__(self, config) -> None:
        sh = config['starship']

        self.hull = StarshipHull(sh['hull'], self)
        self.weaponry = StarshipWeaponry(sh['weaponry'], self)
        self.engine = StarshipEngine(sh['engine'], self)
        self.thrusters = StarshipThruster(sh['thrusters'], self)

def load_starship_loadout(config: dict):
    return StarshipLoadout(config)

from .starship_modules import (
    StarshipHull,
    StarshipWeaponry,
    StarshipEngine,
    StarshipThruster,
)