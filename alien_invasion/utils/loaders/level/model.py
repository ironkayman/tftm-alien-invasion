from typing import Callable
from pathlib import Path

from pydantic import BaseModel, root_validator, ValidationError

from ..config.file_opener import reader


class EmptyWavecompletionRequirements(ValidationError):
    pass


class LevelHasNoOnslaughtWaves(ValidationError):
    pass


class ModelPassRequirements(BaseModel):
    """Requirement for wave completion"""

    score: int = 0
    duration: float = 0.0
    custom: Callable | None

    @root_validator
    def requirements_checker(cls, values: dict):
        """At least 1 value should be filled"""
        if not any(values.values()):
            raise EmptyWavecompletionRequirements()
        return values


class AliewnSpawnRates(BaseModel):
    """
    Attributes
    ----------
    max_count : int | None
        Upper boundry, if needed
    rate : float
        Spawns per second
    rate_increase_interval : int
        `rate` increased with this interval in seconds
    density_multiplier : float
        Base rate increase
    """

    max_count: int = 999
    rate: float
    rate_increase_interval: int | None = None
    density_multiplier: float = 1.00


class AlienSpawnConfiguration(BaseModel):
    """Arbitrary Aliens' Spawner properties

    Attributes
    ----------
    name : str
    movement_velocity_multiplier : list[float]
    spawn_rates : AliewnSpawnRates
    scale : float = 1.0
    random_rotation : bool = False
    xp_multiplier : float = 1.0

    AlienSpawnRates
        max_count : int | None
            Upper boundry, if needed
        rate : int
            Spawns per second
    """

    name: str
    movement_velocity_multiplier: list[float] = [1.0, 1.0]  # l-r u-d
    spawn_rates: AliewnSpawnRates
    _registry_config_reference: None
    scale: float = 1.0
    random_rotation: bool = False
    xp_multiplier: float = 1.0

    @root_validator(pre=True)
    def preproc(cls, v: dict):
        v["spawn_rates"] = AliewnSpawnRates(**v["spawn_rates"])
        return v

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True
        arbitrary_types_allowed = True


class ModelOnslaughtWaveSoundtrack(BaseModel):
    start: str
    stop: str
    loop: bool
    _path: Path

    class Config:
        underscore_attrs_are_private = True


class ModelOnslaughtWave(BaseModel):
    """Describes configuration of an enemy Wave"""

    pass_requirements: ModelPassRequirements
    soundtrack: ModelOnslaughtWaveSoundtrack
    spawns: list[AlienSpawnConfiguration]

    @root_validator(pre=True)
    def preproc(cls, v: dict):
        v["pass_requirements"] = ModelPassRequirements(**v["pass_requirements"])
        v["soundtrack"] = ModelOnslaughtWaveSoundtrack(**v["soundtrack"])
        # v["soundtrack"]._path =
        spawns_replaced = []
        for spawn_dict in v["spawns"]:
            spawns_replaced.append(AlienSpawnConfiguration(**spawn_dict))
        v["spawns"] = spawns_replaced
        return v

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True
        arbitrary_types_allowed = True


class LevelConfiguration:
    """Dict-like descriptin of a level from designated .toml

    Attributes
    ----------
    error : Exception | Ellipsis
    display_name : str
    description : str
    title_image : Path
    onslaught_waves : list[OnslaughtWave]

    OnslaughtWave
        pass_requirements : PassRequirements
        soundtrack : OnslaughtWaveSoundtrack
        spawns : list[AlienSpawnConfiguration]

        PassRequirements
            score : int | None
            duration : int | None
            custom : Callable | None

        OnslaughtWaveSoundtrack
            start : str
            stop : str
            loop : bool

        AlienSpawnConfiguration
            name : str
            movement_velocity_multiplier : list[float]
            spawn_rates : AliewnSpawnRates
            scale : float = 1.0
            random_rotation : bool = False
            xp_multiplier : float = 1.0

            AliewnSpawnRates
                max_count : int | None
                rate : int
    """

    def __init__(self, level_dir: Path) -> None:
        self.__source_path = level_dir
        level_dict, error = reader(level_dir / "level.toml")
        if error:
            self.error = error

        try:
            self.display_name: str = level_dict["display_name"]
            self.description: str = level_dict["description"]

            self.title_image: Path = self.__source_path / "title.png"

            self.onslaught_waves: list[ModelOnslaughtWave] = []
            if len((waves := level_dict["waves"])) == 0:
                raise LevelHasNoOnslaughtWaves()
            for wave in waves:
                self.onslaught_waves.append(ModelOnslaughtWave(**wave))
        except Exception as e:
            self.error = e
