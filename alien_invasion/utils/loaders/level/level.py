"""Loadable entites of level structure.
"""

from pydantic import BaseModel, Field, validator

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

    def __init__(self, config: dict) -> None:
        super().__init__(**config)

    @validator('spawns', pre=True)
    def get_alien_configs(cls, val) -> list[AlienConfig]:
        return [load_alien_by_name(alien_name) for alien_name in val]

    class Config:
        arbitrary_types_allowed = True

class Level(BaseModel):
    """Description of a single level consisting of `Wave`s.

    Attributes
    -----------
    waves : tuple[Wave]
        Tuple of level waves.
    """

    waves: tuple[Wave] = Field(default_factory=object, exclude=True)

    def __init__(self, config: dict) -> None:
        super().__init__(
            waves=tuple(map(
                lambda w: Wave(w), config['waves']
            )),
        )