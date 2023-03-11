from pathlib import Path
from enum import IntEnum, auto

from pydantic import BaseModel, validator

from ..config.file_opener import reader

from .entity_dir import AlientResources


class AlienSize(IntEnum):
    """Alien size as Enum"""

    small = auto()
    medium = auto()


class AlienType(IntEnum):
    corporeal = auto()


class AlienInfo(BaseModel):
    name: str
    size: str
    xp: int
    type: set[AlienType]

    def __init__(self, info_config: dict) -> None:
        super().__init__(**info_config)

    @validator('size', pre=True)
    def get_alien_size_enum(cls, val: str) -> AlienSize:
        """Str -> IntEnum"""
        return AlienSize[val]

    @validator('type', pre=True)
    def get_alien_type_enum(cls, val: list) -> set[AlienType]:
        return set(map(lambda c: AlienType[c], val))


class AlienMoveset(IntEnum):
    """str -> IntEnum possible moveset values"""

    spiralling = auto()
    escaping = auto()

class AlienState(BaseModel):
    name: str
    movesets: set[AlienMoveset]
    hp: int
    death_damage_cap: bool
    texture: Path

    @validator('movesets', pre=True)
    def get_movesets(cls, val) -> set[AlienMoveset]:
        return set(map(lambda m: AlienMoveset[m], val))

    def __init__(self,
        core_props_container: tuple[str, dict],
        texture_props_container: tuple[str, Path]
    ) -> None:
        """
        """
        state_name = core_props_container[0]
        core_props = core_props_container[1]

        texture_name = texture_props_container[0]
        texture_props = texture_props_container[1]

        if state_name != texture_name:
            raise NotImplementedError()

        super().__init__(
            name=state_name,
            movesets=core_props['movesets'],
            hp=core_props['hp'],
            death_damage_cap=core_props['death_damage_cap'],
            texture=texture_props
        )


class AlienConfig:
    """Configuration class for an alien.

    Contains at `self.config` a `dict` representation
    of TOML config and `pathlib.Path`s'
    to images of enemy states (see `load_texture_per_state`).
    """

    info: AlienInfo
    states: list[AlienState] = []

    def __init__(self, resource_dir: Path) -> None:
        """
        Raises
        ------
        NotImplementedError
            - If more than a single toml file was found in a folder
            - If error during reading to dict of a config was found
        """
        self._resource_dir = resource_dir
        self._config = {}
        self._resources = AlientResources(self._resource_dir, self._config)
        self.info = AlienInfo(self._resources.config['info'])
        structures_resources = zip(
            self._resources.config['state'].items(),
            self._resources.texture_paths.items()
        )
        # ((('initial', {'movesets': ['spiralling', 'escaping'], 'hp': 200, 'death_damage_cap': False}), ('initial', PosixPath('/home/kayman/git/mtt/tftm-alien-invasion/data/aliens/dummy_ufo/state.initial.png'))),)
        for resource_pair in structures_resources:
            self.states.append(AlienState(
                resource_pair[0],
                resource_pair[1]
            ))
