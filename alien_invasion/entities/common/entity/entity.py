"""Alien class definition and its wrapper logic
"""
from abc import ABC
from copy import deepcopy
from dataclasses import dataclass

import arcade as arc

from ..state_manager import StateManager
from ..state_manager.state import State


@dataclass(slots=True, kw_only=True)
class Timeouts(ABC):
    """Alien object timeout to track intervals of specific functions execution dinside `on_update` method.

    Attributes
    ----------
    primary : float
        Primary weapon firing timeout.
    """
    pass

@dataclass(slots=True)
class Timers(ABC):
    """Alien object timers increased by `delta_times` in `on_update` methods

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


    def __init__(self,
        config,
        parent_sprite_list: arc.SpriteList,
        origin_bullets: arc.SpriteList,
        enemy_bullets: arc.SpriteList,
        hit_effects: arc.SpriteList,
        # Particle-oriented properties
        change_xy: arc.Vector = (0.0, 0.0),
        center_xy: arc.Point = (0.0, 0.0),
        angle: float = 0.0,
        change_angle: float = 0.0,
        scale: float = 1.0,
        alpha: int = 255,
        mutation_callback=None,
    ):
        """Crearte instance of alien from given `config`
        """
        # self._hp_curr: int
        # self._hp_old: int
        # self.state: State
        self._can_reap: bool = False
        # self.SPEED: int

        super().__init__()
        self._parent_list = parent_sprite_list

        # Particle properties
        self.center_x = center_xy[0]
        self.center_y = center_xy[1]
        self.change_x = change_xy[0]
        # self.change_y = self.SPEED * -0.01
        self.angle = angle
        self.scale = scale
        self.change_angle = change_angle
        self.alpha = alpha
        self.mutation_callback = mutation_callback

        self.config = config

        self.states = deepcopy(self.config.states)
        self.state, _ = next(self.states)
        self.apply_state()

        self.hit_effect_list = hit_effects
        self.fired_shots = origin_bullets
        self.enemy_shots = enemy_bullets


    @property
    def hp(self) -> int:
        """Getter for HP"""
        return self._hp_curr

    @hp.setter
    def hp(self, hp_new: int) -> None:
        """Setter and manager for alien's HP considering current `state`.
        """
        # self._restart_hit_effect_emitter()
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