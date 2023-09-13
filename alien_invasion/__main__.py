import arcade as arc

from alien_invasion.constants import DISPLAY, WINDOW_TITLE

from alien_invasion.views import LoaderForView
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

    with LoaderForView("MainMenu", main_filter):
        arc.run()
