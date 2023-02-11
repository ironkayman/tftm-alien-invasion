from enum import IntEnum, auto

class LastDirection(IntEnum):
    """Direction, at which starship was lastly pointed to.
    """
    
    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()