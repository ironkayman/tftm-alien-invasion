"""Loadable entites of level structure.
"""

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

        Examples
        --------
        >>> config
        {
            'name': '1',
            'waves': [
                {
                    'spawns': ['dummy_ufo', 'castle_wall_sontra'],
                    'total_enemy_health': 400,
                    'pass_score': 30,
                    'interval': 30,
                    'density_multiplier': 1.7
                }
            ]
        }
        """
        super().__init__()
        self.waves=[
            Wave(**wave_config)
            for wave_config
            in config['waves']
        ]
        self.alien_was_hit_effect_particles = arc.SpriteList()

    def setup(self, starship: Starship) -> None:
        """Starts the level.

        Iterates through waves, spawning it's aliens and manages time.
        """

        self.starship = starship
        self.__current_wave: Wave = self.waves[self._current_wave]
        self.alien_bullets = starship.enemy_shots

        # for alien_config in self.__current_wave.spawns:
        #     AlienSpawner(alien_config)

        # Alens are spawned as particle-like objects
        # from an eternal Emitter wth time interval between spawns
        self.spawners = [
            AlienSpawner(
                starship=self.starship,
                center_xy=(
                    CONSTANTS.DISPLAY.WIDTH // 2,
                    CONSTANTS.DISPLAY.HEIGHT - 20
                ),
                emit_controller=arc.EmitInterval(1.6),
                particle_factory=lambda emitter: Alien(
                    config=self.__current_wave.spawns[0],
                    # relative to emitter's center_xy
                    center_xy=arc.rand_on_line(
                        (- CONSTANTS.DISPLAY.WIDTH // 2, 0),
                        (CONSTANTS.DISPLAY.WIDTH // 2, 0)
                    ),
                    hit_effect_list=self.alien_was_hit_effect_particles,
                    starship=self.starship,
                    alien_bullets=self.alien_bullets,
                    change_xy=arc.rand_vec_spread_deg(-90, 12, 1.0),
                    parent_sprite_list=emitter._particles,
                )  # type: ignore
            ),
            AlienSpawner(
                starship=self.starship,
                center_xy=(
                    CONSTANTS.DISPLAY.WIDTH // 2,
                    CONSTANTS.DISPLAY.HEIGHT - 20
                ),
                emit_controller=arc.EmitInterval(3.0),
                particle_factory=lambda emitter: Alien(
                    config=self.__current_wave.spawns[1],
                    # relative to emitter's center_xy
                    center_xy=arc.rand_on_line(
                        (- CONSTANTS.DISPLAY.WIDTH // 2, 0),
                        (CONSTANTS.DISPLAY.WIDTH // 2, 0)
                    ),
                    hit_effect_list=self.alien_was_hit_effect_particles,
                    starship=self.starship,
                    alien_bullets=self.alien_bullets,
                    change_xy=arc.rand_vec_spread_deg(-90, 12, 0.6),
                    parent_sprite_list=emitter._particles,
                    scale=2.0,
                    angle=arc.rand_angle_360_deg(),
                )  # type: ignore
            ),
        ]
        # dont add sprite list to scene since spawner counts it
        # but cant track it so we create only a pointer namespace
        # self.aliens = self.spawners[0]._particles, self.spawners[1]._particles

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
        self.spawners[0].on_update(delta_time)
        self.spawners[1].on_update(delta_time)
        self.alien_bullets.update()

        process_collisions_bullets_clearout()
        process_out_of_bounds_alien_bullets()

        if self.starship.can_reap(): return
        process_collisions_alien_bullets()
        process_collisions_starship_damage_bullets()
        process_collisions_aliens_damage_bullets()
        process_collisions_aliens_starship_sprites()


    def draw(self):
        """
        Render background section.
        """
        self.spawners[0].draw()
        self.spawners[1].draw()
        # Externally (outside of particles and emitter) draw hit effect sprites
        self.alien_was_hit_effect_particles.draw()
        self.alien_bullets.draw()
        super().draw(pixelated=True)
