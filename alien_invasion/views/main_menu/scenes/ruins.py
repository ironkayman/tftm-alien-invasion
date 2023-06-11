"""
Module for Main Menu's Ruins foreground management
"""

from random import randrange

import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.animations import SpriteTimed


class RuinsBackground(SpriteTimed):
    """Ruins' background sprite animations"""

    def timed_update(self) -> None:
        self.center_y += randrange(-3, 3)


class RuinsCathedral(SpriteTimed):
    """Ruins' cathedral sprite animations"""

    def timed_update(self) -> None:
        self.center_y += randrange(-2, 2)


class RuinsTemple(SpriteTimed):
    """Ruins' temple sprite animations"""

    def timed_update(self) -> None:
        self.center_y += randrange(-2, 2)


class Ruins(arc.Scene):
    """Manager for foreground's Ruins"""

    def __init__(self) -> None:
        super().__init__()

        self._dir_images = CONSTANTS.DIR_IMAGES.joinpath("menu/foreground")
        self.__ruins_scaling = 0.26 * CONSTANTS.DISPLAY.SCALE_RELATION

        def init_ruins_bg() -> None:
            self.ruins_background = RuinsBackground(
                filename=self._dir_images / "ruins_bg.png",
                scale=self.__ruins_scaling,
                timer_interval=6.6,
            )
            self.ruins_background.left = 0
            self.ruins_background.top = CONSTANTS.DISPLAY.HEIGHT
            self.add_sprite_list(
                name="ruins_background",
                sprite_list=self.ruins_background,
            )

        def init_ruins_cathedral() -> None:
            self.ruins_cathedral = RuinsCathedral(
                filename=self._dir_images / "ruins_cathedral.png",
                scale=self.__ruins_scaling,
                timer_interval=4.6,
            )
            self.ruins_cathedral.bottom = -20 * CONSTANTS.DISPLAY.SCALE_RELATION
            self.ruins_cathedral.left = 9.8 * CONSTANTS.DISPLAY.SCALE_RELATION
            self.add_sprite_list(
                name="ruins_cathedral",
                sprite_list=self.ruins_cathedral,
            )

        def init_ruins_temple() -> None:
            self.ruins_temple = RuinsTemple(
                filename=self._dir_images / "ruins_temple.png",
                scale=self.__ruins_scaling,
                timer_interval=3.4,
            )
            self.ruins_temple.bottom = -22 * CONSTANTS.DISPLAY.SCALE_RELATION
            self.ruins_temple.left = CONSTANTS.DISPLAY.WIDTH / 4.2
            self.add_sprite_list(
                name="ruins_temple",
                sprite_list=self.ruins_temple,
            )

        def init_ruins_wall() -> None:
            self.ruins_wall = arc.Sprite(
                filename=self._dir_images / "ruins_wall.png",
                scale=self.__ruins_scaling,
            )
            self.ruins_wall.top = CONSTANTS.DISPLAY.HEIGHT
            self.ruins_wall.left = 0
            self.add_sprite_list(
                name="ruins_wall",
                sprite_list=self.ruins_wall,
            )

        init_ruins_bg()
        init_ruins_cathedral()
        init_ruins_wall()
        init_ruins_temple()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.ruins_background.on_update(delta_time)
        self.ruins_cathedral.on_update(delta_time)
        self.ruins_temple.on_update(delta_time)
        # ruins_wall needs no update since it isn't animated
