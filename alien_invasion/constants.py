from pathlib import Path
from dataclasses import dataclass
from enum import IntEnum, auto

import arcade as arc


WINDOW_TITLE = "Tales From the Maelstorm: Alien Invasion"

PROJECT_SOURCE = Path().cwd() / "alien_invasion"

DIR_RESOURCES = PROJECT_SOURCE / 'resources'

DIR_MUSIC = DIR_RESOURCES / 'music'

DIR_IMAGES = DIR_RESOURCES / 'images'
DIR_SAVES = Path().cwd() / 'configs/saves'
DIR_DATA = Path().cwd() / 'data'
DIR_EQUIPMENT = DIR_DATA / 'starship'
DIR_ALIENS = DIR_DATA / 'aliens'
DIR_LEVELS = DIR_DATA / 'levels'
DIR_STARSHIP_CONFIG = DIR_RESOURCES / 'starship'

_HEIGHT = arc.get_display_size()[1] * 8/9

@dataclass(frozen=True)
class CL_DISPLAY:
    """Static setting for app on-screen dimensions."""

    SCALE_RELATION = (_HEIGHT) / 600
    WIDTH = int((_HEIGHT) * 4/3)
    HEIGHT = int(_HEIGHT)


DISPLAY = CL_DISPLAY()

@dataclass(frozen=True)
class GAME_STATE(IntEnum):
    """Main gameplay loop states."""
    RUNNING = auto()
    PAUSED = auto()
    QUIT = auto()
