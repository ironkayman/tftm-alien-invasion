"""On_update extension for movement management
"""

from random import random
from typing import cast
import math

from alien_invasion import CONSTANTS
from alien_invasion.entities.common.state_manager.state import AlienMoveset


def on_update_plot_movement(self, delta_time: float) -> None:
    """Based on current moveset and ship's posirion calculate its movement
    """

    # workaround circular imports
    from ...alien import Alien
    self = cast(Alien, self)

    def get_alien_count_proportion_on_x_axis() -> float:
        """Get proportianal float value of aliens.

        Returns
        -------
        float
            Relative floating-point value of aliens
            on the right side of the current entity,
            divided by same count on the right.
        """
        aliens_count_on_right = len(tuple(filter(
            lambda a: a.center_x > self.center_x,
            self._parent_sprite_list
        ))) or 1
        aliens_count_on_left = len(tuple(filter(
            lambda a: a.center_x < self.center_x,
            self._parent_sprite_list
        ))) or 1
        # >0 - left more, <0 - right more
        return aliens_count_on_left / aliens_count_on_right


    if self._starship.can_reap(): return

    # configure movement based on state's movesets
    movesets = self.state.movesets
    ship_x = self._starship.center_x
    relative_amount = get_alien_count_proportion_on_x_axis()

    # when theresa persuing moveset, stop right above center of the veiwport
    if (
        (
            AlienMoveset.persuing in movesets or self._overrides.should_persue
        ) and (
            self.bottom < CONSTANTS.DISPLAY.HEIGHT * 0.6
        )
    ):
        self.change_y = 0

    if AlienMoveset.tracking in movesets:
        if not self.dodging:
            if math.fabs(self.center_x - ship_x) < self._starship.width / self._starship.width * random():
                self.change_x = 0
            elif self.center_x > ship_x:
                self._timers.reset_track()
                self.change_x = -self.speed * delta_time / relative_amount
            elif self.center_x < ship_x:
                self._timers.reset_track()
                self.change_x = self.speed * delta_time * relative_amount
            self._timers.track += delta_time
        else:
            self._timers.dodge += delta_time

    elif AlienMoveset.escaping in movesets:
        if self.center_x == ship_x:
            self.change_x = self.speed * delta_time
        elif self.center_x > ship_x:
            self.change_x = self.speed * delta_time
        elif self.center_x < ship_x:
            self.change_x = -self.speed * delta_time

    # if alien reaches ship's top, dont change alien's x-axis
    if self.center_y < self._starship.top * 1.33:
        self.change_x = 0
