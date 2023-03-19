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

    self._timer_firing += delta_time
    timeout_corrected = 1000

    if (
        self._timer_firing > timeout_corrected / 1000
    ):
        self._fire(delta_time)
        self._timer_firing = 0
