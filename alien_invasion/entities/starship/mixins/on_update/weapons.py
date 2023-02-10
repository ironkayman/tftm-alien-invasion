def on_update_firing(
    self,
    delta_time: float,
    frame_energy_change: float
):
    """Check for firing button pressed.
    
    Fire if enought energy, rapid fire condiition and weapon timeout.
    """

    full_motion = all((self.moving_left, self.moving_right))
    self.loadout.weaponry.primary._timer += delta_time
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
        self.loadout.weaponry.primary._timer > timeout_corrected / 1000
        and not self.transmission.low_energy
    ):
        self._fire_primary(delta_time)
        self.current_energy_capacity -= self.loadout.weaponry.primary.energy_per_bullet
        self.loadout.weaponry.primary._timer = 0
        frame_energy_change -= self.loadout.weaponry.primary.energy_per_bullet
