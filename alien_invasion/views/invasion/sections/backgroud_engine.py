"""
Module for background management.
"""

from pathlib import Path
from timeit import repeat

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

        self.backgrounds = arc.SpriteList()

        images: list[arc.Sprite] = [
            arc.Sprite(
                CONSTANTS.DIR_RESOURCES / 'images/background/20150327144018-8ba5f9d2-me.png',
                scale=3, #repeat_count_y=3,
            ),
        ]

        # self.fadein_per_frame = 0.4
        # self.upper_bg_alpha = 140

        self.backgrounds.extend(images)

        self.backgrounds[0].change_y = -10
        # self.backgrounds[0].image_height = self.backgrounds[0].height * 2

        self.backgrounds[0].append_texture(self.backgrounds[0].texture)
        print(self.backgrounds[0].textures)

        # self.backgrounds[0].image_y = self.backgrounds[0].height * 2

    def on_update(self, dt):

        if self.backgrounds[0].top < 0:
            self.backgrounds[0].top = CONSTANTS.DISPLAY.HEIGHT
        else:
            self.backgrounds[0].bottom -= 10

        self.backgrounds.update()

    def on_draw(self):
        """
        Render background section.
        """

        # surf_h = surf.get_height()
        # rel_y = ypos % img_rect.height
        # surf.blit(img, (0, rel_y - img_rect.height))

        # if rel_y < surf_h:
        #     surf.blit(img, (0, rel_y))

        self.backgrounds.draw(pixelated=False)
        # Draw the background texture
        # arc.draw_lrwh_rectangle_textured(
        #     0, 0,
        #     CONSTANTS.DISPLAY.WIDTH,
        #     CONSTANTS.DISPLAY.HEIGHT,
        #     self.background,
        #     alpha=self.bg_alpha_reveal,
        # )
