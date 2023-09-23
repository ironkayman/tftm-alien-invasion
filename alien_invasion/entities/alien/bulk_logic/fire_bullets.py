"""on_update mixin for bullet firing
"""

from typing import cast

import arcade as arc

from alien_invasion.entities.common.state_manager.state import AlienMoveset
from alien_invasion.entities import Starship

def on_update_fire_bullets(alien, starship: Starship, delta_time: float) -> None:
    """On-update check for firing in periodic manner
    """

    # workaround circular imports
    from ...alien import Alien
    alien = cast(Alien, alien)

    #  firing is active only in tracking moveset
    if AlienMoveset.tracking not in alien.state.movesets:
        return

    alien._timers.primary += delta_time

    if (
        alien._timers.primary >= alien.timeouts.primary / 1000
    ):
        alien._timers.reset_primary()
        alien._fire(delta_time)
