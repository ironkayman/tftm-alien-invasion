"""Logic for Alien spawners
"""
import arcade as arc

# from alien_invasion.entities import Alien
from alien_invasion.utils.loaders.level.model import AlienSpawnConfiguration
from alien_invasion.utils.loaders.alien.config import AlienConfig
from alien_invasion.entities import Alien

from alien_invasion import CONSTANTS


class AlienSpawner(arc.Emitter):
    """Implementation of Emitter specifically for Alien class particle.

    Attributes
    ----------
    aliens : arc.SpriteList
        Public alias for `._particles` of the Emitter.
    last_reap_results_total_xp : int
        XP gained from the last on_update reap()
        Used in Mission view on_update to sum
        gained XP to the starship.
    last_reap_results_count : int
        Number of reaped entites shose XP we count
    """

    def __init__(
        self,
        spawn_config: AlienSpawnConfiguration,
        alien_config: AlienConfig,
        alien_bullets: arc.SpriteList,
        # hit_effects: arc.SpriteList,
        texture_registry: dict[str, arc.Texture],
    ) -> None:
        """Create Spawner from it's configuration `spawn_config`

        Parameters
        ----------
        spawn_config : AlienSpawnConfiguration
            Configuration of a spawner of a single
            type of alien
        alien_config : AlienConfig
            Confguration of spawnable alien:
            name and other info
        alien_bullets : arc.SpriteList
            Shared across all spawners list of alien bullet.
        texture_registry : dict[str, arc.Texture]
            Finalised aliens' state texture registry to pass
            to individual alien spawned.
        """
        self._spawn_config = spawn_config
        self._alien_config = alien_config
        self._alien_bullets = alien_bullets
        # self._hit_effects = hit_effects
        self._texture_registry = texture_registry

        self.__timer = 0.0

        self.last_reap_results_total_xp = 0
        self.last_reap_results_count = 0

        self._base_rate = self._spawn_config.spawn_rates.rate
        emit_controller = arc.EmitInterval(1 / self._base_rate)
        self._max_count = self._spawn_config.spawn_rates.max_count  # 999 defaut

        # seconds
        self._rate_increase_interval = (
            self._spawn_config.spawn_rates.rate_increase_interval
        )
        self._density_multiplier = self._spawn_config.spawn_rates.density_multiplier
        self._movement_velocity_multiplier = (
            self._spawn_config.movement_velocity_multiplier
        )

        super().__init__(
            center_xy=(0, CONSTANTS.DISPLAY.HEIGHT + 40),
            emit_controller=emit_controller,
            particle_factory=self.__alien_factory,
        )
        # alias
        self.aliens = self._particles

    def __iter__(self) -> list[Alien]:
        return iter(self.aliens)

    def __alien_factory(self, emitter: arc.Emitter) -> Alien:
        return Alien(
            config=self._alien_config,
            system_name=self._spawn_config.name,
            texture_registry=self._texture_registry,
            # approach_velocity_multiplier=
            # alien_config.spawner.approach_velocity_multiplier,
            # relative to emitter's center_xy
            center_xy=arc.rand_on_line(
                (0, 0),
                (CONSTANTS.DISPLAY.WIDTH, 0),
            ),
            # hit_effects=self._hit_effects,
            # starship=self.starship,
            fired_shots=self._alien_bullets,
            change_xy=arc.rand_vec_spread_deg(
                -90, 12, 1 * CONSTANTS.DISPLAY.SCALE_RELATION
            ),
            # parent_sprite_list=emitter._particles,
            scale=self._spawn_config.scale,
            angle=(
                arc.rand_angle_360_deg() if self._spawn_config.random_rotation else 0
            ),
            movement_velocity_multiplier=self._movement_velocity_multiplier,
        )

    def _calculate_interval(
        self,
        current: float,
        base_rate: float,
        multiplier: float,
    ) -> float:
        """An internal function for increasing spawn rate over time

        Works best when base_rate is minimal
        and increased incrimentally,
        and once computed value becomes too low - negative,
        compute 9/10 of current interval (not rate).

        Parameters
        ----------
        current : float
            Current interval in float seconds
        base_rate : float
            Base rate set in spawner's configuration
            To calculate it's interval in float seconds:
                `1 / base_rate`
        multiplier : float
            Multiplier of `base_rate` as set in spawner's configuration

        Returns
        -------
        float
            New, lowerer than the previous interval,
            so spawn rate is higher.
        """
        if (result := current - (base_rate * multiplier)) <= 0:
            return current * 9 / 10
        return result

    def on_update(self, delta_time: float) -> None:
        """Impliments on_update method on par with standard .update"""
        self.__timer += delta_time

        # update emitter
        self.last_reap_results_total_xp = 0
        self.last_reap_results_count = 0
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        # if max_count is exeeded, do not spawn new instances of alien
        if len(self._particles) < self._max_count:
            emit_count = self.rate_factory.how_many(delta_time, len(self._particles))
            for _ in range(emit_count):
                self._emit()

            # and if we have rate increase set, increase the rate
            # with _calculate_interval
            if (
                self._rate_increase_interval
                and self.__timer > self._rate_increase_interval
            ):
                print(
                    "o", self._alien_config.info.name, self.rate_factory._emit_interval
                )
                self.__timer = 0.0
                self.rate_factory = arc.EmitInterval(
                    self._calculate_interval(
                        self.rate_factory._emit_interval,
                        self._base_rate,
                        self._density_multiplier,
                    )
                )
                print(
                    "n", self._alien_config.info.name, self.rate_factory._emit_interval
                )

        self._particles.on_update(delta_time)

        for alien in filter(lambda p: p.can_reap(), self._particles):
            # do not count xp of once below of the viewport
            if not (alien.top <= 0):
                self.last_reap_results_count += 1
                self.last_reap_results_total_xp += alien.config.info.xp
            alien.kill()

    def draw(self, pixelated=False):
        self._particles.draw(pixelated=pixelated)
        for p in self._particles:
            p.draw_hit_effects()
