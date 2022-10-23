import arcade as ac

from alien_invasion.constants import DISPLAY

from alien_invasion.views import Invasion

from alien_invasion.settings import KEYMAP

class MainMenu(ac.View):
    """Main menu view."""

    def on_show_view(self) -> None:
        ac.set_background_color(ac.color.WHITE)

    def on_draw(self) -> None:
        self.clear()
        ac.draw_text(
            "Menu Screen",
            DISPLAY.WIDTH / 2,
            DISPLAY.HEIGHT / 2,
            ac.color.BLACK,
            font_size=50,
            anchor_x="center",
            font_name="Kenney Rocket",
        )
        ac.draw_text(
            "Enter",
            DISPLAY.WIDTH / 2,
            DISPLAY.HEIGHT * 1/3,
            ac.color.GRAY,
            font_size=40,
            anchor_x="center",
            font_name="Kenney Rocket",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == KEYMAP['start']:
            print('starting ...')
            invasion_view = Invasion()
            invasion_view.setup()
            self.window.show_view(invasion_view)
        elif symbol == KEYMAP['quit']:
            print('exitiing ...')
            ac.exit()