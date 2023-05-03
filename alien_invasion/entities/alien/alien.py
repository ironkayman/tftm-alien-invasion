"""Alien class definition and its wrapper logic
"""

import random
from pydantic import BaseModel

from pydantic import BaseModel

import arcade as arc

from alien_invasion import CONSTANTS

from ..common.state_manager.state import State, AlienMoveset

from alien_invasion.utils.loaders.alien import AlienConfig

from ..common.entity import Entity


class Timeouts:
    """Alien object timeout to track intervals of specific functions execution dinside `on_update` method.

    Attributes
    ----------
    primary : float
        Primary weapon firing timeout.
    """

    def __init__(self, primary: float) -> None:
        self.primary = primary


class Timers:
    """Alien object timers increased by `delta_times` in `on_update` methods

    Attributes
    ----------
    primary : float
        Timer for primary weapon.
    dodge : float
        Time elapsed during execution of last move during dodging.
    track : float
        Timer couting the time passed after
        last movement change in during tracking moveset.
    """

    def __init__(self,
        primary: float = 0.0,
        dodge: float = 0.0,
        track: float = 0.0,
    ) -> None:
        self.primary = primary
        self.dodge = dodge
        self.track = track

    def reset_primary(self) -> None:
        self.primary = 0.0

    def reset_dodge(self) -> None:
        self.dodge = 0.0

    def reset_track(self) -> None:
        self.track = 0.0


class Overrides(BaseModel):
    should_persue: bool


class Alien(Entity):
    """Alien sprite class.

    Manages HP, states, emits hit-effects (from `hit_effect_list`).
    Created from configuration objects `AlienConfig` and
    `Particle`-like properties during its
    factory creation inside an `arc.Emitter`.
    """

    def __init__(self,
        config: AlienConfig,
        overrides: dict,
        approach_velocity_multiplier: float,
        hit_effect_list: arc.SpriteList,
        alien_bullets: arc.SpriteList,
        parent_sprite_list: arc.SpriteList,
        # Particle-oriented properties
        **particle_kwargs
    ):
        """Crearte instance of alien from given `config`
        """
        # self._can_reap: bool = False

        # super().__init__()
        # self._aliens = parent_sprite_list

        self._approach_velocity_multiplier = approach_velocity_multiplier

        self._overrides = Overrides.parse_obj(overrides)

        particle_kwargs['scale'] *= CONSTANTS.DISPLAY.SCALE_RELATION

        super().__init__(
            config=config,
            parent_sprite_list=parent_sprite_list,
            fired_shots=alien_bullets,
            enemy_shots=[],
            hit_effects=hit_effect_list,
            **particle_kwargs,
        )

        # create hit-particles emitter
        self.__configure_emitter()
        self.dodging = False

        self.timeouts = Timeouts(
            primary=700 * self.scale / CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        self._timers = Timers()


    def __configure_emitter(self):
        """Creates emitter for particles after being hit.
        """
        self.__hit_emitter = arc.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arc.EmitBurst(0), # no particle given at spawn
            particle_factory=lambda emitter: arc.LifetimeParticle(
                filename_or_texture=":resources:images/space_shooter/meteorGrey_tiny2.png",
                change_xy=arc.rand_vec_spread_deg(90, 20, 0.4 * CONSTANTS.DISPLAY.SCALE_RELATION),
                lifetime=random.uniform(0.4, 1.4),
                scale=0.3 * CONSTANTS.DISPLAY.SCALE_RELATION,
                alpha=200
            ),
        )
        # replace internal spritelist,
        # with enabled spacial haching
        self.__hit_emitter._particles = self.hit_effect_list

    def _restart_hit_effect_emitter(self) -> arc.Emitter:
        """Recreate particle burst

        Since this emitter emits particles by
        configuration from `.emit_controller`, recreate emitter's controller
        by defining its new value, now with non-zero amount of particles
        when we see thnat emitter completes itself (`.is_complete`).

        Returns
        -------
        arc.Emitter
            Hit-particle emitter.
        """
        if self.__hit_emitter.rate_factory.is_complete():
            self.__hit_emitter.rate_factory = arc.EmitBurst(3)
        return self.__hit_emitter

    def handle_final_state(self) -> None:
        """When alien reaches it's final state - simply remove it"""
        self._can_reap = True


    def update_particles_on_hit(self) -> None:
        """Updates health `hp`
        """
        if self.__hit_emitter:
            self.__hit_emitter.center_x = self.center_x
            self.__hit_emitter.center_y = self.center_y
        self.__hit_emitter.update()

    def on_update(self, delta_time: float) -> None:
        """Particle's update method.

        Updates movement from allowed movesets by current `state`.
        """
        self.update_particles_on_hit()
        super().update()

    def can_reap(self) -> bool:
        """Determine if Particle can be deleted.

        Particle-specofoc method which acts as its deletion flag.

        Deletion is allowed either:

        1. when health reaches 0
        at the lst state's healthbar;
        2. when alien leaves viewport visible space
        by going below y-axis.

        Returns
        -------
        bool
            Allow parent emitter to delete this
            particle before the next update call.
        """
        return self._can_reap or self.top < 0

    def apply_state(self) -> None:
        """Applies `self.state`'s changes to the entity
        """
        state: State = self.state  # type: ignore
        self.texture = arc.load_texture(
            file_name=state.texture_path,
            flipped_vertically=True,
            can_cache=True,
            hit_box_algorithm='Simple',
        )
        self._hp_curr = state.hp
        self.speed = state.speed * CONSTANTS.DISPLAY.SCALE_RELATION
        self.change_y = self.speed * -0.01 * self._approach_velocity_multiplier

    def _fire(self, delta_time: float) -> None:
        """Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        # consider shooting functionalities of Starship
        # moving inside separate class as with Transmission
        bullet = arc.Sprite(
            ":resources:images/space_shooter/laserRed01.png",
            flipped_vertically=True,
            scale=0.5 * (self.scale / 2 if self.scale > 2 else self.scale) * CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        bullet.change_y = -1 * self.speed * 4 * delta_time

        # Position the bullet
        bullet.center_x = self.center_x
        bullet.bottom = self.bottom - 20

        # Add the bullet to the appropriate lists
        self.fired_shots.append(bullet)
