"""Module encompasses logic of starship interactions.

This includes:
- area/boundries detection
- firing
- movement
"""

from dataclasses import dataclass
from enum import IntEnum, auto

import arcade as arc

from alien_invasion import CONSTANTS
# from alien_invasion.utils.loaders import starship_loader

# TODO: on equipment change, specifically secondaries, recreate dataclass?
@dataclass(slots=True, kw_only=True)
class Timeouts:
    primary: float
    secondaries: list[float]
    engine: int = 1


class LastDirection(IntEnum):
    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()


@dataclass(frozen=True)
class MovementArea:
    """Params of explorable by ship area.
    
    Used to passthrough StarShip parent Section parameters
    inside which ship can move.
    """
    left: int
    right: int
    bottom: int
    height: int


class Starship(arc.Sprite):
    """ViewModel Starship entity.
    
    Input is passed through parent Section object
    in shich keybindings are being translated to movement states
    of the ship.
    
    Its is ViewModel since more logic can be accumulated inside
    designated controlled by targeted input entity/object
    possibly removing such business-logic from main Controller
    which in our case is View/Section.
    """

    def __init__(self, fired_shots: arc.SpriteList, area_coords: list):
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
        super().__init__(img)

        # workaround for cycling imports
        from alien_invasion.settings import STARSHIP
        from alien_invasion.utils.loaders.config.starship import StarshipLoadout
        self.loadout: StarshipLoadout = STARSHIP

        self.timeouts = Timeouts(
            primary=self.loadout.weaponry.primary.recharge_timeout,
            secondaries=[tm.recharge_timeout for tm in self.loadout.weaponry.secondaries],
        )

        self.movement_borders = MovementArea(*area_coords)
        self.transmission = StarshipTransmission(self, self.movement_borders)
        self.current_energy_capacity = self.loadout.engine.energy_cap

        self.moving_left = False
        self.moving_right = False
        self.last_direction = LastDirection.STATIONARY
        self.free_falling = False
        
        self.firing_primary = False

        self.fired_shots: arc.SpriteList = fired_shots

        self.SPEED = self.loadout.thrusters.velocity

        self.reactivated_since_free_fall = False
        self.free_fall_timer = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Update movement based on its self states."""
        super().update()

        def restore_energy_capacity():
            nonlocal delta_time

            if self.current_energy_capacity < self.loadout.engine.energy_cap:
                self.current_energy_capacity += self.loadout.engine.energy_restored * delta_time
                if self.loadout.engine.energy_cap < self.current_energy_capacity:
                    self.current_energy_capacity = self.loadout.engine.energy_cap

        def update_movement():
            """Transmission-based sprite movement updater.
            
            Since its a ViewModel all external logic is moved here
            for maximasing variables availability for interacting with
            environment and other entitties.
            
            `self.moving_left` and `self.moving_right` is set inside Section
            with `key_down` and `key_up` events.
            """
            nonlocal delta_time

            motion = (self.moving_left, self.moving_right)
            # calculate sprite movement state
            # and stop if its both L and R pressed
            # calculate energy loss from base
            energy_loss = self.loadout.thrusters.energy_requirement * delta_time
            # first check for energy low
            if self.transmission.low_energy:
                energy_loss = 0
            # both
            elif all(motion):
                energy_loss *= 1.3
            # single
            elif any(motion):
                energy_loss *= 1.15
            # first calculatation
            self.current_energy_capacity -= energy_loss

            # are we now out of energy?
            # if already on low energy its free fall for minimum of 2sec
            # but if since free falling (last True value)
            # theres positive amount of energy but were
            # no movement since positivity
            # continue free falling
            # moving will disrupt free falling state
            # when at a timer more than 2sec passed of free fall
            self.free_falling = (
                (
                    0 < self.free_fall_timer < 2
                    or self.transmission.low_energy
                ) or (
                    self.free_falling and
                    not self.transmission.low_energy and
                    not any(motion)
                )
            )

            # standart movement behavior
            if not self.free_falling:
                self.free_fall_timer = 0
                # last movement direction for cahnge of outage
                # this caises to free fall in that direction
                if self.moving_left:
                    self.last_direction = LastDirection.LEFT
                if self.moving_right:
                    self.last_direction = LastDirection.RIGHT
                if all(motion) or not any(motion):
                    self.last_direction = LastDirection.STATIONARY

                # basic L/R movement
                if self.moving_left and not self.transmission.throttle:
                    self.change_x = -self.SPEED
                if self.moving_right and not self.transmission.throttle:
                    self.change_x = self.SPEED

                # slow down while approching to left border
                if self.moving_left and self.transmission.throttle and self.transmission.border_reached_left:
                    self.change_x = -self.SPEED // 3
                    # stop inside a wall
                    if self.left < self.movement_borders.left - self.width * 0.3:
                        self.stop()
                # slow down while approching to right border
                elif self.moving_right and self.transmission.throttle and self.transmission.border_reached_right:
                    self.change_x = self.SPEED // 3
                    # stop inside a wall
                    if self.right > self.movement_borders.right + self.width * 0.3:
                        self.stop()

                # stop at no movement or both L and R
                if not self.transmission.throttle:
                    if (all(motion) or not any(motion)):
                        self.stop()
                # exit
                return

            self.free_fall_timer += delta_time

            # last L/R movement at low energy -> free fall
            if self.last_direction == LastDirection.LEFT:
                self.change_x = -self.SPEED // 3
                # stop inside a wall if deep inside it
                if self.left < self.movement_borders.left - self.width * 0.3:
                    self.stop()
                # reverse reaching wall without slowing down
                elif self.transmission.border_reached_left:
                    self.last_direction = LastDirection.RIGHT
            elif self.last_direction == LastDirection.RIGHT:
                self.change_x = self.SPEED // 3
                # stop inside a wall if deep inside it
                if self.right > self.movement_borders.right + self.width * 0.3:
                    self.stop()
                # reverse reaching wall without slowing down
                elif self.transmission.border_reached_right:
                    self.last_direction = LastDirection.LEFT

        def update_firing():
            nonlocal delta_time

            full_motion = all((self.moving_left, self.moving_right))
            self.loadout.weaponry.primary._timer += delta_time
            # correcteed timeout:
            # it behaves as usual until ship is in static full thruster motion,
            # then timeout is cut to 2/3,
            # while being hicher than 30% of energy capacity
            timeout_corrected = (
                self.timeouts.primary * 0.66 if
                full_motion and ((self.current_energy_capacity / self.loadout.engine.energy_cap) * 100) >= 30
                else self.timeouts.primary
            )
            # firing
            if (
                self.firing_primary and
                self.loadout.weaponry.primary._timer > timeout_corrected / 1000
                and not self.transmission.low_energy
            ):
                self._fire_primary()
                self.current_energy_capacity -= self.loadout.weaponry.primary.energy_per_bullet
                self.loadout.weaponry.primary._timer = 0

        # -------------------

        restore_energy_capacity()
        update_movement()
        update_firing()

        print(f'{self.current_energy_capacity:.2f}/{self.loadout.engine.energy_cap}')


    def _fire_primary(self) -> None:
        """Fire bullets guns blazing logic.
        
        Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        # consider shooting functionalities of Starship
        # moving inside separate class as with Transmission
        bullet = arc.Sprite(":resources:images/space_shooter/laserRed01.png")
        bullet.change_y = self.loadout.weaponry.primary.speed

        # Position the bullet
        bullet.center_x = self.center_x
        bullet.bottom = self.top - 20

        # Add the bullet to the appropriate lists
        self.fired_shots.append(bullet)


class StarshipTransmission:
    """Thransmission and surroundings reactive movement manager."""
    def __init__(self, starship: Starship, area: MovementArea) -> None:
        self.starship = starship
        self.area = area

    @property
    def low_energy(self) -> bool:
        return self.starship.current_energy_capacity <= 0

    @property
    def border_reached_left(self) -> bool:
        """Check if ship touches left border."""
        return self.starship.left < self.area.left

    @property
    def border_reached_right(self) -> bool:
        """Check if ship touches right border."""
        return self.starship.right > self.area.right

    @property
    def throttle(self) -> bool:
        """Throttler manages movement and considers surroundings.

        If anything in block `any` if successful do throttle.
        This logic ties to `movement_update` functions of `StarShip` class
        where transmission calculates and takes
        in an account current ship movement states.
        """
        return any((
            # no energy
            all((
                self.low_energy,
                self.starship.moving_left or self.starship.moving_right,
            )),
            # touched left border
            all((
                self.starship.moving_left,
                self.border_reached_left
            )),
            # touched right border
            all((
                self.starship.moving_right,
                self.border_reached_right
            )),
        ))