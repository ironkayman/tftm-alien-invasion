from typing import cast

import arcade as arc

from alien_invasion.utils.loaders.alien.config import AlienMoveset


def on_update_fire_bullets(self, delta_time: float) -> None:
    """Timer for firing in periodic manner
    """

    # workaround circular imports
    from ...alien import Alien
    self = cast(Alien, self)

    movesets = self.config.states[self.state].movesets

    if AlienMoveset.tracking not in movesets: return

    self._timers.primary += delta_time

    if (
        self._timers.primary > self.timeouts.primary / 1000 / self.SPEED * 100
    ):
        self._fire(delta_time)
        self._timers.reset_primary()
