"""Onslaugh Wave scene represents object of a single wave in a mission
"""

import arcade as arc

from alien_invasion.utils.loaders.alien import load_alien_by_name
from alien_invasion.utils.loaders.alien import AlienConfig

from alien_invasion.utils.loaders.level.model import (
    ModelOnslaughtWave,
    ModelPassRequirements,
)

from alien_invasion.entities import AlienSpawner


class OnslaughtWave(arc.Scene):
    """A single onslaught wave initiated from wave config

    Rest of parameters are once that are shared across
    the entire mission.

    Yet, despite alien_bullets are shared across all aliens,
    aliens themselves are placed to individual spwners' spritelists
    which we iterate through in Mission's view on_update.

    Attributes
    ----------
    state_registry : dict[str, arc.Texture]
        Mapping of loaded textures by a string id,
        composed of alien's name and state's name.
    alien_bullets : arc.SpriteList
        Shared spritelist of all bullets.
    spawners : list[AlienSpawner]
        List aliens' spawners, each contains spritelist
        of aliens (`._particles`, `.alien_group`).
    completion_requirements : ModelPassRequirements
        completion_requirements are loaded from wave's
        config that are required for moving/initiating
        a the next OnsluaghtWave.
    """

    def __init__(
        self,
        config: ModelOnslaughtWave,
        state_registry: dict[str, arc.Texture],
        alien_bullets: arc.SpriteList,
        # hit_effects: arc.SpriteList,
    ) -> None:
        """

        Parameters
        ----------
        config : ModelOnslaughtWave
        state_registry : dict[str, arc.Texture]
            Mapping of loaded textures to their alien-state pairs:
            "<alien name>.<state name>": arc.texture
        alien_bullets : arc.SpriteList
            Shared spritelist of all aliens' bullets
        """
        self.__config = config
        self.state_registry = state_registry
        self.alien_bullets = alien_bullets
        # self.hit_effects = hit_effects
        self.completion_requirements: ModelPassRequirements = (
            self.__config.pass_requirements
        )

        self.timer = 0.0
        self.__alien_configurations: list[AlienConfig] = []
        self.spawners: list[AlienSpawner] = []

    def setup(self):
        """Initiates scene, creates alien spawners"""
        self.__create_spawnables()

    def __create_spawnables(self):
        """Creates this wave's spawners

        Iterates through spawner configurations of wave config.
        From every spawner configuration load an alien by name,
        then load alien's textures delegated to
        it's states and store them in texture registry,
        which is passed to every spawner and spawned alien
        once it is filled.
        """
        for alien_spawn_config in self.__config.spawns:
            alien_name = alien_spawn_config.name
            self.__alien_configurations.append(
                (alien_config := load_alien_by_name(alien_name))
            )
            for state_props in alien_config.states:
                state_name = state_props["name"]
                texture_id = f"{alien_name}.{state_name}"

                # texture_id already exists
                if self.state_registry.get(texture_id):
                    continue

                self.state_registry[texture_id] = arc.load_texture(
                    file_name=state_props["texture_path"],
                    flipped_vertically=True,
                    can_cache=True,
                    hit_box_algorithm="Detailed",
                )
                # link state's texture by an ID akin many-to-one
                state_props["registry_texture_id"] = texture_id
                del state_props["texture_path"]

            self.spawners.append(
                AlienSpawner(
                    spawn_config=alien_spawn_config,
                    alien_config=alien_config,
                    alien_bullets=self.alien_bullets,
                    # hit_effects=self.hit_effects,
                    texture_registry=self.state_registry,
                )
            )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Updates each aliens' spawner"""
        self.timer += delta_time
        for s in self.spawners:
            s.on_update(delta_time)

    def draw(self) -> None:
        for s in self.spawners:
            s.draw()
