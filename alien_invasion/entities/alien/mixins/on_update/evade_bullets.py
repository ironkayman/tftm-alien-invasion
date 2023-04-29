"""On_update extension for evading bullets
"""

from typing import cast
from random import random

import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.entities.common.state_manager.state import AlienMoveset
from alien_invasion.entities import Starship

def on_update_evade_bullets(alien, starship: Starship, delta_time: float) -> None:
    """Considers position of fired by starship shots and tries to dodge them
    """

    # workaround circular imports
    from ...alien import Alien
    alien = cast(Alien, alien)

    spacial_danger_ranges = starship.fired_shots

    # configure movement based on state's movesets
    movesets = alien.state.movesets

    is_bordered = AlienMoveset.bordered in movesets

    cl = arc.get_closest_sprite(alien, spacial_danger_ranges)
    if not cl:
        # set default
        cl = [0, 600] # 600px
    for b in spacial_danger_ranges:
        if (isect := set(range(round(alien.left - alien.width * 0.4), round(alien.right + alien.width * 0.4))).intersection(range(round(b.left), round(b.right)))):
            alien.change_x = alien.speed * delta_time
            # if aggressive moveset present and dodge is active
            # stop dodging by chance not in favour of time past dodging
            if AlienMoveset.tracking in movesets and alien.dodging:
                if random() < alien._timers.dodge * 0.1 * cl[1]:
                    alien.dodging = False
                    break
            alien.dodging = True
            # try to fofge the bullet by changing direction
            # the bullet passed more of left side -> dodge to the right
            if (alien.center_x - b.center_x) < 0:
                alien.change_x *= -1
        else:
            alien.dodging = False
            alien._timers.reset_dodge()
    # dodge timer reset proportianally to proximity to a bullet
    if alien.dodging and alien._timers.dodge > cl[1] / 800:
        alien._timers.reset_dodge()
        alien.dodging = False

    # stop movement when reaching borders with Bordered moveset property
    if is_bordered:
        if (
            alien.center_x <= 0 or
            alien.center_x >= CONSTANTS.DISPLAY.WIDTH
        ):
            alien.change_x *= -1
