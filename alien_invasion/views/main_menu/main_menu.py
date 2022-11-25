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

        # self.background = arc.Sprite(
        #     texture=arc.load_texture(
        #         CONSTANTS.DIR_RESOURCES / 'images/background/main_menu.png'
        #     ),
        #     scale=0.95,
        #     center_x=CONSTANTS.DISPLAY.WIDTH // 2 + 20,
        #     center_y=160
        # )
        # self.background = arc.Sprite(
        #     texture=arc.load_texture(
        #         CONSTANTS.DIR_RESOURCES / 'images/background/main_menu_cold.png'
        #     ),
        #     scale=0.35,
        #     center_x=CONSTANTS.DISPLAY.WIDTH // 2 - 30,
        #     center_y=CONSTANTS.DISPLAY.HEIGHT // 2
        # )
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

        # self.window.set_mouse_visible(False)

    def on_show_view(self) -> None:
        self.human_interface.manager.enable()

    def on_draw(self) -> None:
        arc.start_render()
        # self.background.draw(pixelated=False)
