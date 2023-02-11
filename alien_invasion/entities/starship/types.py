from dataclasses import dataclass

@dataclass(frozen=True)
class TMovementArea:
    """Params of explorable by ship area.
    
    Used to passthrough StarShip parent Section parameters
    inside which ship can move.
    """
    left: int
    right: int
    bottom: int
    height: int
