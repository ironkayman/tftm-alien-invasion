"""Module encompasses logic of starship interactions.

This includes:
- area/boundries detection
- firing
- movement
"""

from dataclasses import dataclass
from random import random

import arcade as arc

from alien_invasion import CONSTANTS

from .constants import LastDirection
from .types import TMovementArea
from .mixins import OnUpdateMixin
from .transmission import Transmission

from ..common.state_manager import StateManager


class Starship(arc.Sprite, OnUpdateMixin):
    """ViewModel Starship entity.
    
    Input is passed through parent Section object
    in shich keybindings are being translated to movement states
    of the ship.
    
    Its is ViewModel since more logic can be accumulated inside
    designated controlled by targeted input entity/object
    possibly removing such business-logic from main Controller
    which in our case is View/Section.
    """

    moving_left = False
    moving_right = False
    last_direction = LastDirection.STATIONARY
    free_falling = False

    firing_primary = False


    _hp_curr: int
    _hp_old: int
    _current_state_index = 0
    _can_reap: bool = False

    @dataclass(slots=True, kw_only=True)
    class Timeouts:
        primary: float
        secondaries: list[float]
        engine: int = 1

    @dataclass(slots=True)
    class Timers:
        """Alien object timers increased by `delta_times` in `on_update` methods

        Attributes
        ----------
        primary : float
            Timer for primary weapon.
        evade : float
            Time elapsed during execution of last move during dodging.
        outage : float
            Time spent in outage mode before any interaction.
        """

        primary: float = 0.0
        evade: float = 0.0
        outage: float = 0.0

        def reset_primary(self) -> None:
            self.primary = 0

        def reset_evade(self) -> None:
            self.evade = 0

        def reset_outage(self) -> None:
            self.outage = 0


    def __init__(self, fired_shots: arc.SpriteList, area_coords: list, alien_shots: arc.SpriteList,):
        """Creates Starship instance.

        Parameters
        ----------
        fired_shots: arc.SpriteList
            List of currently registered bullets
        area_coords:list
            Description of an area at which
            ship is allowed to move.
        """
        super().__init__()

        # workaround for cycling imports
        from alien_invasion.settings import STARSHIP
        self.loadout = STARSHIP

        self._timers = Starship.Timers()

        self.states = StateManager([
            {'initial':
                dict(
                    texture_path=CONSTANTS.DIR_IMAGES / 'initial_starship.png',
                    name='initial',
                    index=0,
                    data=dict(
                        hp=sum([item.armor for item in self.loadout.hull.armor]),
                        movesets=[],
                        speed=self.loadout.thrusters.velocity,
                        death_damage_cap=True,
                    )
                ),
            },
            {'deaths_door': dict(
                    texture_path=CONSTANTS.DIR_IMAGES / 'initial_starship.danger.png',
                    name='deaths_door',
                    index=1,
                    data=dict(
                        movesets=[],
                        speed=self.loadout.thrusters.velocity,
                        hp=1,
                        death_damage_cap=True,
                    )
                )
            },
        ])
        self.state, _ = next(self.states)
        self.apply_state()

        self.timeouts = Starship.Timeouts(
            primary=self.loadout.weaponry.primary.recharge_timeout,
            secondaries=[tm.recharge_timeout for tm in self.loadout.weaponry.secondaries],
        )

        self.movement_borders = TMovementArea(*area_coords)
        self.transmission = Transmission(self)
        self.current_energy_capacity = self.loadout.engine.energy_cap

        self.fired_shots: arc.SpriteList = fired_shots

        # self.reactivated_since_free_fall = False

        self.alien_shots = alien_shots
        self.set_hit_box(
            (
                (-2, 5),
                (2, 5),
                (5, 0),
                (2, -5),
                (-2, -5),
                (-5, 0),
            )
        )

    def apply_state(self) -> None:
        state = self.state
        self.texture = arc.load_texture(
            file_name=state.texture_path,
            can_cache=True,
        )
        self._hp_curr = state.hp
        self.SPEED = state.speed

    def on_update(self, delta_time: float = 1 / 60):
        """Update movement based on its self states."""

        frame_energy_change: float = 0.0
        # including free fall mode conditions
        self._on_update_energy_capacity(delta_time, frame_energy_change)
        # update ship systems considering current energy level
        self._on_update_movement(delta_time)
        self._on_update_firing(delta_time, frame_energy_change)
        # update free-fall timer
        if self.free_falling:
            self._timers.outage += delta_time

        # print(f"{self.current_energy_capacity:.1f}/{self.loadout.engine.energy_cap} | lost: {'++' if frame_energy_change > 0 else '-'}{frame_energy_change:.1f}eu")
        super().update()

    def _fire_primary(self, delta_time: float) -> None:
        """Fire bullets guns blazing logic.

        Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        # consider shooting functionalities of Starship
        # moving inside separate class as with Transmission
        bullet = arc.Sprite(":resources:images/space_shooter/laserRed01.png")
        bullet.change_y = self.loadout.weaponry.primary.speed * delta_time

        # Position the bullet
        bullet.center_x = self.center_x
        bullet.bottom = self.top - 20

        # Add the bullet to the appropriate lists
        self.fired_shots.append(bullet)


    @property
    def hp(self) -> int:
        """Getter for HP"""
        return self._hp_curr

    @hp.setter
    def hp(self, hp_new: int) -> None:
        """Setter and manager for alien's HP considering current `state`.
        """

        breakpoint()
        if self._hp_curr - hp_new > 0:
            self._hp_old = self._hp_curr
            self._hp_curr = hp_new
            return

        self.state, error = next(self.states)
        # death_damage_cap = self.state.death_damage_cap
        if error is not StateManager.FinalStateReached:
            if (chance := random()) > 0.22:
                self._hp_old = self._hp_curr
                self._hp_curr = self.state.hp
            else:
                self._can_reap = True
        else:
            self._hp_old = self._hp_curr
            self.apply_state()

    def can_reap(self) -> bool:
        return self._can_reap
