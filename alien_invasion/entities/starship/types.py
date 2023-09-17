from dataclasses import dataclass

from alien_invasion import CONSTANTS


@dataclass(frozen=True)
class TMovementArea:
    """Params of explorable by ship area.

    Used to passthrough StarShip parent Section parameters
    inside which ship can move.
    """

    left: int = 0
    right: int = CONSTANTS.DISPLAY.WIDTH
    bottom: int = 0
    height: int = CONSTANTS.DISPLAY.HEIGHT
