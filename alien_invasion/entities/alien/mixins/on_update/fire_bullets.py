"""on_update mixin for bullet firing
"""

from typing import cast

import arcade as arc

from alien_invasion.entities.common.state_manager.state import AlienMoveset


def on_update_fire_bullets(self, delta_time: float) -> None:
    """On-update check for firing in periodic manner
    """

    # workaround circular imports
    from ...alien import Alien
    self = cast(Alien, self)

    #  firing is active only in tracking moveset
    if AlienMoveset.tracking not in self.state.movesets:
        return

    self._timers.primary += delta_time

    if (
        self._timers.primary > self.timeouts.primary / 1000 / self.speed * 100
    ):
        self._fire(delta_time)
        self._timers.reset_primary()
