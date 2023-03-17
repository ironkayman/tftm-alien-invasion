from alien_invasion.utils.loaders.alien.config import AlienMoveset


def on_update_plot_movement(self, delta_time) -> None:
    """Based on current moveset and ship's pos calculate movement
    """
    # configure movement based on state's movesets
    movesets = self.config.states[self._current_state_index].movesets
    ship_x = self._starship.center_x

    if AlienMoveset.tracking in movesets:
        # todo add slight drift
        if self.center_x == ship_x:
            self.change_x = 0
        elif self.center_x > ship_x:
            self.change_x = -self._starship.SPEED * delta_time * 0.3
        elif self.center_x < ship_x:
            self.change_x = self._starship.SPEED * delta_time * 0.3

    elif AlienMoveset.escaping in movesets:
        if self.center_x == ship_x:
            self.change_x = self._starship.SPEED * delta_time * 2.3
        elif self.center_x > ship_x:
            self.change_x = self._starship.SPEED * delta_time * 0.3
        elif self.center_x < ship_x:
            self.change_x = -self._starship.SPEED * delta_time * 0.3
