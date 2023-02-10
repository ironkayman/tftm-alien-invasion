import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.settings import KEYMAP
from .sections import (
    AlienArea,
    PlayerArea,
    PilotOverlay,
)
from .scenes import (
    Background,
)

class Invasion(arc.View):
    def __init__(self) -> None:
        """Creates entity vars"""
        super().__init__()

        self.background = Background()

        self.alien_area = AlienArea(
            left=0, bottom=0,
            width=self.window.width,
            height=self.window.height,
            # prevents arcade events capture
            accept_keyboard_events=False,
            name="alien_area",
        )

        self.player_area = PlayerArea(
            left=0, bottom=0,
            width=self.window.width,
            height=64,
            key_left=KEYMAP['player_starship_movement_left'],
            key_right=KEYMAP['player_starship_movement_right'],
            key_fire_primary=KEYMAP['player_starship_fire_primary'],
            name="player_area"
        )

        self.pilot_overlay = PilotOverlay(
            left=0, bottom=0,
            width=self.window.width,
            height=self.window.height,
            # prevents arcade events capture
            accept_keyboard_events=False,
            name="pilot_overlay",
        )

        # self.section_manager.add_section(self.background_engine)
        self.section_manager.add_section(self.alien_area)
        self.section_manager.add_section(self.player_area)
        self.section_manager.add_section(self.pilot_overlay)

        self.window.set_mouse_visible(False)

    def setup(self) -> None:
        """Initialises entities"""
        self.game_state = CONSTANTS.GAME_STATE.RUNNING

    def on_draw(self) -> None:
        arc.start_render()
        self.background.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == KEYMAP['quit']:
            print('exiting ...')
            arc.exit()

    def on_update(self, delta_time: float):
        self.background.on_update(delta_time)
