"""on_update mixin for bullet firing
"""

from typing import cast

from alien_invasion.entities import Starship


def on_update_fire_bullets(alien, starship: Starship, delta_time: float) -> None:
    """On-update check for firing in periodic manner"""

    # workaround circular imports
    from ...alien import Alien

    alien = cast(Alien, alien)

    alien._timers.primary += delta_time

    if alien._timers.primary >= alien.timeouts.primary:
        alien._timers.reset_primary()
        alien._fire(delta_time)
