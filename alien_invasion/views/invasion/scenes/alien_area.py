import arcade as arc

from alien_invasion.utils.loaders.alien import loader
from alien_invasion.entities import Alien


"""
Alien spawner - chain of moving emitters for particles, but particles are aliens
also they cant overlap and should find pathfinding
"""

class AlienArea(arc.Scene):
    """Aliens' area of movement."""
    def __init__(self) -> None:
        super().__init__()

        self.aliens: arc.SpriteList = arc.SpriteList()
        self.aliens_bullet_list: arc.SpriteList = arc.SpriteList()

        alien_categories = loader()
        for config in alien_categories:
            alien = Alien(config)
            self.aliens.append(alien)

        self.add_sprite_list(
            name='aliens',
            sprite_list=self.aliens,
        )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""
        for alien in self.aliens:
            alien.on_update(delta_time)


    def draw(self):
        """
        Render background section.
        """
        super().draw(pixelated=True)