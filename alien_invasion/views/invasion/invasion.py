import arcade as arc
from pathlib import Path

from alien_invasion import CONSTANTS
from alien_invasion.settings import KEYMAP
from .sections import (
    PlayerArea,
)
from alien_invasion.utils.crt_filters import CRTFilterDefault

from .scenes import (
    Background,
    Level,
    PilotOverlay,
    GameOver,
)


class Invasion(arc.View):
    def __init__(
        self, completion_callback_view: arc.View, mission_config: tuple[dict, Path]
    ) -> None:
        """Creates entity vars

        Parameters
        ----------
        completion_callback_view : arc.View
            View to return to at level completion/exit/death.
        mission_config : tuple[dict, Path]
            A pair of objects: mission's config represented as dict,
            and title image path.
        """
        super().__init__()

        self.filter = CRTFilterDefault(self.window)

        self.on_pause = False

        self.completion_callback_view = completion_callback_view

        self.game_over = GameOver()

        self.player_area = PlayerArea(
            left=0,
            bottom=0,
            width=CONSTANTS.DISPLAY.WIDTH,
            height=CONSTANTS.DISPLAY.HEIGHT,
            name="player_area",
            key_left=KEYMAP["player_starship_movement_left"],
            key_right=KEYMAP["player_starship_movement_right"],
            key_up=KEYMAP["player_starship_movement_up"],
            key_down=KEYMAP["player_starship_movement_down"],
            key_fire_primary=KEYMAP["confirm"],
            key_fire_secondary=KEYMAP["fire_secondary"],
            key_on_pause=KEYMAP["pause"],
            parent_view=self,
        )

        self.pilot_overlay = PilotOverlay(self.player_area)

        self.level = Level(*mission_config)

        self.background = Background(self.level.title_image_path)

        self.section_manager.add_section(self.player_area)
        self.window.set_mouse_visible(False)

    def on_show_view(self) -> None:
        """Initialises entities"""
        # FIXME: move passthrough of bullets' lists
        # outside of starship for less propdrilling
        self.level.setup(self.player_area.starship)

    def on_hide_view(self) -> None:
        self.level = None

    def on_draw(self) -> None:
        # arc.start_render()

        self.filter.use()
        self.filter.clear()

        self.background.draw()
        self.level.draw()
        self.player_area.draw()
        if self.level.starship.can_reap():
            self.game_over.draw()
        self.pilot_overlay.draw()

        self.window.use()
        self.window.clear()
        self.filter.draw()

    def on_update(self, delta_time: float) -> None:
        """ """

        if self.on_pause:
            return

        self.background.on_update(delta_time)
        self.level.on_update(delta_time)
        self.player_area.on_update(delta_time)
        if self.level.starship.can_reap():
            self.game_over.on_update(delta_time)
            return
        self.pilot_overlay.on_update(delta_time)

        if self.level.is_finished:
            self.window.show_view(self.completion_callback_view)
