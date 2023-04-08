from typing import cast, Generator

from alien_invasion import CONSTANTS

from ..config.file_opener import reader

from alien_invasion.views.invasion.scenes import Level

def loader() -> Generator[Level, None, None]:
    """Gets predifined levels in a Generator object.

    Returns
    -------
    Generator[Level, None, None]
        Storees every `Level` object inside a `Generator`.
    """
    for level_dir in CONSTANTS.DIR_LEVELS.iterdir():
        level_file = level_dir / 'level.toml'
        title_image = level_dir / 'title.png'
        level_config, error = reader(level_file)
        level_config = cast(dict, level_config)
        if error is not Ellipsis:
            raise NotImplementedError(error)
        yield Level(level_config, title_image)