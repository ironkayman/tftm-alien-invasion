from pathlib import Path
from dataclasses import dataclass
from enum import IntEnum, auto

WINDOW_TITLE = "Tales From the Maelstorm: Alien Invasion"

PROJECT_SOURCE = Path().cwd() / "alien_invasion"

DIR_RESOURCES = PROJECT_SOURCE / 'resources'
DIR_IMAGES = DIR_RESOURCES / 'images'
DIR_SAVES = Path().cwd() / 'configs/saves'
DIR_DATA = Path().cwd() / 'data'
DIR_EQUIPMENT = DIR_DATA / 'starship'

@dataclass(frozen=True)
class CL_DISPLAY:
    """Static setting for app on-screen dimensions."""
    WIDTH = 800
    HEIGHT = 600

DISPLAY = CL_DISPLAY()


@dataclass(frozen=True)
class GAME_STATE(IntEnum):
    """Main gameplay loop states."""
    RUNNING = auto()
    PAUSED = auto()
    QUIT = auto()
