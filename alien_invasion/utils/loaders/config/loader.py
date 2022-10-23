from typing import Dict, Any

import arcade 

from .file_opener import reader
from .keymap import load_keymap

def loader() -> Dict[str, Any]:
    config, error = reader()

    if error is not Ellipsis:
        print('\n\n config file error:', error)

    keymap = load_keymap(config)

    return {
        'config': config,
        'keymap': keymap
    }