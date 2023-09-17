from dataclasses import dataclass

from pydantic import validator

# from alien_invasion.utils.loaders.alien import load_alien_by_name
from alien_invasion.utils.loaders.alien import AlienConfig

from alien_invasion.utils.loaders.level.model import OnslaughtWave


@dataclass(kw_only=True)
class AlienWaveWrapper:
    config: AlienConfig
    # spawner: AlienSpawnerStats


class OnslaughtWave:
    """A single onslaught wave of a `Level`"""

    def __init__(self, config: OnslaughtWave) -> None:
        self.spawns: list[AlienWaveWrapper]
        self.timer: float

    @validator("spawns", pre=True)
    def get_alien_configs(cls, configs_dict: dict) -> list[AlienWaveWrapper]:
        """
        Example
        -------
        >>> configs_dict
        {
            'dummy_ufo': {
                'approach_velocity_multiplier': 1.6,
                'spawn_interval': 1.6,
                'spawn_random_rotation': False
            },
            'castle_wall_sontra': {
                'approach_velocity_multiplier': 1.36,
                'spawn_interval': 3.0,
                'spawn_random_rotation': True
            }
        }
        """
        configs = []
        # for pair in configs_dict.items():
        #     alien_config = load_alien_by_name(pair[0])
        #     # alien_spawner_stats = AlienSpawnerStats.parse_obj(pair[1])
        #     # configs.append(
        #     #     AlienWaveWrapper(config=alien_config, spawner=alien_spawner_stats)
        #     # )
        return configs

    class Config:
        arbitrary_types_allowed = True
