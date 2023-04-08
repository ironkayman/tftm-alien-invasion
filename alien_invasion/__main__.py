import arcade as arc

from alien_invasion.constants import (
    DISPLAY, WINDOW_TITLE
)

from alien_invasion.views import MainMenu

def main() -> None:
    """Creates instance of a game & launch it."""
    window = arc.Window(
        DISPLAY.WIDTH,
        DISPLAY.HEIGHT,
        WINDOW_TITLE,
    )
    arc.enable_timings()
    game = MainMenu()
    window.show_view(game)
    arc.run()
