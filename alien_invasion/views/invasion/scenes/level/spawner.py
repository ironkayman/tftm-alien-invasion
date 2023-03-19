"""Logic for Alien spawners
"""

from typing import cast
from functools import partial


import arcade as arc
from arcade import Particle


class AlienSpawner(arc.Emitter):
    """Implementation of Emitter specifically for Alien class particle.
    """

    def __init__(
        self,
        **emitter_kwargs,
    ) -> None:
        super().__init__(**emitter_kwargs)
        # makes it possible to pass parent sprite list
        self.particle_factory = partial(
            self.particle_factory,
            parent_sprite_list=self._particles
        )

    def on_update(self, delta_time):
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
        particles_to_reap = [p for p in self._particles if cast(Particle, p).can_reap()]
        for dead_particle in particles_to_reap:
            dead_particle.kill()

    def draw(self, pixelated=False):
        self._particles.draw(pixelated=pixelated)