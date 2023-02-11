"""
"""

def on_update_energy_capacity(
    self,
    delta_time: float,
    frame_energy_change: float
):
    """Control engine energy flow and free fall mode.
    """

    # restore energy
    if self.current_energy_capacity < self.loadout.engine.energy_cap:
        self.current_energy_capacity += self.loadout.engine.energy_restored * delta_time
        frame_energy_change += self.loadout.engine.energy_restored * delta_time
        if self.current_energy_capacity > self.loadout.engine.energy_cap:
            self.current_energy_capacity = self.loadout.engine.energy_cap

    motion = (self.moving_left, self.moving_right)
    # calculate sprite movement state
    # and stop if its both L and R pressed
    # calculate energy loss from base
    energy_loss = self.loadout.thrusters.energy_requirement * delta_time
    # first check for energy low
    if self.transmission.low_energy:
        energy_loss = 0
    # both
    elif all(motion):
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
    self.free_falling = (
        (
            0 < self.free_fall_timer < 1 # 1 sec
            or self.transmission.low_energy
        ) or (
            self.free_falling and
            not self.transmission.low_energy and
            not any(motion)
        )
    )

    # disable moving and firing during free fall initialisation (time == 0)
    # and dont forcibly disbale it during free-fall following updates
    # so the player may himself press again keys for moving/fireing
    # separately
    if self.free_falling and self.free_fall_timer == 0:
        self.moving_left = False
        self.moving_right = False
        self.firing_primary = False
