

class Loadout:
    """
    Attributes
    ----------
    hull : Hull
    weaponry : Weaponry
    engine : Engine
    thruster : Thruster
    """

    def __init__(self, config) -> None:
        sh = config['starship']

        self.hull = Hull(sh['hull'], self)
        self.weaponry = Weaponry(sh['weaponry'], self)
        self.engine = Engine(sh['engine'], self)
        self.thrusters = Thruster(sh['thrusters'], self)

    @staticmethod
    def load_from_config(config: dict):
        return Loadout(config)


from .components import (
    Hull,
    Weaponry,
    Engine,
    Thruster,
)