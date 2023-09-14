from threading import Thread, Event
from importlib import import_module

import arcade as arc
import arcade.gui
from arcade.experimental.crt_filter import CRTFilter


from pyglet.media import Player

from alien_invasion.constants import DIR_MUSIC

# from alien_invasion.settings import CONFIG_DICT

from alien_invasion.utils.crt_filters import CRTFilterDefault
from alien_invasion import CONSTANTS


class LoaderForView(arc.View):
    """Loading Screen view."""

    def __init__(
        self,
        view: arc.View,
        view_filter: CRTFilter = None,
    ) -> None:
        """Wrapper around threaded view

        Parameters
        ----------
        view : arc.View
            Targeted `arc.View` class
        view_filter : CRTFilter
            View filter
        """
        super().__init__()

        self._next_view = view
        self._view_filter = view_filter

        # visual dot counter
        self.count = 0

        self.filter = CRTFilterDefault(self.window)

        # Intro audio
        self.media_player: Player | None = None
        self.theme = arc.Sound(
            DIR_MUSIC / "tape_in.opus",
            streaming=False,
        )

        # Create threading events
        self.f1, self.f2, self.f3, self.f4 = Event(), Event(), Event(), Event()
        self.next_view_instance = None
        self._thread = Thread(
            target=self._render_next_view,
            daemon=True,
            args=[self.f1, self.f2, self.f3, self.f4],
        )

    def _render_next_view(self, f1: Event, f2: Event, f3: Event, f4: Event):
        """Threaded func for showin selected view

        Show view from `self._next_view` and
        passes `f*` threading events.
        """
        module = import_module("alien_invasion.views")
        self._class_view = getattr(module, self._next_view)
        self.next_view_instance = self._class_view(
            self.window, self._view_filter, f1, f2, f3, f4
        )
        self.window.show_view(self.next_view_instance)

    def on_show_view(self):
        self.window.set_mouse_visible(True)

    def __enter__(self):
        self.window.show_view(self)
        self.media_player = self.theme.play(
            loop=True,
            volume=1.0,
            speed=1.0,
        )
        self._thread.start()
        return self

    def on_hide_view(self):
        self.media_player.delete()
        self.window.set_mouse_visible(False)

    def __exit__(self, exc_type, exc_value, tb):
        return

    def on_update(self, delta_time: float = 1 / 60):
        self.count += 1
        if self.count > 20:
            self.count = 0

    def on_draw(self):
        self.filter.use()
        self.filter.clear()

        arc.draw_text(
            f"Loading resources{'.' * self.count}",
            20 * CONSTANTS.DISPLAY.SCALE_RELATION,
            CONSTANTS.DISPLAY.HEIGHT - 40 * CONSTANTS.DISPLAY.SCALE_RELATION,
            arcade.color.WHITE,
            18 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
            bold=True,
        )
        if self.f1.is_set():
            arc.draw_text(
                "Loading Obelisk... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 76 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
        if self.f2.is_set():
            arc.draw_text(
                "Loading Golden Ridges... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 112 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
        if self.f3.is_set():
            arc.draw_text(
                "Loading Structure... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 148 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
        if self.f4.is_set():
            arc.draw_text(
                "Loading Human Adapter... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 184 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )

        self.window.use()
        self.filter.draw()
