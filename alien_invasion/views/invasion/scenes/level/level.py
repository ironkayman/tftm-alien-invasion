"""Loadable entites of level structure.
"""

from random import randrange

import arcade as arc

from alien_invasion import CONSTANTS

from .wave import Wave

from alien_invasion.entities import Alien

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
        super().__init__()
        self.waves = [Wave(w) for w in config['waves']]
        self.alien_was_hit_effect_particles = arc.SpriteList()

    def setup(self, starship) -> None:
        """Starts the level.

        Iterates through waves, spawning it's aliens and manages time.
        """

        self.starship = starship
        self.__current_wave: Wave = self.waves[self._current_wave]

        # select random config
        self.__current_alien_config = self.__current_wave.spawns[0]

        # Alens are spawned as particle-like objects
        # from an eternal Emitter wth time interval between spawns
        self.spawner = arc.Emitter(
            center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT - 20),
            emit_controller=arc.EmitInterval(0.6),
            particle_factory=lambda emitter: Alien(
                config=self.__current_alien_config,
                hit_effect_list=self.alien_was_hit_effect_particles,
                change_xy= arc.rand_vec_spread_deg(-90, 40, 2.0),
            )  # type: ignore
        )
        # dont add sprite list to scene since spawner counts it
        # but cant track it so we create only a pointer namespace
        self.aliens = self.spawner._particles

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""

        # select random config
        self.__current_alien_config = self.__current_wave.spawns[randrange(len(self.__current_wave.spawns))]

        # update alien emitter/spawner
        self.spawner.update()

        collisions = []
        # detects cullet collisions
        # TODO: pass collided bullet object for bullet-specific (or ships primary weapon)
        # changes in being-hit animation
        for bullet in self.starship.fired_shots:
            collisions = arc.check_for_collision_with_list(
                bullet, self.spawner._particles
            )
            if not collisions: continue
            bullet_damage: int = self.starship.loadout.weaponry.primary.bullet_damage
            bullet.kill()

            for alien in collisions:
                alien.hp -= bullet_damage

    def draw(self):
        """
        Render background section.
        """
        self.spawner.draw()
        # Externally (outside of particles and emitter) draw hit effect sprites
        self.alien_was_hit_effect_particles.draw()
        super().draw(pixelated=True)
