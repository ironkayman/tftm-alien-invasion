"""Logic for Alien spawners
"""

from typing import cast
from itertools import filterfalse
from functools import partial


import arcade as arc
from arcade import Particle

from alien_invasion.entities import Alien


class AlienSpawner(arc.Emitter):
    """Implementation of Emitter specifically for Alien class particle.
    """

    def __init__(
        self,
        starship,
        **emitter_kwargs,
    ) -> None:
        super().__init__(**emitter_kwargs)
        self.starship = starship

    def on_update(self, delta_time: float) -> None:
        """Impliments on_update method on par with standard .update
        """
        # update emitter
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        # update particles
        emit_count = self.rate_factory.how_many(1 / 60, len(self._particles))
        for _ in range(emit_count):
            self._emit()
        # notice
        self._particles.on_update(delta_time)
        aliens_to_reap: list[Alien] = [p for p in self._particles if cast(Particle, p).can_reap()]
        for alien in aliens_to_reap:
            if not (alien.top <= 0):
                self.starship.xp += alien.config.info.xp
            alien.kill()

    # def _emit(self):
    #     """Emit one particle, its initial position and velocity are relative to the position and angle of the emitter"""
    #     p = self.particle_factory(self)
    #     p.center_x += self.center_x
    #     p.center_y += self.center_y

    #     # given the velocity, rotate it by emitter's current angle
    #     vel = _Vec2(p.change_x, p.change_y).rotated(self.angle)

    #     p.change_x = vel.x
    #     p.change_y = vel.y
    #     self._particles.append(p)

    def draw(self, pixelated=False):
        self._particles.draw(pixelated=pixelated, filter=arc.gl.NEAREST)
