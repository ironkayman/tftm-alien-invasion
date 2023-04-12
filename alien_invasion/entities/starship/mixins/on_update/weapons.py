"""On_update extension for firing bullets on demand
"""

from typing import cast

from alien_invasion import CONSTANTS

def on_update_firing(
    self,
    delta_time: float,
    frame_energy_change: float
):
    """Check for firing button pressed.

    Fire if enought energy, rapid fire condiition and weapon timeout.
    """
    # from ...starship import Starship
    # self = cast(self, Starship)

    full_motion = all((self.moving_left, self.moving_right))
    self._timers.primary += delta_time
    # correcteed timeout:
    # it behaves as usual until ship is in static full thruster motion,
    # then timeout is cut to 2/3,
    # while being hicher than 30% of energy capacity
    timeout_corrected = (
        self.timeouts.primary * 0.66 if
        full_motion and ((self.current_energy_capacity / self.loadout.engine.energy_cap) * 100) >= 30
        else self.timeouts.primary
    )

    # firing
    if (
        self.firing_primary and
        self._timers.primary > timeout_corrected / 1000
        and not self.transmission.low_energy
    ):
        self.current_energy_capacity -= self.loadout.weaponry.primary.energy_per_bullet
        self._timers.reset_primary()
        frame_energy_change -= self.loadout.weaponry.primary.energy_per_bullet

        self._fire_primary(delta_time)
