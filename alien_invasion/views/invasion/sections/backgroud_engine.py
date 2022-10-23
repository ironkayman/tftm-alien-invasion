"""
Module for background management.
"""

from pathlib import Path

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

        self.background = self.load_new_background(
            CONSTANTS.DIR_RESOURCES / 'images/main_menu.png',
            90, 0.4
        )

    def load_new_background(self,
        texture: Path,
        upper_alpha: int,
        fadein_speed: float = 0.4
    ) -> arc.texture.Texture:
        """
        Parameters
        ----------
        texture: Path
            pathlib.Path path to an image.
            Consider RESOURCES constant.
        upper_texture_alpha: int
            Desired transperency background texture channel.
        fadein_speed: float = 0.4
            Desired fade-in speed for alpha channel per frame.
            Is incrimented in `.on_draw` method.
        """
        self.bg_alpha_reveal = 0
        self.bg_upper_alpha = upper_alpha
        self.bg_fadein_speed = fadein_speed
        return arc.load_texture(texture)

    def on_draw(self):
        """
        Render background section.
        """

        def compute_bg_fadein():
            if self.bg_alpha_reveal < self.bg_upper_alpha:
                self.bg_alpha_reveal += self.bg_fadein_speed

        compute_bg_fadein()
        # Draw the background texture
        arc.draw_lrwh_rectangle_textured(
            0, 0,
            CONSTANTS.DISPLAY.WIDTH,
            CONSTANTS.DISPLAY.HEIGHT,
            self.background,
            alpha=self.bg_alpha_reveal,
        )
