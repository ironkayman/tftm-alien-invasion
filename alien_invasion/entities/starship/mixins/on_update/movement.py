"""On_update extension for movement logic
"""

from alien_invasion import CONSTANTS

from ...constants import LastDirection

def on_update_movement(self, delta_time: float):
    """Transmission-based sprite movement updater.
    
    Since its a ViewModel all external logic is moved here
    for maximasing variables availability for interacting with
    environment and other entitties.
    
    `self.moving_left` and `self.moving_right` is set inside Section
    with `key_down` and `key_up` events.
    """

    motion = (self.moving_left, self.moving_right)

    # standart movement behavior
    if not self.free_falling:
        self._timers.outage = 0
        # last movement direction for cahnge of outage
        # this caises to free fall in that direction
        if self.moving_left:
            self.last_direction = LastDirection.LEFT
        if self.moving_right:
            self.last_direction = LastDirection.RIGHT
        if all(motion) or not any(motion):
            self.last_direction = LastDirection.STATIONARY

        # basic L/R movement
        if self.moving_left and not self.transmission.throttle:
            self.change_x = -self.speed * delta_time
        if self.moving_right and not self.transmission.throttle:
            self.change_x = self.speed * delta_time

        # slow down while approching to left border
        if self.moving_left and self.transmission.throttle and self.transmission.border_reached_left:
            self.change_x = -self.speed // 3 * delta_time
            # stop inside a wall
            if self.left < self.movement_borders.left - self.width * 0.3:
                self.stop()
        # slow down while approching to right border
        elif self.moving_right and self.transmission.throttle and self.transmission.border_reached_right:
            self.change_x = self.speed // 3 * delta_time
            # stop inside a wall
            if self.right > self.movement_borders.right + self.width * 0.3:
                self.stop()

        # stop at no movement or both L and R
        if not self.transmission.throttle:
            if (all(motion) or not any(motion)):
                self.stop()
        # exit
        # ---------------------------------------
        return

    # control free fall
    # ---------------------------------
    # last movement at low energy was LEFT
    # -> free fall LEFT
    if self.last_direction == LastDirection.LEFT:
        self.change_x = -self.speed // 3 * delta_time
        # stop inside a wall if deep inside it
        if self.left < self.movement_borders.left - self.width * 0.3:
            self.stop()
        # reverse reaching wall without slowing down
        elif self.transmission.border_reached_left:
            self.last_direction = LastDirection.RIGHT
    # last movement at low energy was RIGHT
    # -> free fall RIGHT
    elif self.last_direction == LastDirection.RIGHT:
        self.change_x = self.speed // 3 * delta_time
        # stop inside a wall if deep inside it
        if self.right > self.movement_borders.right + self.width * 0.3:
            self.stop()
        # reverse reaching wall without slowing down
        elif self.transmission.border_reached_right:
            self.last_direction = LastDirection.LEFT
