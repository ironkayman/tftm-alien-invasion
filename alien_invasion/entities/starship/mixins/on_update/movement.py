"""On_update extension for movement logic
"""
from typing import cast

from ...constants import LastDirection


def on_update_movement(self, delta_time: float):
    """Transmission-based sprite movement updater.

    Since its a ViewModel all external logic is moved here
    for maximasing variables availability for interacting with
    environment and other entitties.

    `self.moving_left` and `self.moving_right` is set inside Section
    with `key_down` and `key_up` events.
    """
    from ...starship import Starship

    self = cast(Starship, self)

    motion = (
        self.moving_left,
        self.moving_right,
        self.moving_up,
        self.moving_down,
    )

    # standart movement behavior
    if not self.free_falling:
        self._timers.outage = 0
        # last movement direction for cahnge of outage
        # this caises to free fall in that direction
        if self.moving_left:
            self.last_direction = LastDirection.LEFT
        if self.moving_right:
            self.last_direction = LastDirection.RIGHT
        if all(motion[0:2]) or not any(motion[0:2]):
            self.last_direction = LastDirection.STATIONARY

        # basic L/R movement
        if self.moving_left and not self.transmission.throttle:
            self.change_x = -self.speed * delta_time
        if self.moving_right and not self.transmission.throttle:
            self.change_x = self.speed * delta_time
        # TODO: move multiplier to external item's property
        # it should be lower than the usual speed
        if self.moving_up and not self.transmission.throttle:
            self.change_y = self.speed * 0.6 * delta_time
        if self.moving_down and not self.transmission.throttle:
            self.change_y = -self.speed * 0.6 * delta_time

        # slow down while approching to left border
        if (
            self.moving_left
            and self.transmission.throttle
            and self.transmission.border_reached_left
        ):
            self.change_x = -self.speed // 3 * delta_time
            # stop inside a wall
            if self.left < self.movement_borders.left - self.width * 0.3:
                self.stop()
        # slow down while approching to right border
        elif (
            self.moving_right
            and self.transmission.throttle
            and self.transmission.border_reached_right
        ):
            self.change_x = self.speed // 3 * delta_time
            # stop inside a wall
            if self.right > self.movement_borders.right + self.width * 0.3:
                self.stop()

        # stop at no movement or both L and R or U and D
        if not self.transmission.throttle:
            # decouple horizontal and vertical controls
            if all((self.moving_left, self.moving_right)) or not any(
                (self.moving_left, self.moving_right)
            ):
                self.change_x = 0
            if all((self.moving_up, self.moving_down)) or not any(
                (self.moving_up, self.moving_down)
            ):
                self.change_y = 0
            if any(
                (
                    all(motion),
                    not any(motion),
                )
            ):
                self.stop()

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
            self.change_x = 0
        # reverse reaching wall without slowing down
        elif self.transmission.border_reached_left:
            self.last_direction = LastDirection.RIGHT
    # last movement at low energy was RIGHT
    # -> free fall RIGHT
    elif self.last_direction == LastDirection.RIGHT:
        self.change_x = self.speed // 3 * delta_time
        # stop inside a wall if deep inside it
        if self.right > self.movement_borders.right + self.width * 0.3:
            self.change_x = 0
        # reverse reaching wall without slowing down
        elif self.transmission.border_reached_right:
            self.last_direction = LastDirection.LEFT

    # tmp_dir = 1
    # if self.change_y < 0:
    #     tmp_dir = -1
    # elif self.change_y == 0:
    #     tmp_dir = 0
    self.change_y = 0
    # self.change_y = -1 * self.speed * 0.6 * delta_time
    # if self.bottom < 0:
    #     self.change_y = 0
    # elif self.top > CONSTANTS.DISPLAY.HEIGHT:
    #     self.change_y = -self.speed * 0.6 * delta_time
