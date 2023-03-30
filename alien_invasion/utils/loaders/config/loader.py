from pathlib import Path
from typing import Dict, Any, NoReturn

from .file_opener import reader
from .keymap import load_keymap_from_config
# from .starship import load_starship_loadout
from alien_invasion.entities.common.loadout import Loadout

def loader() -> Dict[str, Any]|NoReturn:
    config, error = reader(Path().cwd().joinpath('configs/config.json'))

    if error is not Ellipsis:
        print('\nConfig file error:', error)
        exit(0)

    keymap = load_keymap_from_config(config) # type: ignore
    starship = Loadout(config['starship'])

    return {
        'config': config,
        'starship': starship,
        'keymap': keymap
    }