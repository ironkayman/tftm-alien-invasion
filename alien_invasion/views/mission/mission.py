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

from alien_invasion.entities.alien.bulk_logic import (
    on_update_evade_bullets,
    on_update_fire_bullets,
    on_update_plot_movement,
)
from alien_invasion.entities.common.state_manager.state import AlienMoveset


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

        self.starship = Starship(
            fired_shots=self.starship_bullets,
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

        self.is_finished = False
        self._current_onslaught_wave = None
        self._current_onslaught_wave_index = -1

    def on_show_view(self) -> None:
        """Creates and initialises first aliens' onsluaght wave"""
        self.__init_next_onslaught_wave()

    def on_hide_view(self) -> None:
        self.is_finished = False
        self._current_onslaught_wave_index = -1
        self._state_registry = {}

    def __init_next_onslaught_wave(self):
        """Cretates next OnslaughtWave based on it's spawns

        New wave is pleced to `_current_onslaught_wave` and
        increases `_current_onslaught_wave_index` by 1.
        """
        self._state_registry = {}
        if len(self._config.onslaught_waves) == self._current_onslaught_wave_index + 1:
            self.is_finished = True
            return
        self._current_onslaught_wave_index += 1
        self._current_onslaught_wave = OnslaughtWave(
            config=self._config.onslaught_waves[self._current_onslaught_wave_index],
            state_registry=self._state_registry,
            alien_bullets=self.alien_bullets,
            # self.hit_effect_particles,
        )
        self._current_onslaught_wave.setup()

    def on_update(self, delta_time: float) -> None:
        """ """
        if self.on_pause:
            return
        if self.is_finished:
            self.window.show_view(self.completion_callback_view)

        self.background.on_update(delta_time)

        self._current_onslaught_wave.on_update(delta_time)
        for alien_group in self.alien_groups:
            self.starship.xp += alien_group.last_reap_results_total_xp

        self.starship_bullets.update()
        self.alien_bullets.update()

        if self.starship.can_reap():
            self.game_over.on_update(delta_time)
        else:
            self.starship_controls.on_update(delta_time)
            self.starship.on_update(delta_time)

            self.pilot_overlay.on_update(delta_time)

        # Business logic regarding starship-alien interactions
        # ---------------

        self.__process_alien_actions(delta_time)
        self.__process_collisions_bullets_clearout()
        self.__process_out_of_bounds_alien_bullets()
        self.__process_starship_danger_proximity()

        self.__process_bounds_starship_bullets()
        self.__process_collisions_starship_damage_bullets()
        self.__process_collisions_aliens_damage_bullets()
        self.__process_collisions_aliens_starship_sprites()

        if int(self._current_onslaught_wave.timer) % 6 == 5:
            self.__check_wave_completion_requirements()

    def on_draw(self) -> None:
        self.filter.use()
        self.filter.clear()

        self.background.draw()

        self._current_onslaught_wave.draw()

        self.starship_controls.draw()
        self.starship_bullets.draw()

        if self.starship.can_reap():
            self.alien_bullets.draw()
            self.game_over.draw()
        else:
            self.starship.draw()
            # draw proximity box based on texture's original hitbox
            if self.starship.is_proximity:
                arc.draw_polygon_outline(
                    self.starship.current_position_original_hit_box,
                    arc.color.ALIZARIN_CRIMSON,
                    3 * CONSTANTS.DISPLAY.SCALE_RELATION,
                )
            # draw hitbox better
            arc.draw_circle_filled(
                self.starship.center_x,
                self.starship.center_y,
                self.starship.width // 5.3,
                arc.color.AIR_SUPERIORITY_BLUE,
                self._current_onslaught_wave.timer * 10,
                6,
            )
            self.starship.draw_hit_box(
                color=arc.color.ASH_GREY,
                line_thickness=3.5,
            )

            self.pilot_overlay.draw()

            self.alien_bullets.draw()

        self.window.use()
        self.window.clear()
        self.filter.draw()

    @property
    def alien_groups(self) -> list[list]:
        return self._current_onslaught_wave.spawners

    def __check_wave_completion_requirements(self) -> None:
        """Checks if required XP gained to proceed to a next Wave"""
        if (
            self._current_onslaught_wave.completion_requirements.score
            <= self.starship.xp
            and self._current_onslaught_wave.timer
            > self._current_onslaught_wave.completion_requirements.duration
        ):
            self.__init_next_onslaught_wave()

    def __process_collisions_bullets_clearout(self) -> None:
        """Check if starship's bullets collide with aliensm"""
        # ship's bullets can clear out aliens' bullets
        for bullet in self.starship_bullets:
            collisions = arc.check_for_collision_with_list(bullet, self.alien_bullets)
            for c in collisions:
                c.remove_from_sprite_lists()

    def __process_out_of_bounds_alien_bullets(self) -> None:
        """If alien bullets reach bottom of the viewport remove them"""
        # remove all out of window player bullets
        for bullet in self.alien_bullets:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def __process_starship_danger_proximity(self) -> None:
        """Check for enemies' proximity to starship, set it's flag"""
        self.starship.is_proximity = False
        # check bullet proximity, lower than aliens' hitboxes
        if (
            closest := arc.get_closest_sprite(self.starship, self.alien_bullets)
        ) and closest[1] < 50 * CONSTANTS.DISPLAY.SCALE_RELATION:
            self.starship.is_proximity = True
            return

        # check alien hitbox proximity, higher than bullet's proximity
        for alien_group in self.alien_groups:
            if (
                alien_group.aliens
                and (
                    closest := arc.get_closest_sprite(self.starship, alien_group.aliens)
                )
                and closest[1] < 65 * CONSTANTS.DISPLAY.SCALE_RELATION
            ):
                self.starship.is_proximity = True
                return

    def __process_bounds_starship_bullets(self) -> None:
        """Remove starship's bullets which reched top of the viewport"""
        # remove all out of window player bullets
        for bullet in filter(
            lambda bullet: bullet.bottom > CONSTANTS.DISPLAY.HEIGHT,
            self.starship_bullets,
        ):
            bullet.remove_from_sprite_lists()

    def __process_collisions_starship_damage_bullets(self) -> None:
        """Damage starship if alien bullets hit it"""
        for bullet in arc.check_for_collision_with_list(
            self.starship, self.alien_bullets
        ):
            self.starship.hp -= bullet.damage
            bullet.remove_from_sprite_lists()

    def __process_collisions_aliens_damage_bullets(self) -> None:
        """Check if starship's bullets hit aliens"""
        for alien_group in self.alien_groups:
            # detects cullet collisions
            # TODO: pass collided bulle
            #    object for bullet-specific (or ships primary weapon)
            # changes in being-hit animation
            for sbullet in self.starship_bullets:
                collisions_local = arc.check_for_collision_with_list(
                    sbullet, alien_group.aliens
                )
                if not collisions_local:
                    continue
                collisions_local[-1].hp -= sbullet.damage
                sbullet.remove_from_sprite_lists()

    def __process_collisions_aliens_starship_sprites(self) -> None:
        """Damage starship if it collides with aliens"""
        for alien_group in self.alien_groups:
            # process collisions between starship and aliens
            if collisions_alien := arc.check_for_collision_with_list(
                self.starship, alien_group.aliens
            ):
                # drain both starship's and collided alien's HP
                # TODO: perccent taken externally
                self.starship.hp -= round(self.starship.max_hp * 0.01)
                # go through each collided alien
                for alien in collisions_alien:
                    # TODO: perccent taken externally
                    alien.hp -= round(alien.hp * 0.01)

    def __process_alien_actions(self, delta_time: float) -> None:
        """Processes aliens' behavior actions like movement and firing"""
        for alien_group in self.alien_groups:
            # plot movement
            on_update_plot_movement(alien_group, self.starship, delta_time)
            for alien in alien_group:
                # evade bullets
                if AlienMoveset.dodging in alien.state.movesets:
                    on_update_evade_bullets(alien, self.starship, delta_time)
                # firing logic
                if AlienMoveset.firing in alien.state.movesets:
                    on_update_fire_bullets(alien, self.starship, delta_time)
