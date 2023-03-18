from typing import cast

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
            self._timer_track += delta_time
            if self.center_x == ship_x:
                pass
            elif self.center_x > ship_x and self._timer_track > 0.3:
                self._timer_track = 0
                self.change_x = -self.SPEED * delta_time
            elif self.center_x < ship_x and (self._timer_track > 0.3):
                self._timer_track = 0
                self.change_x = self.SPEED * delta_time
        else:
            self._timer_dodge += delta_time


    elif AlienMoveset.escaping in movesets:
        if self.center_x == ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x > ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x < ship_x:
            self.change_x = -self.SPEED * delta_time
