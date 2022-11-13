import arcade as arc
import arcade.gui

from alien_invasion import CONSTANTS

from alien_invasion.views.invasion.sections.backgroud_engine import BackgroundEngine

from .sections import HumanInterface

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
        self.background = arc.Sprite(
            texture=arc.load_texture(
                CONSTANTS.DIR_RESOURCES / 'images/background/entry_ns.png'
            ),
            scale=0.85,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 + 20,
            center_y=20
        )

        self.human_interface = HumanInterface(
            left=0, bottom=0,
            width=self.window.width,
            height=self.window.height,
            name="human_interface",
        )

        # self.section_manager.add_section(self.background_engine)
        self.section_manager.add_section(self.human_interface)

        self.window.set_mouse_visible(False)


    def on_draw(self) -> None:
        arc.start_render()
        self.background.draw(pixelated=True)
