"""Bullet Sprite class used to renderr bullets
"""

import arcade as arc


class Bullet(arc.Sprite):
    """Bullet class used for starship/alien firing

    Parameters
    ----------
    filename : str
        Path to sprite
    damage : int
        Bullet damage, taken from alien's state
        `bullet_damage`
    scale : float = 1
        Scale.
    angle : int = 0
        Sprite rotation
    """

    def __init__(
        self, filename: str, damage: int, scale: float = 1, angle: int = 0, **kwargs
    ):
        super().__init__(filename, scale, **kwargs)
        self.angle = angle
        self.damage = damage
