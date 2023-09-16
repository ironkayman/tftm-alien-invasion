from threading import Thread, Event
from queue import Queue

import arcade as arc
import arcade.gui
from arcade.experimental.crt_filter import CRTFilter


from pyglet.media import Player

from alien_invasion.constants import DIR_MUSIC

# from alien_invasion.settings import CONFIG_DICT

from alien_invasion.utils.crt_filters import CRTFilterDefault
from alien_invasion import CONSTANTS


class ViewLoader(arc.View):
    """Loading Screen view."""

    def __init__(
        self,
        view: arc.View,
        view_filter: CRTFilter = None,
        progress_flag_count: int = 3,
        is_root: bool = False,
    ) -> None:
        """Displays `LoaderView` for a period of `view` loading.

        Parameters
        ----------
        view : arc.View
            Targeted `View` class
        view_filter : CRTFilter
            Filter instance that is applied to a target view
        is_root : Bool
            Does this instnce wrap the arcade.run function
        """
        super().__init__()

        self._next_view = view
        self._view_filter = view_filter
        self.is_root = is_root

        # visual dot counter
        self.__trailing_count = 0

        self.filter = CRTFilterDefault(self.window)

        # Intro audio
        self.media_player: Player | None = None
        self.theme = arc.Sound(
            DIR_MUSIC / "tape_in.opus",
            streaming=False,
        )
        self._queue = Queue()
        # prepare passable events
        self._progress_events = [Event() for _ in range(progress_flag_count + 1)]
        # breakpoint()
        self._target_view_loaded = Event()
        self._thread = Thread(
            target=ViewLoader._render_next_view,
            daemon=True,
            args=[
                self._queue,
                self._next_view,
                self.window,
                self.filter,
                self._progress_events,
                self._target_view_loaded,
            ],
        )

    @staticmethod
    def _render_next_view(
        queue: Queue,
        target_view: arc.View,
        window: arc.Window,
        view_filter: CRTFilter,
        progress_flags: list[Event],
        closing_event: Event,
    ):
        """Loads view in `_thread` thread, appends the result to `queue`

        Parameters
        ----------
        queue : Queue
            Synchronious queue of tasks in which result is being put
        target_view : arc.View
            View to load
        window : arc.Window
            Window to pass
        view_filter : CRTFilter
            View CRTfilter to apply to
        progress_flags : list[Event]
            A list of flags to set from a targt view
        closing_event : Event
            Event set at the end of threaded function
        """
        queue.put(
            target_view(
                window,
                view_filter,
                progress_flags,
            )
        )
        closing_event.set()

    def on_show_view(self):
        self.window.set_mouse_visible(True)

    def __enter__(self):
        self._thread.start()
        self.window.show_view(self)
        self.media_player = self.theme.play(
            loop=True,
            volume=1.0,
            speed=1.0,
        )
        return self

    def on_hide_view(self):
        self.media_player.delete()
        self.window.set_mouse_visible(False)

    def __exit__(self, exc_type, exc_value, tb):
        if not self.is_root:
            self._thread.join()

    def on_update(self, _: float = 1 / 60):
        """Update the view

        Updates the view. Checks `_thread`ed
        view completion and if so, switches to it.
        """
        self.__trailing_count += 1
        if self.__trailing_count > 20:
            self.__trailing_count = 0

        # check for created view instance
        if self._target_view_loaded.is_set():
            self._thread.join()
            self.window.show_view(self._queue.get())

    def on_draw(self):
        self.filter.use()
        self.filter.clear()

        arc.draw_text(
            f"Loading resources{'.' * self.__trailing_count}",
            20 * CONSTANTS.DISPLAY.SCALE_RELATION,
            CONSTANTS.DISPLAY.HEIGHT - 40 * CONSTANTS.DISPLAY.SCALE_RELATION,
            arcade.color.WHITE,
            18 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
            bold=True,
        )
        if self._progress_events[0].is_set():
            arc.draw_text(
                "Loading Obelisk... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 76 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
        if self._progress_events[1].is_set():
            arc.draw_text(
                "Loading Golden Ridges... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 112 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
        if self._progress_events[2].is_set():
            arc.draw_text(
                "Loading Structure... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 148 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
        if self._progress_events[3].is_set():
            arc.draw_text(
                "Loading Human Adapter... OK",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 184 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.WHITE,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )
            arc.draw_text(
                "Loading Narraphysic Isolation Env... MALFUNC",
                20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                CONSTANTS.DISPLAY.HEIGHT - 220 * CONSTANTS.DISPLAY.SCALE_RELATION,
                arcade.color.CRIMSON,
                18 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
                bold=True,
            )

        self.window.use()
        self.filter.draw()
