import arcade as arc
import arcade.gui
from pyglet.media import Player

from alien_invasion.constants import DIR_MUSIC

from .scenes import Background
from .sections import Interface


class MainMenu(arc.View):
    """Main menu view."""

    def __init__(self) -> None:
        super().__init__()

        self.background = Background()
        # print('factor', arc.get_scaling_factor())

        # isolate UI
        self.human_interface = Interface(
            left=0,
            bottom=0,
            width=self.window.width,
            height=self.window.height,
            name="human_interface",
        )

        self.section_manager.add_section(self.human_interface)

        self.media_player: Player | None = None
        self.theme = arc.Sound(
            DIR_MUSIC / "main_menu.opus",
            streaming=False,
        )

    def on_show_view(self) -> None:
        self.human_interface.manager.enable()

        self.human_interface.reset_widget_selection()
        self.human_interface.selected_index = 1
        self.human_interface.get_widget().hovered = True

        self.media_player = self.theme.play(
            loop=True,
            volume=0.3,
            speed=1.0,
        )

    def on_hide_view(self) -> None:
        self.human_interface.manager.disable()
        self.theme.stop(self.media_player)

    def on_update(self, delta_time: float):
        self.background.on_update(delta_time)

    def on_draw(self) -> None:
        arc.start_render()
        self.background.draw()
        self.human_interface.draw()
