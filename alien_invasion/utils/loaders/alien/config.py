"""Object respresention processor for any `Alien` entity
"""

from typing import cast
from pathlib import Path
from enum import IntEnum, auto

from pydantic import (
    BaseModel,
    validator,
    PrivateAttr,
)

from ..config.file_opener import reader

from alien_invasion.entities.common.loadout import Loadout


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

    # required kwargs
    movesets: set[AlienMoveset]
    speed: int
    hp: int
    death_damage_cap: bool

    # overrides of prev state, optional
    bullet_damage: int | None
    bullet_speed: int | None
    recharge_timeout: int | None

    # hidden
    _state_name: str = PrivateAttr()
    _state_data: dict = PrivateAttr()
    _texture_path: Path = PrivateAttr()

    # created from given values loadout maybe always reload from pydantic keys
    _loadout: Loadout = PrivateAttr()

    @validator('movesets', pre=True)
    def get_movesets(cls, val) -> set[AlienMoveset]:
        """Turns moveset string names to Enums"""
        return set(map(lambda m: AlienMoveset[m], val))

    def __init__(self,
        state_name: str,
        texture_path: Path,
        state_data: dict,
    ) -> None:
        """Maps groups of entity's properties to a coherent data structure

        Parameters
        ----------
        state_name : str
            State's name.
        texture_path : Path
            Corresponding texture to a given state by its name att `state_name`.
        state_data : dict
            All data from `::state:state_name`.

        Examples
        --------
        >>> state_name
        'initial'
        >>> state_data
        {
            'movesets': ['tracking'],
            'speed': 90,
            'hp': 20,
            'death_damage_cap': False,
            'bullet_damage': 8,
            'bullet_speed': 800,
            'recharge_timeout': 300
        }
        >>> texture_path
        PosixPath('/home/kayman/git/mtt/tftm-alien-invasion/data/aliens/dummy_ufo/state.initial.png')
        """
        self._state_name = state_name
        self._state_data = state_data
        self._texture_path = texture_path

        super().__init__(**self._state_data)


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

    info: AlienInfo
    states: list[AlienState] = []

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

        self._resource_dir = resource_dir

        if (config_files := list(self._resource_dir.glob('*.toml'))) and \
            len(config_files) > 1:
            raise NotImplementedError('One config per folder/alien')

        config, error = reader(config_files[0])


        if error is not Ellipsis:
            raise NotImplementedError(error)
        self.config = cast(dict, config)

        self.info = AlienInfo(self.config['info'])
        for state_name, state in self.config['state'].items():
            texture_path = self.define_state_texture_path(state_name)
            self.states.append(AlienState(
                state_name=state_name,
                state_data=state,
                texture_path=texture_path,
            ))

    def define_state_texture_path(self, state_name: str) -> Path:
        """Checks alien config for image-state pair.

        This means that for avery enemy state there's a
        required texture as a png file with state's name.
        If image is successfully found, save its `pathlib.Path`
        to states' `image_path` key to be loaded later at *runtime*.

        Paramters
        ---------
        state_name: str
            Name of existing `Alien` state defined at central config file.

        Returns
        -------
        Path
            `pathlib.Path` object to state's texture.

        Raises
        ------
        FileNotFoundError
            If no state-texture was found for any
            of described at alien config's states.
        """
        # texture foir a state file naming pattern
        file_name = f'state.{state_name}.png'
        image_path = self._resource_dir / file_name
        if not image_path.exists():
            raise FileNotFoundError('alien state texture', file_name, 'not found')
        return image_path