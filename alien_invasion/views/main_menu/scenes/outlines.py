"""
Module for main_menu background management.
"""

import arcade as arc

from alien_invasion import CONSTANTS


class Outlines(arc.Scene):
    """Foreground outlines manager"""

    OUTLINE_COLOR = (237, 207, 80)

    def __init__(self) -> None:
        """Animated backfround logic setup."""
        super().__init__()

        self.last_update_time = 0
        # time interval between moveming blocks
        self.float_interval = 0.6
        # index of moving block during the interval,
        # is increased per interval
        self.float_interval_repeat = 6
        # counter for current index of float_interval_repeat
        # negative value adds slight delay when app starts
        self.float_interval_repeat_counter = -2
        # self.vertical_movement_step is multiplied by it
        # so movement can be done up or down
        self.movement_direction = 1
        # step in pixels for every block mvement per interval
        self.vertical_movement_step = 4 * CONSTANTS.DISPLAY.SCALE_RELATION

        self.position_top_wide = CONSTANTS.DISPLAY.HEIGHT - 20
        self.position_top_vertical_middle = CONSTANTS.DISPLAY.HEIGHT * 6 / 7 + 15
        self.position_top_vertical_center = CONSTANTS.DISPLAY.HEIGHT * 5 / 6
        self.position_bottom_vertical = CONSTANTS.DISPLAY.HEIGHT // 7

    def on_update(self, dt: float = 1 / 60) -> None:
        """Compute background layer changes."""
        self.last_update_time += dt

        if self.float_interval_repeat_counter == self.float_interval_repeat:
            self.movement_direction *= -1
            self.float_interval_repeat_counter = 0

        if self.last_update_time > self.float_interval:
            # self.movement_direction *= -1
            movement = self.movement_direction * self.vertical_movement_step
            self.last_update_time = 0

            if self.float_interval_repeat_counter == 4:
                self.position_top_vertical_center += movement
            elif self.float_interval_repeat_counter == 2:
                self.position_top_vertical_middle += movement
                self.position_bottom_vertical += movement
            elif self.float_interval_repeat_counter == 0:
                self.position_top_wide += movement

            self.float_interval_repeat_counter += 1

    def draw(self):
        """
        Render background section.
        """
        # golden frame
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            CONSTANTS.DISPLAY.HEIGHT // 2,
            CONSTANTS.DISPLAY.WIDTH - 20,
            CONSTANTS.DISPLAY.HEIGHT - 20,
            Outlines.OUTLINE_COLOR,
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )

        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            self.position_top_wide,
            320 * CONSTANTS.DISPLAY.SCALE_RELATION,
            160 * CONSTANTS.DISPLAY.SCALE_RELATION,
            Outlines.OUTLINE_COLOR,
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            self.position_top_vertical_middle,
            120 * CONSTANTS.DISPLAY.SCALE_RELATION,
            260 * CONSTANTS.DISPLAY.SCALE_RELATION,
            Outlines.OUTLINE_COLOR,
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            self.position_top_vertical_center,
            80 * CONSTANTS.DISPLAY.SCALE_RELATION,
            300 * CONSTANTS.DISPLAY.SCALE_RELATION,
            Outlines.OUTLINE_COLOR,
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            self.position_bottom_vertical,
            100 * CONSTANTS.DISPLAY.SCALE_RELATION,
            240 * CONSTANTS.DISPLAY.SCALE_RELATION,
            Outlines.OUTLINE_COLOR,
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
