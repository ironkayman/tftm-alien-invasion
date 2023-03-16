"""Logic for Alien spawners
"""

from typing import cast

import arcade as arc
from arcade import Particle


class AlienSpawner(arc.Emitter):
    """Implementation of Emitter specifically for Alien class particle.
    """

    def __init__(
        self,
        **emitter_kwargs,
    ) -> None:
        return super().__init__(**emitter_kwargs)

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
