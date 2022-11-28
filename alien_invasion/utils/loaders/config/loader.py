from pathlib import Path
from typing import Dict, Any, NoReturn

from .file_opener import reader
from .keymap import load_keymap_from_config
from .starship import load_starship_loadout

def loader() -> Dict[str, Any]|NoReturn:
    config, error = reader(Path().cwd().joinpath('configs/config.json'))

    if error is not Ellipsis:
        print('\nConfig file error:', error)
        exit(0)

    keymap = load_keymap_from_config(config) # type: ignore
    starship = load_starship_loadout(config)

    return {
        'config': config,
        'keymap': keymap
    }