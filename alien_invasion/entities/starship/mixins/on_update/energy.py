"""
"""

from typing import cast


def on_update_energy_capacity(self, delta_time: float, frame_energy_change: float):
    """Control engine energy flow and free fall mode."""
    # workaround circular imports
    from ...starship import Starship

    self = cast(Starship, self)

    # restore energy
    if self.current_energy_capacity < self.loadout.engine.energy_cap:
        self.current_energy_capacity += self.loadout.engine.energy_restored * delta_time
        frame_energy_change += self.loadout.engine.energy_restored * delta_time
        if self.current_energy_capacity > self.loadout.engine.energy_cap:
            self.current_energy_capacity = self.loadout.engine.energy_cap

    motion = (
        self.moving_left,
        self.moving_right,
        self.moving_up,
        self.moving_down,
    )
    # calculate sprite movement state
    # and stop if its both L and R pressed
    # calculate energy loss from base
    energy_loss = self.loadout.thrusters.energy_requirement * delta_time
    # first check for energy low
    if self.transmission.low_energy:
        energy_loss = 0
    # l+r+u/d
    elif all(motion[0:2]) and self.moving_up:
        energy_loss *= 1.4
    # l+r
    elif all(motion[0:2]):
        energy_loss *= 1.3
    # single
    elif any(motion):
        energy_loss *= 1.15
    # first calculatation
    self.current_energy_capacity -= energy_loss
    frame_energy_change -= energy_loss

    # are we now out of energy?
    # if already on low energy its free fall for minimum of 2sec
    # but if since free falling (last True value)
    # theres positive amount of energy but were
    # no movement since positivity
    # continue free falling
    # moving will disrupt free falling state
    # when at a timer more than 2sec passed of free fall
    free_falling_prev = self.free_falling
    self.free_falling = (
        0 < self._timers.outage < 1 or self.transmission.low_energy  # 1 sec
    ) or (self.free_falling and not self.transmission.low_energy and not any(motion))

    # disable moving and firing during free fall initialisation (time == 0)
    # and dont forcibly disbale it during free-fall following updates
    # so the player may himself press again keys for moving/fireing
    # separately
    if self.free_falling and not free_falling_prev:
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.firing_primary = False
