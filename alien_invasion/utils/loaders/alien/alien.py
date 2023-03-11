from typing import cast, Any
from pathlib import Path

from ..config.file_opener import reader

from alien_invasion import CONSTANTS


class AlienConfig:
    """Configuration entity for alien.

    Contains dict-like TOML config and `pathlib.Path`s'
    to images of alien states.
    """

    IMAGE_FORMAT = "png"

    def __init__(self, resource_dir: Path) -> None:
        self.resource_dir = resource_dir
        if (config_files := list(resource_dir.glob('*.toml'))) and len(config_files) > 1:
            raise NotImplementedError('One config per folder/alien')

        config, error = reader(config_files[0])

        if error is not Ellipsis:
            raise NotImplementedError(error)
        self.config = cast(dict, config)

        self.load_texture_per_state()

    def load_texture_per_state(self):
        for state_name in self.config['state'].keys():
            file_name = f'state.{state_name}.{AlienConfig.IMAGE_FORMAT}'
            image_path = self.resource_dir / file_name
            if not image_path.exists():
                raise FileNotFoundError('alien state texture', file_name, 'not found')
            self.config['state'][state_name]['image_path'] = image_path

def loader() -> list[AlienConfig]:
    """Creates configs-dicts for all aliens forund in data directory.

    Returns
    -------
    list[AlienConfig]
        List of AlienConfig objects containing
        information + texture paths of entities.
    """
    alien_configs = []
    for alien_folder in CONSTANTS.DIR_ALIENS.iterdir():
        # ignore folders with .skip in its' names
        if alien_folder.name.endswith('.skip'): continue

        alien_configs.append(AlienConfig(alien_folder))
    return alien_configs
