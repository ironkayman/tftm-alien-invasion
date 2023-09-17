"""Logic for Alien spawners
"""

from typing import Callable

import arcade as arc

# from alien_invasion.entities import Alien
from alien_invasion.utils.loaders.level.model import AlienSpawnConfiguration
from alien_invasion.entities import Alien

from alien_invasion import CONSTANTS


class AlienSpawner(arc.Emitter):
    """Implementation of Emitter specifically for Alien class particle."""

    def __init__(
        self,
        config: AlienSpawnConfiguration,
    ) -> None:
        self._config = config

        rate = self._config.spawn_rates.rate
        emit_controller = arc.EmitInterval(rate / 60)
        # overrides
        if (max_count := self._config.spawn_rates.max_count):
            emit_controller = arc.EmitMaintainCount(max_count)

        super().__init__(
            center_xy=(
                CONSTANTS.DISPLAY.WIDTH,
                CONSTANTS.DISPLAY.HEIGHT + 20
            ),
            emit_controller=emit_controller,
            particle_factory=self.__alien_factory,
        )
        # self.particle_factory = self.__alien_factory

    def __alien_factory(self, emitter: arc.Emitter) -> Alien:
        return Alien(
            # config=alien_config.config,
            # approach_velocity_multiplier=alien_config.spawner.approach_velocity_multiplier,
            # relative to emitter's center_xy
            center_xy=arc.rand_on_line(
                (-CONSTANTS.DISPLAY.WIDTH // 2, 0),
                (CONSTANTS.DISPLAY.WIDTH // 2, 0),
            ),
            hit_effect_list=self.alien_was_hit_effect_particles,
            # starship=self.starship,
            alien_bullets=self.alien_bullets,
            change_xy=arc.rand_vec_spread_deg(
                -90, 12, 1 * CONSTANTS.DISPLAY.SCALE_RELATION
            ),
            parent_sprite_list=emitter._particles,
            scale=self._config.scale,
            angle=(arc.rand_angle_360_deg()
                if self._config.spawn_random_rotation
                else 0
            ),
        )

    def on_update(self, delta_time: float) -> None:
        """Impliments on_update method on par with standard .update"""
        # update emitter
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        # update particles
        emit_count = self.rate_factory.how_many(1 / 60, len(self._particles))
        for _ in range(emit_count):
            self._emit()

        self._particles.on_update(delta_time)

        for alien in filter(lambda p: p.can_reap(), self._particles):
            if not (alien.top <= 0):
                self.starship.xp += alien.config.info.xp
            alien.kill()

    def draw(self, pixelated=False):
        self._particles.draw(pixelated=pixelated, filter=arc.gl.NEAREST)
