import arcade as arc

from alien_invasion.utils.loaders.alien import loader
from alien_invasion.entities import Alien

from alien_invasion import CONSTANTS

"""
Alien spawner - chain of moving emitters for particles, but particles are aliens
also they cant overlap and should find pathfinding
"""

class AlienArea(arc.Scene):
    """Aliens' area of movement."""
    def __init__(self) -> None:
        super().__init__()

        self.aliens_types: arc.SpriteList = arc.SpriteList()
        self.aliens_bullet_list: arc.SpriteList = arc.SpriteList()

        alien_categories = loader()
        for config in alien_categories:
            alien = Alien(config)
            self.aliens_types.append(alien)

        self.add_sprite_list(
            name='aliens_types',
            sprite_list=self.aliens_types,
        )
        self.spawner = arc.Emitter(
            center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT // 2),
            emit_controller=arc.EmitInterval(0.02),
            particle_factory=lambda emitter: Alien(
                config=config,
                change_xy= arc.rand_in_circle((0.0, 0.0), 10),
            )  # type: ignore
        )
        # dont add sprite list to scene since spawner counts it
        # self.add_sprite_list(
        #     name='aliens',
        #     sprite_list=self.spawner._particles,
        # )
        self.aliens = self.spawner._particles

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""

        if self.spawner:
            self.spawner.update()
        print('aliens:', self.spawner.get_count())



    def draw(self):
        """
        Render background section.
        """
        self.spawner.draw()
        super().draw(pixelated=True)