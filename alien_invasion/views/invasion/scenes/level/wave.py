from pydantic import BaseModel, validator, ValidationError

from alien_invasion.utils.loaders.alien import load_alien_by_name
from alien_invasion.utils.loaders.alien import AlienConfig


class Wave(BaseModel):
    """Single wave of a `Level`.

    Attributes
    ----------
    spawns : list[AlienConfig]
        Aliens Configs whom are present in this wave.
    pass_score : int
        Score/experince from aliens required to pass a wave.
    interval : int
        Interval in seconds before `density_multplier` increase.
    density_multiplier : float
        How many enemies and their speed
        will increase at next interval.
    """

    spawns: list[AlienConfig]
    pass_score: int
    interval: int
    density_multiplier: float
    total_enemy_health: int

    @validator('spawns', pre=True)
    def get_alien_configs(cls, configs_dict: dict) -> list[AlienConfig]:
        """
        Example
        -------
        >>> configs_dict
        {
            'dummy_ufo': {
                'approach_velocity': 60.0,
                'spawn_interval': 1.6,
                'spawn_random_rotation': False
            },
            'castle_wall_sontra': {
                'approach_velocity': 36.0,
                'spawn_interval': 3.0,
                'spawn_random_rotation': True
            }
        }
        """
        alien_configs = []
        for pair in configs_dict.items():
            alien_config = load_alien_by_name(pair[0])
            alien_config.spawner = pair[1]
            alien_configs.append(alien_config)
        return alien_configs

    class Config:
        arbitrary_types_allowed = True
