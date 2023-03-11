from typing import cast
from pathlib import Path

from ..config.file_opener import reader


class AlientResources:

    IMAGE_FORMAT = 'png'

    config: dict
    texture_paths: dict[str, Path] = {}

    def __init__(self, resource_dir: Path, config: dict) -> None:
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
        file_name = f'state.{state_name}.{AlientResources.IMAGE_FORMAT}'
        image_path = self.resource_dir / file_name
        if not image_path.exists():
            raise FileNotFoundError('alien state texture', file_name, 'not found')
        return image_path


    def compile_entity_directory_contents(self):
        # check config file
        if (config_files := list(self.resource_dir.glob('*.toml'))) and \
            len(config_files) > 1:
            raise NotImplementedError('One config per folder/alien')

        config, error = reader(config_files[0])

        if error is not Ellipsis:
            raise NotImplementedError(error)
        self.config = cast(dict, config)

        # check states
        for state_name in self.config['state'].keys():
            self.texture_paths[
                state_name
            ] = self.define_state_texture_path(state_name)
