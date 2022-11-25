import arcade as arc
import arcade.gui

from alien_invasion import CONSTANTS

from alien_invasion.views.invasion.sections.backgroud_engine import BackgroundEngine

from .sections import HumanInterface
from .sections import Background


class MainMenu(arc.View):
    """Main menu view."""

    def __init__(self) -> None:
        super().__init__()

        self.background = Background(
            left=0, bottom=0,
            width=self.window.width,
            height=self.window.height,
            name="background",
        )

        self.human_interface = HumanInterface(
            left=0, bottom=0,
            width=self.window.width,
            height=self.window.height,
            name="human_interface",
        )

        self.section_manager.add_section(self.background)
        self.section_manager.add_section(self.human_interface)

    def on_show_view(self) -> None:
        self.human_interface.manager.enable()

    def on_draw(self) -> None:
        arc.start_render()
