import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.settings import KEYMAP
from .sections import (
    PlayerArea,
)
from .scenes import (
    Background,
    AlienArea,
    PilotOverlay,
)

class Invasion(arc.View):
    def __init__(self) -> None:
        """Creates entity vars"""
        super().__init__()

        self.background = Background()

        self.player_area = PlayerArea(
            left=0, bottom=0,
            width=self.window.width,
            height=64,
            name="player_area",
            key_left=KEYMAP['player_starship_movement_left'],
            key_right=KEYMAP['player_starship_movement_right'],
            key_fire_primary=KEYMAP['player_starship_fire_primary'],
        )

        self.pilot_overlay = PilotOverlay(self.player_area)

        self.alien_area = AlienArea(self.player_area.starship)

        self.section_manager.add_section(self.player_area)
        self.window.set_mouse_visible(False)

    def setup(self) -> None:
        """Initialises entities"""
        self.game_state = CONSTANTS.GAME_STATE.RUNNING

    def on_draw(self) -> None:
        arc.start_render()
        self.background.draw()
        self.alien_area.draw()
        self.player_area.draw()
        self.pilot_overlay.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == KEYMAP['quit']:
            print('exiting ...')
            arc.exit()

    def on_update(self, delta_time: float):
        self.background.on_update(delta_time)
        self.alien_area.on_update(delta_time)
        self.player_area.on_update(delta_time)
        self.pilot_overlay.on_update(delta_time)
