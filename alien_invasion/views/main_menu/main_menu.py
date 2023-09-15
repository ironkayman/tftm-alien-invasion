from threading import Event

import arcade as arc
import arcade.gui
from pyglet.media import Player

from alien_invasion.constants import DIR_MUSIC
from alien_invasion.settings import CONFIG_DICT

from .scenes import Obelisk, Outlines, Ruins
from .sections import Interface

from alien_invasion.utils.crt_filters import CRTFilterDefault


class MainMenu(arc.View):
    """Main menu view."""

    SFX_MAIN: float = 0.3
    SFX_BUTTON_PRESS: float = 0.4

    def __init__(
        self,
        window: arc.Window = None,
        view_filter=None,
        flags: (Event) = None,
    ) -> None:
        """ """
        super().__init__(window=window)

        self.filter = view_filter or CRTFilterDefault(self.window)

        self.obelisk = Obelisk()
        flags[0].set()
        self.outlines = Outlines()
        flags[1].set()
        self.ruins = Ruins()
        flags[2].set()

        # isolate UI
        self.human_interface = Interface(
            left=0,
            bottom=0,
            width=self.window.width,
            height=self.window.height,
            name="human_interface",
        )
        self.section_manager.add_section(self.human_interface)
        flags[3].set()

        self.media_player: Player | None = None
        self.theme = arc.Sound(
            DIR_MUSIC / "main_menu.opus",
            streaming=False,
        )

    def on_show_view(self) -> None:
        self.window.set_mouse_visible(False)
        self.human_interface.manager.enable()

        self.human_interface.reset_widget_selection()
        self.human_interface.selected_index = 1
        self.human_interface.get_widget().hovered = True

        self.media_player = self.theme.play(
            loop=True,
            volume=0.3 if not CONFIG_DICT["config"]["mute"] else 0.0,
            speed=1.0,
        )

    def on_hide_view(self) -> None:
        self.human_interface.manager.disable()
        self.theme.stop(self.media_player)

    def on_update(self, delta_time: float):
        self.obelisk.on_update(delta_time)
        self.outlines.on_update(delta_time)
        self.ruins.on_update(delta_time)

    def on_draw(self) -> None:
        """Render

        - renders `obelisk` structure under 2 filter layers
        - `outline` is rendered with 1 filter (inherited by next render) layer
        - `ruins` and `human_interface` are drawn with 1 filter layer
        """
        self.filter.use()
        self.filter.clear()

        self.obelisk.draw()

        # self.filter.draw()

        self.outlines.draw()

        # self.filter.use()

        self.ruins.draw()
        self.human_interface.draw()

        self.window.use()
        self.filter.draw()

    def _toggle_mute_main_theme(self) -> None:
        """Toggle volume of main menu theme"""
        self.media_player.volume = 0.0 if self.media_player.volume else self.SFX_MAIN
