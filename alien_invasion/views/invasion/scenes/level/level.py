"""Loadable entites of level structure.
"""

import arcade as arc

from .wave import Wave


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

    def setup(self, starship) -> None:
        """Starts the level.

        Iterates through waves, spawning it's aliens and manages time.
        """

        self.starship = starship
        wave = self.waves[self._current_wave]

        # Alens are spawned as particle-like objects
        # from an eternal Emitter wth time interval between spawns
        # self.spawner = arc.Emitter(
        #     center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT - 20),
        #     emit_controller=arc.EmitInterval(0.6),
        #     particle_factory=lambda emitter: Alien(
        #         config=config,
        #         hit_effect_list=self.alien_was_hit_effect_particles,
        #         change_xy= arc.rand_vec_spread_deg(-90, 40, 2.0),
        #     )  # type: ignore
        # )
        # # dont add sprite list to scene since spawner counts it
        # # but cant track it so we create only a pointer namespace
        # self.aliens = self.spawner._particles

    def on_update(self, delta_time: float = 1 / 60) -> None:
        return super().on_update(delta_time)

    # def draw(self) -> None:
    #     return super().draw()
