from typing import cast
import math

import arcade as arc

from alien_invasion.utils.loaders.alien.config import AlienMoveset


def on_update_plot_movement(self, delta_time) -> None:
    """Based on current moveset and ship's pos calculate movement
    """

    # workaround circular imports
    from ...alien import Alien
    self = cast(Alien, self)

    # configure movement based on state's movesets
    movesets = self.config.states[self.state].movesets
    ship_x = self._starship.center_x

    if AlienMoveset.tracking in movesets:
        if not self.dodging:
            if math.fabs(self.center_x - ship_x) < self._starship.width / 2:
                self.change_x = 0
            elif self.center_x > ship_x:
                self._timers.reset_track()
                self.change_x = -self.SPEED * delta_time
            elif self.center_x < ship_x:
                self._timers.reset_track()
                self.change_x = self.SPEED * delta_time
            self._timers.track += delta_time
        else:
            self._timers.dodge += delta_time


    elif AlienMoveset.escaping in movesets:
        if self.center_x == ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x > ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x < ship_x:
            self.change_x = -self.SPEED * delta_time
