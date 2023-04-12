"""
Module for main_menu background management.
"""

from random import randrange

import arcade as arc

from alien_invasion import CONSTANTS


class Background(arc.Scene):
    """Background logic."""

    def __init__(self) -> None:
        """Animated backfround logic setup.
        
        Prepares 4 sprites as a background for
        UIManager at `human_interface` section.
        """
        super().__init__()

        arc.set_background_color(arc.color.BLACK)

        # unanimated background
        self.backfall = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/entry_ns.png'),
            scale=0.36 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 30,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        )
        self.backfall.color = (85, 70, 110)
        self.backfall.alpha = 170
        self.add_sprite_list(
            name='backfall',
            sprite_list=self.backfall,
        )


        # structure at screen center behind buttons
        self.cental_node = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_cold_crack.png'),
            scale=0.36 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 20,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        )
        self.add_sprite_list(
            name='central_node',
            sprite_list=self.cental_node,
        )


        # inner asteroids, should periodically float up-and-down
        self.asteroids_float = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_cold_asteroids.png'),
            scale=0.38 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 20,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2 + 40,
        )
        self.add_sprite_list(name='asteroids_float', sprite_list=self.asteroids_float)

        # outter asteroid circle, spins slowly
        self.asteroids_spin = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_cold_asteroids.png'),
            scale=0.58 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 40,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2 + 60,
            angle=-30,
        )
        # alternate color
        # self.asteroids_spin.color = (240, 220, 200)
        # make more bluish and darker tint
        self.asteroids_spin.color = (200, 220, 240)
        self.add_sprite_list(name='asteroids_spin', sprite_list=self.asteroids_spin)

        # variables for periodic center_y change of asteroids_float
        self.last_update_time = 0
        self.float_interval = 1.4

        # foreground
        self.foreground_castle_ruins = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_foreground.png'),
            scale=0.8 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 6,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 14,
            angle=-20,
        )

    def on_update(self, dt: float = 1 / 60) -> None:
        """Compute background layer changes."""
        # calculate inner astaroids elevation
        self.last_update_time += dt
        if self.last_update_time > self.float_interval:
            self.asteroids_float.center_y += randrange(-6, 6)
            self.last_update_time = 0

        # spin outer asteroids
        self.asteroids_spin.angle += 0.02
        # super().on_update(dt)

    def draw(self):
        """
        Render background section.
        """
        super().draw(pixelated=False)

        # draw under specific progression conditions
        #
        # golden frame
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            CONSTANTS.DISPLAY.HEIGHT // 2,
            CONSTANTS.DISPLAY.WIDTH - 20,
            CONSTANTS.DISPLAY.HEIGHT - 20,
            (237, 207, 80),
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )

        # golden columns
        # top wide
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            CONSTANTS.DISPLAY.HEIGHT - 20,
            320 * CONSTANTS.DISPLAY.SCALE_RELATION,
            160 * CONSTANTS.DISPLAY.SCALE_RELATION,
            (237, 207, 80),
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        # top long
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            CONSTANTS.DISPLAY.HEIGHT * 6/7,
            120 * CONSTANTS.DISPLAY.SCALE_RELATION,
            260 * CONSTANTS.DISPLAY.SCALE_RELATION,
            (237, 207, 80),
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            CONSTANTS.DISPLAY.HEIGHT * 5/6,
            80 * CONSTANTS.DISPLAY.SCALE_RELATION,
            300 * CONSTANTS.DISPLAY.SCALE_RELATION,
            (237, 207, 80),
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        # bottom
        arc.draw_rectangle_outline(
            CONSTANTS.DISPLAY.WIDTH // 2,
            CONSTANTS.DISPLAY.HEIGHT // 7,
            100 * CONSTANTS.DISPLAY.SCALE_RELATION,
            240 * CONSTANTS.DISPLAY.SCALE_RELATION,
            (237, 207, 80),
            1 * CONSTANTS.DISPLAY.SCALE_RELATION,
        )

        # render foreground over all golden arcs
        self.foreground_castle_ruins.draw(pixelated=False)
