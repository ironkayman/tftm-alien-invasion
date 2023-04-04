"""Loadable entites of level structure.
"""

from itertools import chain

import arcade as arc

from alien_invasion import CONSTANTS

from .wave import Wave
from alien_invasion.entities import Starship
from alien_invasion.entities import Alien

from .spawner import AlienSpawner


class Level(arc.Scene):
    """Description of a single level consisting of `Wave`s.

    Attributes
    -----------
    waves : tuple[Wave]
        Tuple of level waves.
    """

    waves: list[Wave]
    _current_wave: int = 0

    def __init__(self, config: dict) -> None:
        """

        Parameters
        ----------
        config : dict
        """
        super().__init__()
        self.display_name = config['display_name']
        self.description = config['description']
        self.waves=[
            Wave(**wave_config)
            for wave_config
            in config['waves']
        ]
        self.alien_was_hit_effect_particles = arc.SpriteList()

    def alien_constructor(self, alien_config) -> AlienSpawner:
        particle_factory = lambda emitter: Alien(
            config=alien_config.config,
            # relative to emitter's center_xy
            center_xy=arc.rand_on_line(
                (- CONSTANTS.DISPLAY.WIDTH // 2, 0),
                (CONSTANTS.DISPLAY.WIDTH // 2, 0)
            ),
            hit_effect_list=self.alien_was_hit_effect_particles,
            starship=self.starship,
            alien_bullets=self.alien_bullets,
            change_xy=arc.rand_vec_spread_deg(-90, 12, alien_config.spawner.approach_velocity / 60),
            parent_sprite_list=emitter._particles,
            scale=alien_config.spawner.scale,
            angle=arc.rand_angle_360_deg() if alien_config.spawner.spawn_random_rotation else 0
        )
        return AlienSpawner(
            starship=self.starship,
            center_xy=(
                CONSTANTS.DISPLAY.WIDTH // 2,
                CONSTANTS.DISPLAY.HEIGHT - 20
            ),
            emit_controller=arc.EmitInterval(alien_config.spawner.spawn_interval),
            particle_factory=particle_factory,
        )


    def setup(self, starship: Starship) -> None:
        """Starts the level.

        Iterates through waves, spawning it's aliens and manages time.
        """

        self.starship = starship
        self.__current_wave: Wave = self.waves[self._current_wave]
        self.alien_bullets = starship.enemy_shots

        # Alens are spawned as particle-like objects
        # from an eternal Emitter wth time interval between spawns

        # sort by size, this will affect draw order, so
        # less sized aliens may be placed under larger once
        self.__current_wave.spawns.sort(
            key=lambda c: c.config.info.size.value,
            reverse=True
        )
        self.spawners = []
        spawn_pairs = zip(
            [self.alien_constructor] * len(self.__current_wave.spawns),
            self.__current_wave.spawns
        )
        # workound to prevent pointer of config-spawners
        # to update through external variable passed to func
        # under for/while cycle across multiple iterations
        # of AlienSpawner object creation (one per alien)
        for spawn_pair in spawn_pairs:
            self.spawners.append(spawn_pair[0](spawn_pair[1]))

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""

        def process_collisions_aliens_damage_bullets():
            collisions = []
            # detects cullet collisions
            # TODO: pass collided bullet object for bullet-specific (or ships primary weapon)
            # changes in being-hit animation
            for bullet in self.starship.fired_shots:
                collisions = arc.check_for_collision_with_lists(
                    bullet, [self.spawners[0]._particles, self.spawners[1]._particles]
                )
                if not collisions: continue
                bullet_damage: int = self.starship.loadout.weaponry.primary.bullet_damage
                bullet.kill()

                for alien in collisions:
                    alien.hp -= bullet_damage

        def process_collisions_bullets_clearout():
            # ship's bullets can clear out aliens' bullets
            for bullet in self.starship.fired_shots:
                collisions = arc.check_for_collision_with_list(
                    bullet, self.alien_bullets
                )
                for c in collisions:
                    c.remove_from_sprite_lists()

        def process_out_of_bounds_alien_bullets():
            # remove all out of window player bullets
            for bullet in self.alien_bullets:
                if bullet.top < 0:
                    bullet.remove_from_sprite_lists()

        def process_collisions_alien_bullets():
            # remove all out of window player bullets
            for bullet in self.starship.fired_shots:
                if bullet.bottom > CONSTANTS.DISPLAY.HEIGHT:
                    bullet.remove_from_sprite_lists()

        def process_collisions_starship_damage_bullets():
            collisions = arc.check_for_collision_with_list(self.starship, self.alien_bullets)
            for collision in collisions:
                self.starship.hp -= 9
                collision.remove_from_sprite_lists()

        def process_collisions_aliens_starship_sprites():
            # process collisions between starship and aliens
            if (collisions := arc.check_for_collision_with_lists(
                self.starship,
                [
                    self.spawners[0]._particles,
                    self.spawners[1]._particles,
                ]
            )):
                for c in collisions:
                    c.remove_from_sprite_lists()
                    self.starship.hp -= round(self.starship.hp * 0.2)

        # update alien emitter/spawner
        for spawn in self.spawners:
            spawn.on_update(delta_time)
        self.alien_bullets.update()

        process_collisions_bullets_clearout()
        process_out_of_bounds_alien_bullets()

        if self.starship.can_reap(): return
        process_collisions_alien_bullets()
        process_collisions_starship_damage_bullets()
        process_collisions_aliens_damage_bullets()
        process_collisions_aliens_starship_sprites()

        self.alien_was_hit_effect_particles.update()


    def draw(self):
        """
        Render background section.
        """
        for spawn in self.spawners:
            spawn.draw()
        # Externally (outside of particles and emitter) draw hit effect sprites
        self.alien_was_hit_effect_particles.draw()
        self.alien_bullets.draw()
        super().draw(pixelated=True)
