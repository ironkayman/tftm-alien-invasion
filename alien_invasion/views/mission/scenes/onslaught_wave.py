from dataclasses import dataclass
from typing import List, Optional

from pydantic import validator

import arcade as arc

from alien_invasion.utils.loaders.alien import load_alien_by_name
from alien_invasion.utils.loaders.alien import AlienConfig

from alien_invasion.utils.loaders.level.model import (
    ModelOnslaughtWave,
    AlienSpawnConfiguration,
)

from alien_invasion.entities import AlienSpawner

class OnslaughtWave(arc.Scene):
    """A single onslaught wave of a `Level`"""

    def __init__(
        self,
        config: ModelOnslaughtWave,
        state_registry: dict[str, arc.Texture],
    ) -> None:
        """

        Parameters
        ----------
        config : ModelOnslaughtWave
        state_registry : dict[str, arc.Texture]
            "<alien name>.<state name>": bytes
        """
        self.__config = config
        self.state_registry = state_registry

        self.timer = 0.0
        self.__alien_configurations: list[AlienConfig] = []

        # configs = []
        # for pair in configs_dict.items():
        #     alien_config = load_alien_by_name(pair[0])
        #     alien_spawner_stats = AlienSpawnerStats.parse_obj(pair[1])
        #     configs.append(
        #         AlienWaveWrapper(config=alien_config, spawner=alien_spawner_stats)
        #     )
        # return configs

    def setup(self):
        """
        Put registry, remove path key
        """
        self.__create_spawnables()

    def __create_spawnables(self):
        for alien_spawn_config in self.__config.spawns:
            alien_name = alien_spawn_config.name
            self.__alien_configurations.append(
                (alien_config := load_alien_by_name(alien_name))
            )
            for state_props in alien_config.states:
                state_name = state_props['name']
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

            AlienSpawner(
                config=alien_spawn_config
                # starship=self.starship,
                # center_xy=(CONSTANTS.DISPLAY.WIDTH // 2, CONSTANTS.DISPLAY.HEIGHT - 20),
                # emit_controller=arc.EmitInterval(alien_config.spawner.spawn_interval),
                # particle_factory=particle_factory,
            )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.timer += delta_time
        print(self.timer)
        return super().on_update()

    def draw(self) -> None:
        return super().draw()