"""
Module for main_menu background management.
"""

from random import randrange
from pathlib import Path

import arcade as arc

from alien_invasion import CONSTANTS


class Background(arc.Section):
    """Background logic."""

    def __init__(
        self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        **kwargs,
    ) -> None:
        super().__init__(
            left,
            bottom,
            width,
            height,
            **kwargs,
            accept_keyboard_events=False,
        )

        arc.set_background_color(arc.color.BLACK)

        self.background_layers = arc.SpriteList()

        # unanimated background
        self.backfall = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/entry_ns.png'),
            scale=0.36,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 30,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        )
        self.backfall.color = (85, 70, 110)
        self.backfall.alpha = 170
        self.background_layers.append(self.backfall)


        # cold center structure
        self.cental_node = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_cold_crack.png'),
            scale=0.36,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 20,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        )
        # self.cental_node.color = (231, 221, 200)
        self.background_layers.append(self.cental_node)


        # inner asteroids, should periodically float up-down
        self.asteroids_float = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_cold_asteroids.png'),
            scale=0.38,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 20,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2 + 40,
        )
        self.background_layers.append(self.asteroids_float)

        # outter asteroid circle, spins slowly
        self.asteroids_spin = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath('background/main_menu_cold_asteroids.png'),
            scale=0.58,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 40,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2 + 60,
            angle=-30,
        )
        # self.asteroids_spin.color = (240, 220, 200)
        self.asteroids_spin.color = (200, 220, 240)
        self.background_layers.append(self.asteroids_spin)

        # variables for periodic center_y change of asteroids_float
        self.last_update_time = 0
        self.float_interval = 1.4

    def on_update(self, dt: float = 1 / 60) -> None:
        """Compute background layer changes."""
        self.last_update_time += dt
        if self.last_update_time > self.float_interval:
            self.asteroids_float.center_y += randrange(-6, 6)
            self.last_update_time = 0

        self.asteroids_spin.angle += 0.02

    def on_draw(self):
        """
        Render background section.
        """
        self.background_layers.draw(pixelated=False)
