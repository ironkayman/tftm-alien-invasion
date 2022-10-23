"""
Module for background management.
"""

from pathlib import Path
from timeit import repeat

import arcade as arc

from alien_invasion import CONSTANTS



class BackgroundEngine(arc.Section):
    """Background logic."""

    def __init__(
        self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        **kwargs,
    ) -> None:
        """
        Initialise background images.
        """
        super().__init__(
            left,
            bottom,
            width,
            height,
            **kwargs
        )

        arc.set_background_color(arc.color.BLACK)

        self.backgrounds = arc.SpriteList()

        bg_pair = arc.load_texture_pair(CONSTANTS.DIR_RESOURCES / 'images/background/20150327144347-2dca2987-me.png')
        sprites: list[arc.Sprite] = [
            arc.Sprite(
                texture=bg_pair[0], scale=3,
            ),
            arc.Sprite(
                texture=bg_pair[1], scale=3,
            ),
        ]

        # self.fadein_per_frame = 0.4
        # self.upper_bg_alpha = 250

        self.backgrounds.extend(sprites)
        self.backgrounds.alpha = 110

        # velocity
        self.backgrounds[0].change_y = -0.2
        self.backgrounds[1].change_y = self.backgrounds[0].change_y

        # position 1 above 0 for the first update_l1 iteration loop
        self.backgrounds[1].bottom = self.backgrounds[0].top

    def on_update(self, dt) -> None:
        """Compute background layer changes."""

        def update_layer_3() -> None:
            """
            Repositions textures of layer 3 background.

            When first img 0 reaches bottom, move above it an img 1,
            then then img 1 reaches bottom, move above it an img 0
            """
            if self.backgrounds[0].bottom < 0:
                self.backgrounds[1].bottom = self.backgrounds[0].top
            if self.backgrounds[1].bottom < 0:
                self.backgrounds[0].bottom = self.backgrounds[1].top

        update_layer_3()
        self.backgrounds.update()


    def on_draw(self):
        """
        Render background section.
        """

        # Draw the background texture
        self.backgrounds.draw(pixelated=True)

        # arc.draw_lrwh_rectangle_textured(
        #     0, 0,
        #     CONSTANTS.DISPLAY.WIDTH,
        #     CONSTANTS.DISPLAY.HEIGHT,
        #     self.background,
        #     alpha=self.bg_alpha_reveal,
        # )
