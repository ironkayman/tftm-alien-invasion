"""Module encompasses logic of starship interactions.

This includes:
- area/boundries detection
- firing
- movement
"""

from dataclasses import dataclass

import arcade as arc

from alien_invasion import CONSTANTS

from .constants import LastDirection
from .types import TMovementArea
from .mixins import OnUpdateMixin
from .transmission import Transmission

from alien_invasion.utils.loaders.config.starship import StarshipLoadout


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

    loadout: StarshipLoadout

    @dataclass(slots=True, kw_only=True)
    class Timeouts:
        primary: float
        secondaries: list[float]
        engine: int = 1


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
        img = CONSTANTS.DIR_IMAGES / 'player_60x48.png'
        super().__init__(img, hit_box_algorithm='Simple',)

        # workaround for cycling imports
        from alien_invasion.settings import STARSHIP
        self.loadout = STARSHIP

        self.timeouts = Starship.Timeouts(
            primary=self.loadout.weaponry.primary.recharge_timeout,
            secondaries=[tm.recharge_timeout for tm in self.loadout.weaponry.secondaries],
        )

        self.movement_borders = TMovementArea(*area_coords)
        self.transmission = Transmission(self) # <- movement_borders
        self.current_energy_capacity = self.loadout.engine.energy_cap


        self.fired_shots: arc.SpriteList = fired_shots

        self.SPEED = self.loadout.thrusters.velocity

        self.reactivated_since_free_fall = False
        self.free_fall_timer = 0

        self.alien_shots = alien_shots

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
            self.free_fall_timer += delta_time

        self._on_update_manage_health(delta_time)

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
