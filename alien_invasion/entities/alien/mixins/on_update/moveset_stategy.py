"""On_update extension for movement management
"""

from random import random
from typing import cast
import math


from alien_invasion import CONSTANTS
from alien_invasion.entities.common.state_manager.state import AlienMoveset
from alien_invasion.entities.starship import Starship


def on_update_plot_movement(alien, starship: Starship, delta_time: float) -> None:
    """Based on current moveset and ship's posirion calculate its movement"""

    # workaround circular imports
    from ...alien import Alien

    alien = cast(Alien, alien)

    if starship.can_reap():
        return

    # configure movement based on state's movesets
    movesets = alien.state.movesets
    ship_x = starship.center_x
    relative_amount = random()

    # when theresa persuing moveset, stop right above center of the veiwport
    if AlienMoveset.persuing in movesets and alien.center_y < CONSTANTS.DISPLAY.HEIGHT * 0.8:
        alien.change_y = starship.change_y * 0.94
        alien.change_x = starship.change_x * 0.94

    is_bordered = AlienMoveset.bordered in movesets

    if AlienMoveset.tracking in movesets:
        if not alien.dodging:
            if (
                math.fabs(alien.center_x - ship_x)
                < starship.width / starship.width * random()
            ):
                alien.change_x = 0
            elif alien.center_x > ship_x:
                alien._timers.reset_track()
                alien.change_x = -alien.speed * delta_time / relative_amount
            elif alien.center_x < ship_x:
                alien._timers.reset_track()
                alien.change_x = alien.speed * delta_time * relative_amount
            alien._timers.track += delta_time
        else:
            alien._timers.dodge += delta_time

        # stop movement when reaching borders with Bordered moveset property
        if is_bordered:
            if alien.center_x <= 0 or alien.center_x >= CONSTANTS.DISPLAY.WIDTH:
                alien.change_x *= -1

    elif AlienMoveset.escaping in movesets:
        if alien.center_x == ship_x:
            alien.change_x = alien.speed * delta_time
        elif alien.center_x > ship_x:
            alien.change_x = alien.speed * delta_time
        elif alien.center_x < ship_x:
            alien.change_x = -alien.speed * delta_time
