import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.loaders.alien import loader


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

        aliens_categories = loader()
        print(aliens_categories)
