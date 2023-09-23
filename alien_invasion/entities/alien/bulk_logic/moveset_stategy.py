"""On_update extension for movement management
"""
from random import random
from typing import cast
from math import fabs

import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.entities.common.state_manager.state import AlienMoveset
from alien_invasion.entities.starship import Starship

def on_update_plot_movement(
    alien_group: arc.SpriteList,
    starship: Starship,
    delta_time: float,
) -> None:
    """Based on current moveset and ship's posirion calculate its movement
    
    Parameters
    ----------
    alien_group : arc.SpriteList
        SpriteList of `Alien`s generated from a common spawner.
    starship : Starship
    delta_time : float
    """

    from ...alien import Alien

    ship_pos_x = starship.center_x
    ship_pos_y = starship.center_y
    ship_chg_x = starship.change_x
    ship_chg_y = starship.change_y

    # configure movement based on state's movesets
    for alien in alien_group:
        # workaround circular imports
        alien = cast(Alien, alien)

        movesets = alien.state.movesets

        if AlienMoveset.persuing in movesets:
            alien.change_x = starship.change_x * 0.95

        if AlienMoveset.tracking in movesets:
            # dodge timer, tracks starship's bullets
            if not alien.dodging:
                if (
                    fabs(alien.center_x - ship_pos_x)
                    < starship.width / starship.width 
                ):
                    alien.change_x = 0
                elif alien.center_x > ship_pos_x:
                    alien._timers.reset_track()
                    alien.change_x = -alien.speed * delta_time
                elif alien.center_x < ship_pos_x:
                    alien._timers.reset_track()
                    alien.change_x = alien.speed * delta_time
                alien._timers.track += delta_time
            else:
                alien._timers.dodge += delta_time

        elif AlienMoveset.escaping in movesets:
            if alien.center_x == ship_pos_x:
                alien.change_x = alien.speed * delta_time
            elif alien.center_x > ship_pos_x:
                alien.change_x = fabs(alien.speed) * delta_time
            elif alien.center_x < ship_pos_x:
                alien.change_x = -alien.speed * delta_time
