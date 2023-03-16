"""Object respresention processor for any `Alien` entity.
"""

from pathlib import Path
from enum import IntEnum, auto

from pydantic import BaseModel, validator

from .entity_dir import AlientResources


class AlienSize(IntEnum):
    """Allowed enemy sizes"""

    small = auto()
    medium = auto()
    large = auto()
    colossal = auto()
    unimaginable = auto()


class AlienType(IntEnum):
    """Allowed enemy types"""

    # Tier 1
    corporeal = auto()
    ancient = auto()
    # Tier 2
    possessed = auto()
    undead = auto()
    # Tier 3
    narrativistic = auto()
    metaphysic = auto()


class AlienInfo(BaseModel):
    """Structured representation of `info` block of alien's central config.

    Attrbutes
    ---------
    name: str
        Alien's vusible name.
    size: str
        Aliens size.
    xp: int
        Amount of Experience gained.
    type: set[AlienType]
        Alien's enemy types.
    """

    name: str
    size: str
    xp: int
    type: set[AlienType]

    def __init__(self, info_config: dict) -> None:
        super().__init__(**info_config)

    @validator('size', pre=True)
    def get_alien_size_enum(cls, val: str) -> AlienSize:
        """Alien's Size naming - Str -> IntEnum mapping"""
        return AlienSize[val]

    @validator('type', pre=True)
    def get_alien_type_enum(cls, val: list) -> set[AlienType]:
        """Alien's Type naming - Str -> IntEnum mapping"""
        return set(map(lambda c: AlienType[c], val))


class AlienMoveset(IntEnum):
    """Allowed movesets for an arbitrary state.

    Attributes
    ----------
    spiralling : int
        Flies across screen (left<->right) in overlapping circles.
    tracking : int
        Vaguely follows starship's x-axis and when needed dodges bullets.
    escaping : int
        Opposite of `tracking`, tries never to cross x-axis of a starship.
    """

    spiralling = auto()
    tracking = auto()
    escaping = auto()


class AlienState(BaseModel):
    """Scheme for `Alien` states data strcture

    Attributes
    ----------
    name: str
        State name.
    movesets: set[AlienMoveset]
        Movesets available for this alien's state represented as Enums.
    hp: int
        HitPoints for this state.
    death_damage_cap: bool
        Does damage beyond hp = 0 is translated to damage to alen's nex state.
        `True` - damage is capped whch means that next state does not
        absorb this state's incoming damage.
        `False` - remaining from hp = 0 damage is absorbed by
        next alien's state if any present, dealng damage to its HP bar.
    texture: Path
        Path to a state's texure.
    """

    name: str
    movesets: set[AlienMoveset]
    hp: int
    death_damage_cap: bool
    texture: Path

    @validator('movesets', pre=True)
    def get_movesets(cls, val) -> set[AlienMoveset]:
        """Turns moveset string names to Enums"""
        return set(map(lambda m: AlienMoveset[m], val))

    def __init__(self,
        core_props_container: tuple[str, dict],
        texture_props_container: tuple[str, Path]
    ) -> None:
        """Maps groups of entity's properties to a coherent data structure

        Parameters
        ----------
        core_props_container: tuple[str, dict]
            Tupled pair of specific state name
            and it's internal properties.

            NOTE: Naming conventions:
                One would consider `core_` preperties
                as primary information, not the states.
        texture_props_container: tuple[str, Path]
            Tuple of alien's state [0] and
            its designated `Path` to a texture.
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

    Attributes
    ----------
    info: AlienInfo
        Inforamtion about specific `Alien`.
    states: list[AlienState] = []
        Listed alien's states.
    """


    def __init__(self, resource_dir: Path) -> None:
        """Constructs universal object representation of `Alien`.

        Consructs data structure of mapped properties from entity's
        config directory by mapping out the paths to specific resources
        and saving them at finalised config file object.

        Raises
        ------
        NotImplementedError
            - If more than a single toml file was found in a folder
            - If error during reading to dict of a config was found
        """

        self.info: AlienInfo
        self.states: list[AlienState] = []

        self._resource_dir = resource_dir
        print('resource_dir', resource_dir)
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
