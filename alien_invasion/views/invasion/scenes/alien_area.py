import arcade as arc

from alien_invasion.utils.loaders.alien import loader
from alien_invasion.entities import Alien

from alien_invasion.entities.starship import Starship

from alien_invasion import CONSTANTS

"""
Alien spawner - chain of moving emitters for particles, but particles are aliens
also they cant overlap and should find pathfinding
"""

class AlienArea(arc.Scene):
    """Aliens' area of movement."""
    def __init__(self, starship: Starship) -> None:
        super().__init__()

        self.starship = starship

        self.aliens_types: arc.SpriteList = arc.SpriteList()
        self.aliens_bullet_list: arc.SpriteList = arc.SpriteList()
        self.alien_was_hit_effect_particles = arc.SpriteList()

        alien_categories = loader()
        config = alien_categories[0]


        self.add_sprite_list(
            name='aliens_types',
            sprite_list=self.aliens_types,
        )


        self.spawner = arc.Emitter(
            center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT - 20),
            emit_controller=arc.EmitInterval(0.6),
            particle_factory=lambda emitter: Alien(
                config=config,
                hit_effect_list=self.alien_was_hit_effect_particles,
                change_xy= arc.rand_vec_spread_deg(-90, 40, 2.0),
            )  # type: ignore
        )
        # self.spawner._particles = arc.SpriteList(use_spatial_hash=False)
        # dont add sprite list to scene since spawner counts it
        # self.add_sprite_list(
        #     name='aliens',
        #     sprite_list=self.spawner._particles,
        # )
        self.aliens = self.spawner._particles

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Compute background layer changes."""

        self.spawner.update()

        collisions = []
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
        self.alien_was_hit_effect_particles.draw()
        super().draw(pixelated=True)