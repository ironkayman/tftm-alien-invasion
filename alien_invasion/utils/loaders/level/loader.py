from typing import cast, Generator
from pathlib import Path

from alien_invasion import CONSTANTS

from ..config.file_opener import reader


def loader() -> list[tuple[dict, Path]]:
    """Gets predifined levels in a Generator object.

    Returns
    -------
    list[Level]
    """
    levels = []
    for level_dir in CONSTANTS.DIR_LEVELS.iterdir():
        level_file = level_dir / 'level.toml'
        title_image = level_dir / 'title.png'
        level_config, error = reader(level_file)
        level_config = cast(dict, level_config)
        if error is not Ellipsis:
            raise NotImplementedError(error)
        levels.append((level_config, title_image))
    return levels