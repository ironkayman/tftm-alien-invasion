import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.settings import KEYMAP
from .sections import (
    PlayerArea,
)
from alien_invasion.utils.loaders.level import loader as load_levels

from .scenes import (
    Background,
    Level,
    PilotOverlay,
    GameOver,
)


class Invasion(arc.View):
    def __init__(self, completion_callback_view: arc.View) -> None:
        """Creates entity vars"""
        super().__init__()

        self.on_pause = False

        self.completion_callback_view = completion_callback_view

        self.game_over = GameOver()

        self.player_area = PlayerArea(
            left=0, bottom=0,
            width=self.window.width,
            height=64,
            name="player_area",
            key_left=KEYMAP['player_starship_movement_left'],
            key_right=KEYMAP['player_starship_movement_right'],
            key_fire_primary=KEYMAP['confirm'],
            key_fire_secondary=KEYMAP['fire_secondary'],
            key_on_pause=KEYMAP['pause'],
            parent_view=self,
        )

        self.pilot_overlay = PilotOverlay(self.player_area)

        self.LEVELS = load_levels()
        self.level: Level = self.LEVELS[0]

        self.background = Background(self.level.title_image_path)

        self.section_manager.add_section(self.player_area)
        self.window.set_mouse_visible(False)

    def setup(self) -> None:
        """Initialises entities"""
        # move passing of bullet lists outside of starship
        # for more transparency
        self.level.setup(self.player_area.starship)

    def on_draw(self) -> None:
        arc.start_render()
        self.background.draw()
        self.level.draw()
        self.player_area.draw()
        if self.level.starship.can_reap():
            self.game_over.draw()
            return
        self.pilot_overlay.draw()

    # def on_key_press(self, symbol: int, modifiers: int) -> None:
    #     if symbol == KEYMAP['pause']:
    #         self.on_pause = not self.on_pause
    #         # print('exiting ...')
    #         # arc.exit()

    def on_update(self, delta_time: float) -> None:
        """
        """

        if self.on_pause: return

        self.background.on_update(delta_time)
        self.level.on_update(delta_time)
        self.player_area.on_update(delta_time)
        if self.level.starship.can_reap():
            self.game_over.on_update(delta_time)
            return
        self.pilot_overlay.on_update(delta_time)

        if self.level.is_finished:
            self.window.show_view(self.completion_callback_view)
