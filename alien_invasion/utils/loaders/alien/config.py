"""Object respresention processor for any `Alien` entity
"""

from typing import cast, Generator
from pathlib import Path
from enum import IntEnum, auto

from pydantic import (
    BaseModel,
    validator,
    PrivateAttr,
)

from ..config.file_opener import reader

from alien_invasion.entities.common.loadout import Loadout

from alien_invasion.entities.common.state_manager import State
from alien_invasion.entities.common.state_manager.state import AlienType, AlienSize


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


class AlienConfig:
    """Configuration class for an alien.

    Contains at `self.config` a `dict` representation
    of TOML config and `pathlib.Path`s'
    to images of enemy states (see `load_texture_per_state`).

    Attributes
    ----------
    info : AlienInfo
        Inforamtion about specific `Alien`.
    states : list[State] = []
        Listed alien's states.
    """

    info: AlienInfo
    states: Generator[State, None, None] = []

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

        from alien_invasion.entities.common.state_manager import StateManager

        self.info = AlienInfo(self.config['info'])
        states = []
        for index, state in enumerate(self.config['state'].items()):
            state_name, state = state
            texture_path = self.define_state_texture_path(state_name)
            states.append({f'{state_name}': dict(
                name=state_name,
                index=index,
                data=state,
                texture_path=texture_path,
            )})
        self.states = StateManager(states)

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