import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.settings import KEYMAP
from .sections import (
    StarshipControls,
)
from alien_invasion.utils.crt_filters import CRTFilterDefault

from .scenes import (
    Background,
    OnslaughtWave,
    PilotOverlay,
    GameOver,
)

from alien_invasion.utils.loaders.level.model import LevelConfiguration

from alien_invasion.entities import Starship


class Mission(arc.View):
    def __init__(
        self,
        completion_callback_view: arc.View,
        mission_config: LevelConfiguration,
    ) -> None:
        """Creates entity vars

        Parameters
        ----------
        completion_callback_view : arc.View
            View to return to at level completion/exit.
        mission_config : LevelConfiguration
            Mission configuration object.
        """
        super().__init__()

        self.filter = CRTFilterDefault(self.window)
        self.on_pause = False
        self.completion_callback_view = completion_callback_view
        self.game_over = GameOver()

        self._config = mission_config

        self._state_registry = {}

        # spritelists
        self.starship_bullets = arc.SpriteList()
        self.alien_bullets = arc.SpriteList()
        self.hit_effect_particles = arc.SpriteList()

        # the player ship
        self.starship = Starship(
            fired_shots=self.starship_bullets,
            enemy_shots=self.alien_bullets,
            hit_effect_list=self.hit_effect_particles,
        )
        # move to level setup
        self.starship.center_x = CONSTANTS.DISPLAY.WIDTH // 2
        self.starship.center_y = self.starship.height

        self.starship_controls = StarshipControls(
            name="starship_controls",
            key_left=KEYMAP["player_starship_movement_left"],
            key_right=KEYMAP["player_starship_movement_right"],
            key_up=KEYMAP["player_starship_movement_up"],
            key_down=KEYMAP["player_starship_movement_down"],
            key_fire_primary=KEYMAP["confirm"],
            key_fire_secondary=KEYMAP["fire_secondary"],
            key_on_pause=KEYMAP["pause"],
            starship=self.starship,
            parent_view=self,
        )
        self.pilot_overlay = PilotOverlay(self.starship)
        self.background = Background(self._config.title_image)

        self.section_manager.add_section(self.starship_controls)

        # is mission finished
        self.is_finished = False
        self.__current_inslaught_wave = None
        self.__current_onslaught_wave_index = -1

    def on_show_view(self) -> None:
        """Initialises entities"""
        self.__init_next_onslaught_wave()

    def on_hide_view(self) -> None:
        return

    def __init_next_onslaught_wave(self):
        self.__current_onslaught_wave_index += 1
        if len(self._config.onslaught_waves) - 1 == self.__current_onslaught_wave_index:
            # self.is_finished = True
            return
        self.__current_inslaught_wave = OnslaughtWave(
            self._config.onslaught_waves[self.__current_onslaught_wave_index],
            self._state_registry,
        )
        self.__current_inslaught_wave.setup()

    def on_draw(self) -> None:
        self.filter.use()
        self.filter.clear()

        self.background.draw()
        # self.level.draw()
        self.starship_controls.draw()
        self.starship_bullets.draw()

        if self.starship.can_reap():
            return

        self.starship.draw()
        self.starship.draw_hit_box(
            color=arc.color.BLUE_BELL,
            line_thickness=1.5,
        )

        if self.starship.can_reap():
            self.game_over.draw()
        self.pilot_overlay.draw()

        self.window.use()
        self.window.clear()
        self.filter.draw()

    def on_update(self, delta_time: float) -> None:
        """ """
        if self.on_pause:
            return
        if self.is_finished:
            self.window.show_view(self.completion_callback_view)

        self.background.on_update(delta_time)
        # self.level.on_update(delta_time)
        self.starship_controls.on_update(delta_time)

        self.starship.on_update(delta_time)
        self.starship_bullets.update()
        if self.starship.can_reap():
            self.game_over.on_update(delta_time)
            return

        self.pilot_overlay.on_update(delta_time)
