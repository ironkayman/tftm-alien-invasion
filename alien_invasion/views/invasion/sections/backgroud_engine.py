"""
Module for background management.
"""

from pathlib import Path

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
        Initialise background images/particle layers.
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

        def create_layer_microcomets():
            """Create layers of rare but fast moving objects."""
            return arc.Emitter(
                center_xy=(0, CONSTANTS.DISPLAY.HEIGHT),
                emit_controller=arc.EmitInterval(0.6),
                particle_factory=lambda emitter: arc.LifetimeParticle(
                    filename_or_texture=":resources:images/pinball/pool_cue_ball.png",
                    change_xy=(0.0, -35.0),
                    lifetime=5,
                    center_xy=arc.rand_on_line(
                        (0.0, 0.0),
                        (CONSTANTS.DISPLAY.WIDTH, CONSTANTS.DISPLAY.HEIGHT)
                    ),
                    scale=0.1,
                    alpha=35
                )
            )

        def create_layer_stardust():
            """Creates moving particle background.

            Create second moving layer above
            background image, slightly faster than it.
            """
            return arc.Emitter(
                center_xy=(0, CONSTANTS.DISPLAY.HEIGHT),
                emit_controller=arc.EmitInterval(0.75),
                particle_factory=lambda emitter: arc.LifetimeParticle(
                    filename_or_texture=":resources:images/tiles/dirtCenter.png",
                    change_xy=(0.0, -0.12),
                    lifetime=120,
                    center_xy=arc.rand_on_line(
                        (0.0, 0.0),
                        (CONSTANTS.DISPLAY.WIDTH, CONSTANTS.DISPLAY.HEIGHT)
                    ),
                    scale=0.04,
                    alpha=15
                )
            )

        def create_background_rolling_image_layer():
            bg_pair = arc.load_texture_pair(
                CONSTANTS.DIR_RESOURCES / 'images/background/20150327144347-2dca2987-me.png'
            )
            sprites: list[arc.Sprite] = [
                arc.Sprite(
                    texture=bg_pair[0], scale=3,
                ),
                arc.Sprite(
                    texture=bg_pair[1], scale=3,
                ),
            ]

            self.backgrounds.extend(sprites)
            self.backgrounds.alpha = 110

            # velocity
            self.backgrounds[0].change_y = -0.05
            self.backgrounds[1].change_y = self.backgrounds[0].change_y

            # position 1 above 0 for the first update_l1 iteration loop
            self.backgrounds[1].bottom = self.backgrounds[0].top

        create_background_rolling_image_layer()
        self.emitter_stardust = create_layer_stardust()
        self.emitter_microcomet = create_layer_microcomets()

    def on_update(self, dt) -> None:
        """Compute background layer changes."""

        def compute_viewport_layer_3() -> None:
            """
            Reposition textures of layer 3/image background.

            When first img 0 reaches bottom, move above it an img 1,
            then then img 1 reaches bottom, move above it an img 0
            """
            if self.backgrounds[0].bottom < 0:
                self.backgrounds[1].bottom = self.backgrounds[0].top
            if self.backgrounds[1].bottom < 0:
                self.backgrounds[0].bottom = self.backgrounds[1].top

        # compute image shifting against veiwport
        compute_viewport_layer_3()
        # call emitters
        self.emitter_stardust.update()
        self.emitter_microcomet.update()
        # update computes background
        self.backgrounds.update()


    def on_draw(self):
        """
        Render background section.
        """

        # Draw the background texture
        self.backgrounds.draw(pixelated=True)
        # render emitted particles
        self.emitter_stardust.draw()
        self.emitter_microcomet.draw()

