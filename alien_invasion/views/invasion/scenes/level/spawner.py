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
        # notice:
        # self._particles.on_update(delta_time)
        aliens_to_reap: list[Alien] = [p for p in self._particles if cast(Particle, p).can_reap()]
        for alien in aliens_to_reap:
            if not (alien.top <= 0):
                self.starship.xp += alien.config.info.xp
            alien.kill()

    def draw(self, pixelated=False):
        self._particles.draw(pixelated=pixelated, filter=arc.gl.NEAREST)
