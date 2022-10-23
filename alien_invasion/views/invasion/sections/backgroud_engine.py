"""
Module for background management.
"""

import arcade as arc

from alien_invasion import CONSTANTS

class BackgroundEngine(arc.Section):
    """Gameplay loop background logic."""
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
            **kwargs
        )

        arc.set_background_color(arc.color.BLACK)

        self.background = arc.load_texture(
            CONSTANTS.DIR_RESOURCES / 'images/main_menu.png'
        )

    def on_draw(self):
        """
        Render background section.
        """

        # This command has to happen before we start drawing
        # self.clear()

        # Draw the background texture
        arc.draw_lrwh_rectangle_textured(
            0, 0,
            CONSTANTS.DISPLAY.WIDTH,
            CONSTANTS.DISPLAY.HEIGHT,
            self.background
        )
