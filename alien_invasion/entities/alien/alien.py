"""Alien class definition and its wrapper logic
"""

import random
from copy import deepcopy
from dataclasses import dataclass

import arcade as arc

from .mixins import OnUpdateMixin

from ..common.state_manager.state import State, AlienMoveset
from alien_invasion.entities import Starship

from alien_invasion.utils.loaders.alien import AlienConfig

from ..common.entity import Entity



@dataclass(slots=True, kw_only=True)
class Timeouts:
    """Alien object timeout to track intervals of specific functions execution dinside `on_update` method.

    Attributes
    ----------
    primary : float
        Primary weapon firing timeout.
    """

    primary: float


@dataclass(slots=True)
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

    primary: float = 0.0
    dodge: float = 0.0
    track: float = 0.0

    def reset_primary(self) -> None:
        self.primary = 0

    def reset_dodge(self) -> None:
        self.dodge = 0

    def reset_track(self) -> None:
        self.track = 0


class Alien(Entity, OnUpdateMixin):
    """Alien sprite class.

    Manages HP, states, emits hit-effects (from `hit_effect_list`).
    Created from configuration objects `AlienConfig` and
    `Particle`-like properties during its
    factory creation inside an `arc.Emitter`.
    """

    def __init__(self,
        config: AlienConfig,
        hit_effect_list: arc.SpriteList,
        starship: Starship,
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

        self._starship = starship

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
        self._spacial_danger_ranges: arc.SpriteList = self._starship.fired_shots
        self.dodging = False

        self.timeouts = Timeouts(
            primary=self.speed * self.scale**2 * 10,
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
                change_xy=arc.rand_vec_spread_deg(90, 20, 0.4),
                lifetime=random.uniform(0.4, 1.4),
                scale=0.3,
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

    def on_update(self, delta_time) -> None:
        """Particle's update method.

        Updates movement from allowed movesets by current `state`.
        """

        def update_particles_on_hit() -> None:
            """Updates health `hp`
            """
            if self.__hit_emitter:
                self.__hit_emitter.center_x = self.center_x
                self.__hit_emitter.center_y = self.center_y
            self.__hit_emitter.update()

        update_particles_on_hit()

        self._on_update_plot_movement(delta_time)

        if AlienMoveset.dodging in self.state.movesets:
            self._on_update_evade_bullets(delta_time)

        if AlienMoveset.firing in self.state.movesets:
            self._on_update_fire_bullets(delta_time)

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
        self.speed = state.speed
        self.change_y = self.speed * -0.01

    def _fire(self, delta_time: float) -> None:
        """Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        # consider shooting functionalities of Starship
        # moving inside separate class as with Transmission
        bullet = arc.Sprite(
            ":resources:images/space_shooter/laserRed01.png",
            flipped_vertically=True,
            scale=0.5 * (self.scale / 2 if self.scale > 2 else self.scale),
        )
        bullet.change_y = -self.speed * delta_time * 4

        # Position the bullet
        bullet.center_x = self.center_x
        bullet.bottom = self.bottom - 20

        # Add the bullet to the appropriate lists
        self.fired_shots.append(bullet)
