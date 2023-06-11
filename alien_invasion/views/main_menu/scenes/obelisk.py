"""
Module for Main Menu's background sprite management
"""

from random import randrange

import arcade as arc

from alien_invasion import CONSTANTS


class Obelisk(arc.Scene):
    """Background Obelisk manager"""

    def __init__(self) -> None:
        """Animated backfround logic setup."""
        super().__init__()

        arc.set_background_color(arc.color.BLACK)

        # unanimated background
        self.clouds = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath("menu/background/clouds.png"),
            scale=0.36 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 30,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        )
        self.clouds.color = (85, 70, 110)
        self.clouds.alpha = 170
        self.add_sprite_list(
            name="clouds",
            sprite_list=self.clouds,
        )

        # structure at screen center behind buttons
        self.obelisk_pillar = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath(
                "menu/background/obelisk_pillars.png"
            ),
            scale=0.36 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 20,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        )
        self.add_sprite_list(
            name="obelisk_pillar",
            sprite_list=self.obelisk_pillar,
        )

        # inner asteroids, should periodically float up-and-down
        self.asteroids_float = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath(
                "menu/background/obelisk_fragments.png"
            ),
            scale=0.38 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 20,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2 + 40,
        )
        self.add_sprite_list(name="asteroids_float", sprite_list=self.asteroids_float)

        # outter asteroid circle, spins slowly
        self.asteroids_spin = arc.Sprite(
            filename=CONSTANTS.DIR_IMAGES.joinpath(
                "menu/background/obelisk_fragments.png"
            ),
            scale=0.58 * CONSTANTS.DISPLAY.SCALE_RELATION,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 40,
            center_y=CONSTANTS.DISPLAY.HEIGHT // 2 + 60,
            angle=-30,
        )
        # alternate color
        # self.asteroids_spin.color = (240, 220, 200)
        # make more bluish and darker tint
        self.asteroids_spin.color = (200, 220, 240)
        self.add_sprite_list(name="asteroids_spin", sprite_list=self.asteroids_spin)

        # variables for periodic center_y change of asteroids_float
        self.last_update_time = 0
        self.float_interval = 1.4

        # foreground
        # self.foreground_castle_ruins = arc.Sprite(
        #     filename=CONSTANTS.DIR_IMAGES.joinpath(
        #         "background/main_menu_foreground_new.png"
        #     ),
        #     scale=0.26 * CONSTANTS.DISPLAY.SCALE_RELATION,
        #     center_x=CONSTANTS.DISPLAY.WIDTH // 3,
        #     center_y=CONSTANTS.DISPLAY.HEIGHT // 2,
        #     angle=0,
        # )
        # self.foreground_castle_ruins.left = 0
        # self.foreground_castle_ruins.top = CONSTANTS.DISPLAY.HEIGHT

    def on_update(self, dt: float = 1 / 60) -> None:
        """Compute background layer changes."""
        # calculate inner astaroids elevation
        self.last_update_time += dt
        if self.last_update_time > self.float_interval:
            self.asteroids_float.center_y += randrange(-6, 6)
            self.last_update_time = 0

        # spin outer asteroids
        self.asteroids_spin.angle += 0.02

    def draw(self):
        """
        Render background section.
        """
        super().draw(pixelated=True)

        # render foreground over all golden arcs
        # self.foreground_castle_ruins.draw(pixelated=False)
