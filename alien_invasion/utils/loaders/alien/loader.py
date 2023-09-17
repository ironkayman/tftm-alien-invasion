"""Main loader for `Alien` configs

Accumultaes every `Alien` to their
designanted `AlienConfig` configuration object.
"""

from .config import AlienConfig
from alien_invasion import CONSTANTS


def load_alien_by_name(alien_name: str) -> AlienConfig:
    """Loads alien config by its service name.

    Returns
    -------
    AlienConfig
        Returns alien's config if alien is found.
    """
    alien_folder = CONSTANTS.DIR_ALIENS / alien_name
    # ignore folders with .skip in its' names
    if alien_folder.name.endswith(".skip"):
        raise NotImplementedError("cant skip alien whom required by a specific wave")
    return AlienConfig(alien_folder)
