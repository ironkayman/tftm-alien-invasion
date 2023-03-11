from typing import cast, Any
from pathlib import Path

from pydantic import BaseModel

from .config import AlienConfig
from alien_invasion import CONSTANTS


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
