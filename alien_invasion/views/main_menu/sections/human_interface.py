import arcade as arc
import arcade.gui

from alien_invasion.constants import DISPLAY

from alien_invasion.views import Invasion

from alien_invasion.settings import KEYMAP

class QuitButton(arc.gui.UIFlatButton):
    def on_click(self, event: arc.gui.UIOnClickEvent):
        arc.exit()

class HumanInterface(arc.Section):

    def __init__(
        self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        **kwargs,
    ) -> None:
        """
        """
        super().__init__(
            left,
            bottom,
            width,
            height,
            **kwargs
        )
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
        # arc.start_render()
        # self.clear()
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