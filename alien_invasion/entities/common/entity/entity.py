"""Alien class definition and its wrapper logic
"""
from abc import ABC
from copy import deepcopy

import arcade as arc

from alien_invasion import CONSTANTS

from ..state_manager import StateManager
from ..state_manager.state import State


class Timeouts(ABC):
    """Interval tracker for `on_update` submethods

    Attributes
    ----------
    primary : float
        Primary weapon firing timeout.
    """

    pass


class Timers(ABC):
    """Timers increased by `delta_time` in `on_update` method

    Attributes
    ----------
    """

    pass


class Entity(arc.Sprite, ABC):
    """Alien sprite class.

    Manages HP, states, emits hit-effects (from `hit_effect_list`).
    Created from configuration objects `AlienConfig` and
    `Particle`-like properties during its
    factory creation inside an `arc.Emitter`.
    """

    _hp_curr: int
    _hp_old: int
    state: State
    _can_reap: bool = False

    timeouts: Timeouts
    _timers: Timers

    def __init__(
        self,
        config,
        system_name: str,
        fired_shots: arc.SpriteList,
        hit_effects: arc.SpriteList,
        texture_registry: dict,
        # Particle-oriented properties
        change_xy: arc.Vector = (0.0, 0.0),
        center_xy: arc.Point = (0.0, 0.0),
        angle: float = 0.0,
        change_angle: float = 0.0,
        scale: float = 1.0,
        alpha: int = 255,
        mutation_callback=None,
    ):
        """Crearte instance of alien from given `config`"""
        # self._hp_curr: int
        # self._hp_old: int
        # self.state: State
        self._can_reap: bool = False
        # self.speed: int

        super().__init__(
            center_x=center_xy[0],
            center_y=center_xy[1],
            angle=angle,
            scale=scale * CONSTANTS.DISPLAY.SCALE_RELATION,
            hit_box_algorithm="Detailed",
        )
        self.change_x=change_xy[0]

        self.change_angle = change_angle
        self.alpha = alpha
        
        self.config = config
        self._texture_registry = texture_registry
        self.system_name = system_name

        self.states = deepcopy(self.config.states)

        self.state, _ = next(self.states)
        self.apply_state()

        self.hit_effect_list = hit_effects
        self.fired_shots = fired_shots

    def _restart_hit_effect_emitter(self) -> None:
        """Method for restarting emitter animation"""
        raise NotImplementedError

    @property
    def hp(self) -> int:
        """Getter for HP"""
        return self._hp_curr

    @hp.setter
    def hp(self, hp_new: int) -> None:
        """Setter and manager for alien's HP considering current `state`."""
        self._restart_hit_effect_emitter()
        if hp_new > 0:
            self._hp_old = self._hp_curr
            self._hp_curr = hp_new
            return

        self.state, error = next(self.states)
        # death_damage_cap = self.state.death_damage_cap
        if error is StateManager.FinalStateReached:
            self.handle_final_state()
        else:
            self._hp_old = self._hp_curr
        self.apply_state()

    def handle_final_state(self) -> None:
        """
        Should impliment logic for `_can_reap = True`
        """
        raise NotImplementedError

    def on_update(self, delta_time) -> None:
        """Particle's update method.

        Updates movement from allowed movesets by current `state`.
        """
        raise NotImplementedError

    def can_reap(self) -> bool:
        """Determine if Particle can be deleted

        Particle-specifoc method which acts as its deletion flag.
        See `_can_reap : bool`.

        Returns
        -------
        bool
            Allow parent emitter to delete this
            particle before the next update call.
        """
        raise NotImplementedError

    def apply_state(self) -> None:
        raise NotImplementedError

    def _fire(self, delta_time: float) -> None:
        """Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        raise NotImplementedError
