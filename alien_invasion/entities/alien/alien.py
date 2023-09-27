"""Alien class definition and its wrapper logic
"""

import random

import arcade as arc
from pydantic import BaseModel

from alien_invasion import CONSTANTS
from alien_invasion.utils.loaders.alien import AlienConfig

from ..common.entity import Entity
from ..common.state_manager.state import State


class Timeouts:
    """Alien timeouts tracker

    Attributes
    ----------
    primary : float
        Primary weapon firing timeout.
    """

    def __init__(self, primary: float) -> None:
        self.primary = primary


class Timers:
    """Timers increased by `delta_times` in `on_update` submethods

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

    def __init__(
        self,
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


ALIEN_BULLET_TEXTURE = arc.load_texture(":resources:/images/pinball/bumper.png")


class Alien(Entity):
    """Alien sprite class.

    Manages HP, states, emits hit-effects (from `hit_effect_list`).
    Created from configuration objects `AlienConfig` and
    `Particle`-like properties during its
    factory creation inside an `arc.Emitter`.
    """

    BULLET_SCALE = 0.12

    def __init__(
        self,
        config: AlienConfig,
        system_name: str,
        fired_shots: arc.SpriteList,
        # hit_effects: arc.SpriteList,
        texture_registry: dict,
        movement_velocity_multiplier: tuple[float],
        **sprite_kwargs,
    ):
        """Crearte instance of alien from given `config`

        config : AlienConfig
            Main configuration properties
        system_name : str
            ID of an alien
        fired_shots : arc.SpriteList
            Shared list of all fired by all aliens bullets
        texture_registry : dict
            Shared read-only registry of each alien
            in a wave with their state textures loaded
        movement_velocity_multiplier : tuple[float]
            tuple of 2 floats:
            [0]: multiplies movement up/down
            [1]: multiplies movement left/right
        """

        super().__init__(
            config=config,
            system_name=system_name,
            fired_shots=fired_shots,
            # hit_effects=hit_effects,
            texture_registry=texture_registry,
            **sprite_kwargs,
        )

        # create hit-particles emitter
        self.__configure_emitter()
        self.dodging = False

        self.timeouts = Timeouts(
            primary=1300 * self.scale / CONSTANTS.DISPLAY.SCALE_RELATION,
        )
        self._timers = Timers()
        self._movement_velocity_multiplier = movement_velocity_multiplier
        self.change_x *= self._movement_velocity_multiplier[0]
        self.change_y *= self._movement_velocity_multiplier[1]

    def __configure_emitter(self):
        """Creates emitter for particles after being hit."""
        self.__hit_emitter = arc.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arc.EmitBurst(0),  # no particle given at spawn
            particle_factory=lambda emitter: arc.LifetimeParticle(
                filename_or_texture=":resources:images/tiles/stone.png",
                change_xy=arc.rand_vec_spread_deg(
                    90, 20, 0.4 * CONSTANTS.DISPLAY.SCALE_RELATION
                ),
                lifetime=random.uniform(0.4, 1.4),
                scale=0.05 * CONSTANTS.DISPLAY.SCALE_RELATION,
                alpha=200,
            ),
        )
        # replace internal spritelist,
        # with enabled spacial haching
        # self.__hit_emitter._particles = self.hit_effects

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
        """Updates health `hp`"""
        if self.__hit_emitter:
            wd = self.width / 3
            hd = self.height / 3
            x = self.center_x - wd
            y = self.center_y - hd
            self.__hit_emitter.center_x = x + wd * 2 * random.random()
            self.__hit_emitter.center_y = y + hd * 2 * random.random()
        self.__hit_emitter.update()

    def on_update(self, delta_time: float) -> None:
        """Particle's update method.

        Updates movement from allowed movesets by current `state`.
        """
        self.update_particles_on_hit()
        super().update()

    def draw_hit_effects(self):
        self.__hit_emitter.draw()

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
        """Applies `self.state`'s changes to the entity"""
        state: State = self.state  # type: ignore

        # Texture is extracted from the the passed
        # texture registry based on alien's name
        # and desired state
        self.texture = self._texture_registry[f"{self.system_name}.{state.name}"]

        self._hp_curr = state.hp
        self.speed = state.speed * CONSTANTS.DISPLAY.SCALE_RELATION
        self.change_y = self.speed * -0.01

    def _fire(self, delta_time: float) -> None:
        """Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        from alien_invasion.entities import Bullet

        # consider shooting functionalities of Starship
        # moving inside separate class as with Transmission
        bullet = Bullet(
            filename=None,
            damage=self.state.bullet_damage,
            scale=Alien.BULLET_SCALE,
            angle=180,
            texture=ALIEN_BULLET_TEXTURE,
        )
        # if self.state.recharge_timeout
        bullet.change_y = -1 * (self.state.bullet_speed or self.speed * 4) * delta_time

        # Position the bullet
        bullet.center_x = self.center_x
        bullet.bottom = self.bottom - 20

        # Add the bullet to the appropriate lists
        self.fired_shots.append(bullet)
