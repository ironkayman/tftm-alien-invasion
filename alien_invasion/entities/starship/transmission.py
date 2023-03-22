"""Logic for considering window borders
"""

from .types import TMovementArea

class Transmission:
    """Thransmission and surroundings reactive movement manager."""
    def __init__(self, starship: 'Starship') -> None:
        self.starship = starship
        self.area: TMovementArea = self.starship.movement_borders

    @property
    def low_energy(self) -> bool:
        return self.starship.current_energy_capacity <= 0

    @property
    def border_reached_left(self) -> bool:
        """Check if ship touches left border."""
        return self.starship.left < self.area.left

    @property
    def border_reached_right(self) -> bool:
        """Check if ship touches right border."""
        return self.starship.right > self.area.right

    @property
    def throttle(self) -> bool:
        """Throttler manages movement and considers surroundings.

        If anything in block `any` if successful do throttle.
        This logic ties to `movement_update` functions of `StarShip` class
        where transmission calculates and takes
        in an account current ship movement states.
        """
        return any((
            # no energy
            all((
                self.low_energy,
                self.starship.moving_left or self.starship.moving_right,
            )),
            # touched left border
            all((
                self.starship.moving_left,
                self.border_reached_left
            )),
            # touched right border
            all((
                self.starship.moving_right,
                self.border_reached_right
            )),
        ))