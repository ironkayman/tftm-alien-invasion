"""On_update extension for movement management
"""
from random import random
from typing import cast
import math

import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.entities.common.state_manager.state import AlienMoveset
from alien_invasion.entities.starship import Starship


def on_update_plot_movement(alien_group: arc.SpriteList, starship: Starship, delta_time: float) -> None:
    """Based on current moveset and ship's posirion calculate its movement"""

    # configure movement based on state's movesets
    for alien in alien_group:
        # workaround circular imports
        from ...alien import Alien
        alien = cast(Alien, alien)

        # TODO: is_* flags generate/move to alien instance's class
        # and update per state change
        movesets = alien.state.movesets
        ship_x = starship.center_x

        # when theresa persuing moveset, stop right above center of the veiwport
        if AlienMoveset.persuing in movesets:
            alien.change_x = starship.change_x * 0.95

        is_bordered = AlienMoveset.bordered in movesets

        if AlienMoveset.tracking in movesets:
            if not alien.dodging:
                if (
                    math.fabs(alien.center_x - ship_x)
                    < starship.width / starship.width 
                ):
                    alien.change_x = 0
                elif alien.center_x > ship_x:
                    alien._timers.reset_track()
                    alien.change_x = -alien.speed * delta_time
                elif alien.center_x < ship_x:
                    alien._timers.reset_track()
                    alien.change_x = alien.speed * delta_time
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
