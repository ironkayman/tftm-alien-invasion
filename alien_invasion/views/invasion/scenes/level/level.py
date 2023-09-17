"""Loadable entites of level structure.
"""

from itertools import chain
from pathlib import Path

import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.utils.loaders.level.model import LevelConfiguration
from alien_invasion.entities import Alien, Starship
from alien_invasion.entities.alien.mixins.on_update.evade_bullets import (
    on_update_evade_bullets,
)
from alien_invasion.entities.alien.mixins.on_update.fire_bullets import (
    on_update_fire_bullets,
)
from alien_invasion.entities.alien.mixins.on_update.moveset_stategy import (
    on_update_plot_movement,
)
from alien_invasion.entities.common.state_manager.state import AlienMoveset

from .spawner import AlienSpawner
from .wave import Wave


class Level(arc.Scene):
    """Description of a single level consisting of `Wave`s.

    Attributes
    -----------
    waves : tuple[Wave]
        Tuple of level waves.
    """

    waves: list[Wave]
    _current_wave_index: int = 0
    _wave_timer: float = 0.0
    is_finished: bool = False
    title_image_path: Path

    def __init__(self, config: LevelConfiguration) -> None:
        """

        Parameters
        ----------
        config : LevelConfiguration
        """
        super().__init__()
        self._config = config
        self.display_name = config.display_name
        self.description = config.description
        self.waves = [
            Wave(**wave_config) for wave_config in self._config.onslaught_waves
        ]
        self.alien_was_hit_effect_particles = arc.SpriteList()
        self.title_image_path = config.title_image

    def alien_constructor(self, alien_config) -> AlienSpawner:
        particle_factory = lambda emitter: Alien(
            config=alien_config.config,
            overrides=dict(
                should_persue=alien_config.spawner.should_persue,
            ),
            approach_velocity_multiplier=alien_config.spawner.approach_velocity_multiplier,
            # relative to emitter's center_xy
            center_xy=arc.rand_on_line(
                (-CONSTANTS.DISPLAY.WIDTH // 2, 0), (CONSTANTS.DISPLAY.WIDTH // 2, 0)
            ),
            hit_effect_list=self.alien_was_hit_effect_particles,
            # starship=self.starship,
            alien_bullets=self.alien_bullets,
            change_xy=arc.rand_vec_spread_deg(
                -90, 12, 1 * CONSTANTS.DISPLAY.SCALE_RELATION
            ),
            parent_sprite_list=emitter._particles,
            scale=alien_config.spawner.scale,
            angle=arc.rand_angle_360_deg()
            if alien_config.spawner.spawn_random_rotation
            else 0,
        )  # type: ignore E731
        return AlienSpawner(
            starship=self.starship,
            center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT - 20),
            emit_controller=arc.EmitInterval(alien_config.spawner.spawn_interval),
            particle_factory=particle_factory,
        )

    def setup(self, starship: Starship) -> None:
        """Starts the level.

        Iterates through waves, spawning it's aliens and manages time.
        """

        self.starship = starship
        self.__current_wave: Wave = self.waves[self._current_wave_index]
        self.alien_bullets = starship.enemy_shots

        # Alens are spawned as particle-like objects
        # from an eternal Emitter wth time interval between spawns
        self.initialise_wave()

    def initialise_wave(self) -> None:
        """Initialises a `Wave` object to spawn aliens from"""
        # sort by size, this will affect draw order, so
        # less sized aliens may be placed under larger once
        wave = self.__current_wave
        wave.spawns.sort(key=lambda c: c.config.info.size.value, reverse=True)
        self.spawners = []
        spawn_pairs = zip([self.alien_constructor] * len(wave.spawns), wave.spawns)
        # workound to prevent pointer of config-spawners
        # to update through external variable passed to func
        # under for/while cycle across multiple iterations
        # of AlienSpawner object creation (one per alien)
        for spawn_pair in spawn_pairs:
            self.spawners.append(spawn_pair[0](spawn_pair[1]))

    @property
    def aliens(self) -> arc.SpriteList:
        """All aliens

        Returns
        -------
        arc.SpriteList
            All aliens currently present,
            disregarding their original spawner.
        """
        aliens_all = arc.SpriteList()
        for aliens in self.spawners:
            aliens_all.extend(aliens._particles)
        return aliens_all

    @property
    def starship_danger(self) -> arc.SpriteList:
        """All objects capable of damaging starship

        Returns
        -------
        arc.SpriteList
            All aliens (`self.aliens` property) and their
            currently present bullets.
        """
        starship_danger_list = self.aliens
        starship_danger_list.extend(self.alien_bullets)
        return starship_danger_list

    def check_wave_completion_requirements(self) -> None:
        """Checks if required XP gained to proceed to a next Wave"""
        if all(
            (
                self.__current_wave.pass_score <= self.starship.xp,
                self._wave_timer > self.__current_wave.pass_time,
            )
        ):
            self._wave_timer = 0.0
            if self._current_wave_index == len(self.waves) - 1:
                self.is_finished = True
                return
            self._current_wave_index += 1
            print("Reached Wave:", self._current_wave_index + 1)
            self.__current_wave: Wave = self.waves[self._current_wave_index]
            self.initialise_wave()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""

        def process_collisions_aliens_damage_bullets() -> None:
            """Check if starship's bullets hit aliens"""
            collisions = []
            for aliens in self.spawners:
                # detects cullet collisions
                # TODO: pass collided bulle
                #    object for bullet-specific (or ships primary weapon)
                # changes in being-hit animation
                for bullet in self.starship.fired_shots:
                    collisions_local = arc.check_for_collision_with_list(
                        bullet, aliens._particles
                    )
                    if not collisions_local:
                        continue
                    collisions.append([collisions_local[-1], bullet.damage])
                    bullet.kill()

            for alien_bullet_pair in collisions:
                alien_bullet_pair[0].hp -= alien_bullet_pair[1]

        def process_collisions_bullets_clearout() -> None:
            """Check if starship's bullets collide with aliensm"""
            # ship's bullets can clear out aliens' bullets
            for bullet in self.starship.fired_shots:
                collisions = arc.check_for_collision_with_list(
                    bullet, self.alien_bullets
                )
                for c in collisions:
                    c.remove_from_sprite_lists()

        def process_out_of_bounds_alien_bullets() -> None:
            """If alien bullets reach bottom of the viewport remove them"""
            # remove all out of window player bullets
            for bullet in self.alien_bullets:
                if bullet.top < 0:
                    bullet.remove_from_sprite_lists()

        def process_bounds_starship_bullets() -> None:
            """Remove starship's bullets which reched top of the viewport"""
            # remove all out of window player bullets
            for bullet in filter(
                lambda bullet: bullet.bottom > CONSTANTS.DISPLAY.HEIGHT,
                self.starship.fired_shots,
            ):
                bullet.remove_from_sprite_lists()

        def process_collisions_starship_damage_bullets() -> None:
            """Damage starship if alien bullets hit it"""
            for bullet in arc.check_for_collision_with_list(
                self.starship, self.alien_bullets
            ):
                self.starship.hp -= bullet.damage
                bullet.remove_from_sprite_lists()

        def process_collisions_aliens_starship_sprites() -> None:
            """Damage starship if it collides with aliens"""
            collisions = []
            for aliens in self.spawners:
                # process collisions between starship and aliens
                if collisions_local := arc.check_for_collision_with_list(
                    self.starship, aliens._particles
                ):
                    collisions.extend(collisions_local)
            for collisioned_alien in collisions:
                # drain both starship's and collided alien's HP
                self.starship.hp -= round(self.starship.max_hp * 0.01)
                collisioned_alien.hp -= round(collisioned_alien.hp * 0.01)

        def process_starship_danger_proximity() -> None:
            """Check for enemies' proximity to starship, set it's flag"""
            self.starship.is_proximity = False
            tracked_objects = self.starship_danger
            if (
                closest := arc.get_closest_sprite(self.starship, tracked_objects)
            ) and closest[1] < 45 * CONSTANTS.DISPLAY.SCALE_RELATION:
                self.starship.is_proximity = True

        def process_wave_amplification() -> None:
            """Amplifies alien spawning density

            Each wave has an `interval` (timer) in which its will once
            increase wpawn density by deviding spawners' `EmitInterval`
            or `.taye_factory` value by the wave's `density_multiplier`.
            """
            self.__current_wave._timer += delta_time
            if self.__current_wave._timer >= self.__current_wave.interval:
                # reset timer
                self.__current_wave._timer = 0
                for spawner in self.spawners:
                    spawner.rate_factory = arc.EmitInterval(
                        round(
                            spawner.rate_factory._emit_interval
                            / self.__current_wave.density_multiplier,
                            2,
                        )
                    )
                    print(
                        "amplification:",
                        spawner.rate_factory._emit_interval,
                        "->",
                        round(
                            spawner.rate_factory._emit_interval
                            / self.__current_wave.density_multiplier,
                            2,
                        ),
                    )

        self._wave_timer += delta_time
        process_wave_amplification()

        for alien in chain.from_iterable([sp._particles for sp in self.spawners]):
            # plot movement
            on_update_plot_movement(alien, self.starship, delta_time)
            # evade bullets
            if AlienMoveset.dodging in alien.state.movesets:
                on_update_evade_bullets(alien, self.starship, delta_time)
            # firing logic
            if AlienMoveset.firing in alien.state.movesets:
                on_update_fire_bullets(alien, self.starship, delta_time)
            # alien.on_update(delta_time)
        # update alien emitter/spawner
        for spawn in self.spawners:
            spawn.on_update(delta_time)
        self.alien_bullets.update()

        process_collisions_bullets_clearout()
        process_out_of_bounds_alien_bullets()
        process_starship_danger_proximity()

        if self.starship.can_reap():
            return
        process_bounds_starship_bullets()
        process_collisions_starship_damage_bullets()
        process_collisions_aliens_damage_bullets()
        process_collisions_aliens_starship_sprites()

        self.alien_was_hit_effect_particles.update()

        self.check_wave_completion_requirements()

    def draw(self):
        """
        Render background section.
        """
        for spawn in self.spawners:
            spawn.draw()

        if self.starship.is_proximity:
            arc.draw_polygon_outline(
                self.starship.current_position_original_hit_box,
                arc.color.ALIZARIN_CRIMSON,
                3 * CONSTANTS.DISPLAY.SCALE_RELATION,
            )

        # Externally (outside of particles and emitter) draw hit effect sprites
        self.alien_was_hit_effect_particles.draw()
        self.alien_bullets.draw()
        super().draw(pixelated=True)
