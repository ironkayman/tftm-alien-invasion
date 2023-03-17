from alien_invasion.utils.loaders.alien.config import AlienMoveset

from alien_invasion.entities.starship.starship import LastDirection

def on_update_plot_movement(self, delta_time) -> None:
    """Based on current moveset and ship's pos calculate movement
    """
    self.last_direction_elapsed += delta_time

    # configure movement based on state's movesets
    movesets = self.config.states[self.state].movesets
    ship_x = self._starship.center_x
    # last_direction = self.change_x

    if AlienMoveset.tracking in movesets:
        # todo add slight drift
        if self.center_x == ship_x:
            self.change_x = 0
        elif self.center_x > ship_x:
            self.change_x = -self.SPEED * delta_time
        elif self.center_x < ship_x:
            self.change_x = self.SPEED * delta_time

    elif AlienMoveset.escaping in movesets:
        if self.center_x == ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x > ship_x:
            self.change_x = self.SPEED * delta_time
        elif self.center_x < ship_x:
            self.change_x = -self.SPEED * delta_time
