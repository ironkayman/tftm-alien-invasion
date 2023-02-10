import arcade as arc
import arcade.gui

from alien_invasion import CONSTANTS


from .sections import HumanInterface
from .scenes import Background


class MainMenu(arc.View):
    """Main menu view."""

    def __init__(self) -> None:
        super().__init__()

        self.background = Background()

        # isolate UI
        self.human_interface = HumanInterface(
            left=0, bottom=0,
            width=self.window.width,
            height=self.window.height,
            name="human_interface",
        )

        self.section_manager.add_section(self.human_interface)

    def on_show_view(self) -> None:
        self.human_interface.manager.enable()

    def on_update(self, delta_time: float):
        self.background.on_update(delta_time)

    def on_draw(self) -> None:
        arc.start_render()
        self.background.draw()
        self.human_interface.draw()
