"""
Module for background management.
"""

from pathlib import Path

import arcade as arc

from alien_invasion import CONSTANTS


class BackgroundImage(arc.Sprite):
    """Background image wrapper

    Used fot wrappig [copyrighted content]
    Observatory taken images due to their size.

    Attributes
    ----------
    pixelated: bool
        Make class images pixeletad when drawn.
    """

    pixelated: bool = True

    def __init__(self, texture, scale: float|int) -> None:
        """Initialise preset center_* values by `scale`.

        Default position is bottom-left of the screen (0,0)
        """
        scale=3 # ->
        center_x = 0
        center_y = 0
        # scale=1.5, ->
        # center_x = CONSTANTS.DISPLAY.WIDTH // 2,
        # center_y = CONSTANTS.DISPLAY.HEIGHT // 2,
        super().__init__(
            texture=texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
        )


class Background(arc.Scene):
    """Background logic."""

    def __init__(self, level_title_image_path: Path) -> None:
        """
        Initialise background images/particle layers.
        """
        super().__init__()

        arc.set_background_color(arc.color.BLACK)

        self.backgrounds = arc.SpriteList()

        def create_layer_microcomets() -> arc.Emitter:
            """Create layers of rare but fast moving objects."""
            return arc.Emitter(
                center_xy=(0, CONSTANTS.DISPLAY.HEIGHT),
                emit_controller=arc.EmitInterval(0.75),
                particle_factory=lambda emitter: arc.LifetimeParticle(
                    filename_or_texture=":resources:images/pinball/pool_cue_ball.png",
                    change_xy=(0.0, -16.0),
                    lifetime=5,
                    center_xy=arc.rand_on_line(
                        (0.0, 0.0),
                        (CONSTANTS.DISPLAY.WIDTH, 0.0)
                    ),
                    scale=0.1,
                    alpha=40
                )
            )

        def create_layer_stardust_primary() -> arc.Emitter:
            """Creates relatively faster moving particle background.

            Create primary moving layer above
            background image, slightly faster than it.
            """
            return arc.Emitter(
                center_xy=(0, CONSTANTS.DISPLAY.HEIGHT),
                emit_controller=arc.EmitInterval(0.9),
                particle_factory=lambda emitter: arc.LifetimeParticle(
                    filename_or_texture=":resources:images/tiles/dirtCenter.png",
                    change_xy=(0.0, -1.5),
                    lifetime=180,
                    center_xy=arc.rand_on_line(
                        (0.0, 0.0),
                        (CONSTANTS.DISPLAY.WIDTH, 0.0)
                    ),
                    scale=0.04,
                    alpha=60,
                )
            )

        def create_layer_stardust_secondary() -> arc.Emitter:
            """Creates slower moving particle background.

            Create secondary and more slow layer above
            background image, slightly faster than it.
            """
            return arc.Emitter(
                center_xy=(0, CONSTANTS.DISPLAY.HEIGHT),
                emit_controller=arc.EmitInterval(0.6),
                particle_factory=lambda emitter: arc.LifetimeParticle(
                    filename_or_texture=":resources:images/tiles/dirtCenter.png",
                    change_xy=(0.0, -1.0),
                    lifetime=240,
                    center_xy=arc.rand_on_line(
                        (0.0, 0.0),
                        (CONSTANTS.DISPLAY.WIDTH, 0.0)
                    ),
                    scale=0.04,
                    alpha=30
                )
            )

        def create_background_rolling_image_layer() -> None:
            bg_pair = arc.load_texture_pair(
                CONSTANTS.DIR_RESOURCES / 'images/background/20150327144347-2dca2987-me.png'
            )
            sprites: list[arc.Sprite] = [
                BackgroundImage(texture=bg_pair[0], scale=1.2),
                BackgroundImage(texture=bg_pair[1], scale=1.2),
            ]

            self.backgrounds.extend(sprites)
            self.backgrounds.alpha = 80

            # velocity
            self.backgrounds[0].change_y = -0.6
            self.backgrounds[1].change_y = self.backgrounds[0].change_y

            # position 1 above 0 for the first update_l1 iteration loop
            self.backgrounds[1].bottom = self.backgrounds[0].top

        create_background_rolling_image_layer()

        self.title_sprite = BackgroundImage(texture=arc.load_texture(level_title_image_path), scale=0.2),
        self.title_sprite[0].center_x = CONSTANTS.DISPLAY.WIDTH // 2
        self.title_sprite[0].center_y = CONSTANTS.DISPLAY.HEIGHT * 4/5
        self.title_sprite[0].scale = 0.78
        self.title_sprite[0].alpha = 210

        self.emitter_stardust_secondary = create_layer_stardust_secondary()
        self.emitter_stardust_primary = create_layer_stardust_primary()
        self.emitter_microcomet = create_layer_microcomets()

    def on_update(self, _: float = 1 / 60) -> None:
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
        [layer.update() for layer in (
            self.emitter_stardust_secondary,
            self.emitter_stardust_primary,
            self.emitter_microcomet,
            self.backgrounds,)]

    def draw(self):
        """
        Render background section.
        """

        # Draw the background texture
        self.backgrounds.draw(pixelated=BackgroundImage.pixelated)
        # render emitted particles
        [layer.draw() for layer in (
            self.title_sprite[0],
            self.emitter_stardust_secondary,
            self.emitter_stardust_primary,
            self.emitter_microcomet,)]

