"""Logic for considering window borders
"""

from .types import TMovementArea
from alien_invasion import CONSTANTS


class Transmission:
    """Thransmission and surroundings reactive movement manager."""

    def __init__(self, starship) -> None:
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
    def border_reached_top(self) -> bool:
        """Check if ship touches top border."""
        return self.starship.top > CONSTANTS.DISPLAY.HEIGHT

    @property
    def border_reached_bottom(self) -> bool:
        """Check if ship touches bottom border."""
        return self.starship.bottom < 0

    @property
    def throttle(self) -> bool:
        """Throttler manages movement and considers surroundings.

        If anything in block `any` if successful do throttle.
        This logic ties to `movement_update` functions of `StarShip` class
        where transmission calculates and takes
        in an account current ship movement states.
        """
        return any(
            (
                # no energy
                all(
                    (
                        self.low_energy,
                        any(
                            (
                                self.starship.moving_left,
                                self.starship.moving_right,
                                self.starship.moving_up,
                                self.starship.moving_down,
                            )
                        ),
                    )
                ),
                # touched borders
                self.starship.moving_left and self.border_reached_left,
                self.starship.moving_right and self.border_reached_right,
                self.starship.moving_up and self.border_reached_top,
                self.starship.moving_down and self.border_reached_bottom,
            )
        )
