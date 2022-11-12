import arcade as arc
import arcade.gui

from alien_invasion import CONSTANTS

from alien_invasion.views import Invasion

from alien_invasion.settings import KEYMAP


from alien_invasion.views.invasion.sections.backgroud_engine import BackgroundEngine

# from .sections import HumanInterface

class QuitButton(arc.gui.UIFlatButton):
    def on_click(self, event: arc.gui.UIOnClickEvent):
        arc.exit()

class MainMenu(arc.View):
    """Main menu view."""

    def __init__(self) -> None:
        super().__init__()

        self.background = arc.Sprite(
            texture=arc.load_texture(
                CONSTANTS.DIR_RESOURCES / 'images/background/main_menu.png'
            ),
            scale=0.95,
            center_x=CONSTANTS.DISPLAY.WIDTH // 2 + 20,
            center_y=160
        )

        self.background_engine = BackgroundEngine(
            left=1000, bottom=0,
            width=self.window.width,
            height=self.window.height,
            prevent_dispatch_view=False,
            # prevent_dispatch={True},
            # prevents events to propagate to the view
            # prevent_dispatch_view={True},
            # prevents arcade events capture
            accept_keyboard_events=False,
            name="background_engine",
        )

        # self.human_interface = HumanInterface(
        #     left=0, bottom=0,
        #     width=self.window.width,
        #     height=self.window.height,
        #     name="human_interface",
        # )

        # self.section_manager.add_section(self.background_engine)
        # self.section_manager.add_section(self.human_interface, 444)

        self.window.set_mouse_visible(True)

        # a UIManager to handle the UI
        self.manager = arc.gui.UIManager(self.window)
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arc.gui.UIBoxLayout()

        # Create the buttons
        start_button = arc.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        @start_button.event("on_click")
        def on_click_start_invasion(event):
            print("Starting...", event)
            invasion_view = Invasion()
            invasion_view.setup()
            self.window.show_view(invasion_view)

        # Again, method 1. Use a child class to handle events.
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arc.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
            )
        )




    def on_draw(self) -> None:
        self.clear()
        arc.start_render()
        self.background.draw(pixelated=True)
        self.manager.draw()
        # print(arc.gui.UIEvent)


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == KEYMAP['start']:
            print('starting ...')
            invasion_view = Invasion()
            invasion_view.setup()
            self.window.show_view(invasion_view)
        elif symbol == KEYMAP['quit']:
            print('exitiing ...')
            arc.exit()