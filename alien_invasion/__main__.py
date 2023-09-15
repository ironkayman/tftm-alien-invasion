import arcade as arc

from alien_invasion.constants import DISPLAY, WINDOW_TITLE

from alien_invasion.views import ViewLoader, MainMenu
from alien_invasion.utils.crt_filters import CRTFilterDefault


def main() -> None:
    """Creates instance of a game & launch it."""
    window = arc.Window(
        DISPLAY.WIDTH,
        DISPLAY.HEIGHT,
        WINDOW_TITLE,
    )
    window.gc_mode = "context_gc"
    window.ctx.gc()
    arc.enable_timings()

    main_filter = CRTFilterDefault(window)

    with ViewLoader(MainMenu, main_filter, progress_flag_count=4, is_root=True):
        arc.run()
