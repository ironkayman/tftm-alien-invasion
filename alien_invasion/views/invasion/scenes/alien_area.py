"""Scane and a manager for aliens' movement and interaction logic.
"""

import arcade as arc

from alien_invasion.utils.loaders.level import loader as load_levels
from alien_invasion.entities import Alien

from alien_invasion.entities.starship import Starship

from alien_invasion import CONSTANTS


class AlienArea(arc.Scene):
    """Aliens' Scene

    Contains logic for starship-bulets-aliens' interactions.
    """

    def __init__(self, starship: Starship) -> None:
        super().__init__()

        self.starship = starship

        # spritelist for all partcles which should be emitter when
        # any aliens s ht by a bullet, is given to all Alien instances
        # and is modified there internally
        #
        # ARCHITECTURAL NOTE: External definition solves the problem of impossibilty
        # to draw this spritelist inside alien-instances (particle intances)
        # since they do not have regulary called .draw method and
        # rely on being drawn solely by emitter's internal spritelist (.particles)
        # internal optimzational logic,
        # so, as a workaround, we draw this spritelist outside of particles
        # or their emitter.
        self.alien_was_hit_effect_particles = arc.SpriteList()
        # unused
        self.aliens_bullet_list: arc.SpriteList = arc.SpriteList()

        self.LEVELS = load_levels()

        config = list(self.LEVELS)[0].waves[0].spawns[0]

        level = next(self.LEVELS)

        # level.launch(self.starship)

        # Alens are spawned as particle-like objects
        # from an eternal Emitter wth time interval between spawns
        self.spawner = arc.Emitter(
            center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT - 20),
            emit_controller=arc.EmitInterval(0.6),
            particle_factory=lambda emitter: Alien(
                config=config,
                hit_effect_list=self.alien_was_hit_effect_particles,
                change_xy= arc.rand_vec_spread_deg(-90, 40, 2.0),
            )  # type: ignore
        )
        # dont add sprite list to scene since spawner counts it
        # but cant track it so we create only a pointer namespace
        self.aliens = self.spawner._particles

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""

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
