import arcade as arc

from alien_invasion import CONSTANTS

"""
Alien spawner - chain of moving emitters for particles, but particles are aliens
also they cant overlap and should find pathfinding
"""

class AlienArea(arc.Section):
    """Aliens' area of movement."""
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

        self.aliens: arc.SpriteList = arc.SpriteList()
        self.aliens_bullet_list: arc.SpriteList = arc.SpriteList()
