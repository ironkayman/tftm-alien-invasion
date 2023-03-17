from typing import cast

import arcade as arc

from alien_invasion.utils.loaders.alien.config import AlienMoveset

from alien_invasion.entities.starship.starship import LastDirection

def on_update_plot_movement(self, delta_time) -> None:
    """Based on current moveset and ship's pos calculate movement
    """
    self.last_direction_elapsed += delta_time

    # workaround circular imports
    from ...alien import Alien
    self = cast(Alien, self)

    # configure movement based on state's movesets
    movesets = self.config.states[self.state].movesets
    ship_x = self._starship.center_x

    # closes_bullet = arc.get_closest_sprite(self, self._starship.fired_shots)

    if AlienMoveset.tracking in movesets:
        if self.center_x == ship_x:
            self.change_x = 0
        elif self.center_x > ship_x:
            # if not (self.center_x - ship_x) < self.width // 2:
            self.change_x = -self.SPEED * delta_time
        elif self.center_x < ship_x:
            # if not (ship_x - self.center_x) < self.width // 2:
            self.change_x = self.SPEED * delta_time


    elif AlienMoveset.escaping in movesets:
        if self.center_x == ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x > ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x < ship_x:
            self.change_x = -self.SPEED * delta_time
