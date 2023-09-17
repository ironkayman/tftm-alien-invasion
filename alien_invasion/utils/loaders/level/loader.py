from alien_invasion import CONSTANTS

from .model import LevelConfiguration


def loader() -> list[LevelConfiguration]:
    """Gets predifined levels in a Generator object.

    Skips levels whose folders end with `.ignore`.

    Returns
    -------
    list[LevelConfiguration]
        List of level configurations
        represented as Pydantic models
    """
    levels = []
    for level_dir in CONSTANTS.DIR_LEVELS.iterdir():
        if level_dir.name.endswith(".ignore"):
            continue
        level = LevelConfiguration(level_dir)
        # if level.error: continue
        levels.append(level)
    return levels
