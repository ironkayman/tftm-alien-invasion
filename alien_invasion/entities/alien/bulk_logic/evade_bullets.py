"""On_update extension for evading bullets
"""

from typing import cast
from random import random

import arcade as arc

from alien_invasion.entities.common.state_manager.state import AlienMoveset
from alien_invasion.entities import Starship

def on_update_evade_bullets(
    alien,
    starship: Starship,
    delta_time: float,
) -> None:
    """Considers position of starship's bullets and tries to dodge them
    """

    # workaround circular imports
    from ...alien import Alien
    alien = cast(Alien, alien)

    starship_bullets = starship.fired_shots

    # configure movement based on state's movesets
    movesets = alien.state.movesets

    # is_bordered = AlienMoveset.bordered in movesets

    # closest starship's bullet
    closest_bullet, closest_distance = arc.get_closest_sprite(
        alien, starship_bullets
    ) or [None, None]
    # if not closest_bullet: continue

    alien_last_chg_x = alien.change_x

    #----_a_--- - alien on line with a bullet, where _ - proximity to hitbox
    #----|----
    #----|---- - bullet trajectory
    #----*---- - vertically fired bullet
    #    ^ - staship
    isect = None
    for b in starship_bullets:
        # 2 ranges are created, of ints, if they intersect, this means that
        # alien's extended proximity hitbox area is on the line
        # with a bullet's hitbox
        # TODO: extended proximity area move to calculatable @property
        # of an Alien/Entity class, whose extended proximity is calculated ased on .size
        if (isect := \
            set(range(
                round(alien.left - alien.width * 0.4),
                round(alien.right + alien.width * 0.4)
            )).intersection(range(
                round(b.left),
                round(b.right)
            ))
        ):
            alien.change_x = alien.speed * delta_time

            # if aggressive moveset present and dodge is active
            # stop dodging by chance not in favour of time past dodging
            if AlienMoveset.tracking in movesets and alien.dodging:
                if random() < alien._timers.dodge * 0.1 * closest_distance:
                    alien.dodging = False
                    break
            alien.dodging = True
            # try to dodge the bullet by changing direction
            # the bullet passed more of left side -> dodge to the right
            if (alien.center_x - b.center_x) < 0:
                alien.change_x *= -1
    if isect is None or not closest_bullet:
        alien.dodging = False
        alien._timers.reset_dodge()
        # restore origina direction, or alien will fall out of the viewport
        alien.change_x = alien_last_chg_x
    # dodge timer reset proportianally to proximity to a bullet
    if alien.dodging and alien._timers.dodge > closest_distance / 800:
        alien._timers.reset_dodge()
        alien.dodging = False

    # stop movement when reaching borders with Bordered moveset property
    # if is_bordered:
    #     if (
    #         alien.center_x <= 0 or
    #         alien.center_x >= CONSTANTS.DISPLAY.WIDTH
    #     ):
    #         alien.change_x *= -1
