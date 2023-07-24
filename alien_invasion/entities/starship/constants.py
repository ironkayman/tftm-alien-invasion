from enum import IntEnum, auto


class LastDirection(IntEnum):
    """Direction, at which starship was lastly pointed to."""

    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()


# set hitbox size
HITBOX_POLYGON_SHAPE = (
    (-2, 5),
    (2, 5),
    (5, 0),
    (2, -5),
    (-2, -5),
    (-5, 0),
)
