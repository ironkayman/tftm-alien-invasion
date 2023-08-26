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

    def get_alien_count_proportion_on_x_axis() -> float:
        """Get proportianal float value of aliens.

        Returns
        -------
        float
            Relative floating-point value of aliens
            on the right side of the current entity,
            divided by same count on the right.
        """
        aliens_count_on_right = (
            len(
                tuple(
                    filter(
                        lambda a: a.center_x > alien.center_x, alien._parent_sprite_list
                    )
                )
            )
            or 1
        )
        aliens_count_on_left = (
            len(
                tuple(
                    filter(
                        lambda a: a.center_x < alien.center_x, alien._parent_sprite_list
                    )
                )
            )
            or 1
        )
        # >0 - left more, <0 - right more
        return aliens_count_on_left / aliens_count_on_right

    if starship.can_reap():
        return

    # configure movement based on state's movesets
    movesets = alien.state.movesets
    ship_x = starship.center_x
    relative_amount = get_alien_count_proportion_on_x_axis()

    # when theresa persuing moveset, stop right above center of the veiwport
    if (AlienMoveset.persuing in movesets or alien._overrides.should_persue) and (
        alien.bottom < CONSTANTS.DISPLAY.HEIGHT * 0.6
    ):
        alien.change_y = 0

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
