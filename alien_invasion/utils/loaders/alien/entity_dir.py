"""Module for `Alien` resources' scheme

Module contains `Alien`-class specific logic for loading
from a directory before `Alien`-instance creation.
"""

from typing import cast
from pathlib import Path

from ..config.file_opener import reader


class AlientResources:
    """Accumulates and binds textures to central entity config.

    Checks main config and binds textures to it,
    creating universal config for `Alien` initialisation.
    """

    IMAGE_FORMAT = 'png'

    def __init__(self, resource_dir: Path, config: dict) -> None:
        """Prepares director location and build resource config.

        Parameters
        ----------
        resource_dir: Path
            `pathlib.Path` object to directory wih config and resources.
        config: dict
            External pointer to save finalised annd structured data into.
        """
        self.texture_paths: dict[str, Path] = {}

        self.resource_dir = resource_dir
        self.config = config
        # loads texture_paths, overwrites given self.config
        self.compile_entity_directory_contents()

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
        file_name = f'state.{state_name}.{AlientResources.IMAGE_FORMAT}'
        image_path = self.resource_dir / file_name
        if not image_path.exists():
            raise FileNotFoundError('alien state texture', file_name, 'not found')
        return image_path

    def compile_entity_directory_contents(self):
        """Checks config file and loads its resources.

        1. Reads config file itself, then saves defined there states.
        2. Maps state names onto files frim the resource drectory,
        saving their paths.
        """
        # check config file
        if (config_files := list(self.resource_dir.glob('*.toml'))) and \
            len(config_files) > 1:
            raise NotImplementedError('One config per folder/alien')

        config, error = reader(config_files[0])

        if error is not Ellipsis:
            raise NotImplementedError(error)
        self.config = cast(dict, config)

        for state_name in self.config['state'].keys():
            self.texture_paths[
                state_name
            ] = self.define_state_texture_path(state_name)
