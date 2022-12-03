"""Module encompasses logic of starship interactions.

This includes:
- area/boundries detection
- firing
- movement
"""

from dataclasses import dataclass

import arcade as arc

from alien_invasion import CONSTANTS
# from alien_invasion.utils.loaders import starship_loader

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

        self.movement_borders = MovementArea(*area_coords)
        self.transmission = StarshipTransmission(self, self.movement_borders)

        # based on ship configuration
        self.SPEED = 10.5
        self.moving_left = False
        self.moving_right = False

        self.BULLET_SPEED = 5.5
        # recharge_timeout
        self.BULLET_COOLDOWN = self.loadout.weaponry.primary.reload_speed
        self.firing_primary = False

        self.fired_shots: arc.SpriteList = fired_shots

        self.last_update_time = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Update movement based on its self states."""
        super().update()

        def update_movement():
            """Transmission-based sprite movement updater.
            
            Since its a ViewModel all external logic is moved here
            for maximasing variables availability for interacting with
            environment and other entitties.
            
            `self.moving_left` and `self.moving_right` is set inside Section
            with `key_down` and `key_up` events.
            """
            # basic L/R movement
            if self.moving_left and not self.transmission.throttle:
                self.change_x = -self.SPEED
            if self.moving_right and not self.transmission.throttle:
                self.change_x = self.SPEED

            # slow down while approching to left border
            if self.moving_left and self.transmission.throttle:
                self.change_x = -self.SPEED // 3
                if self.left < self.movement_borders.left - self.width * 0.3:
                    self.stop()

            # slow down while approching to right border
            elif self.moving_right and self.transmission.throttle:
                self.change_x = self.SPEED // 3
                if self.right > self.movement_borders.right + self.width * 0.3:
                    self.stop()

            # calculate sprite movement state
            # and stop if its both L and R pressed
            motion = (self.moving_left, self.moving_right)
            if (all(motion) or not any(motion)):
                self.stop()

        def update_firing():
            nonlocal delta_time
            self.last_update_time += delta_time
            # firing
            if self.firing_primary and self.last_update_time > self.BULLET_COOLDOWN / 1000:
                self._fire_primary()
                self.last_update_time = 0

        # -------------------

        update_movement()
        update_firing()


    def _fire_primary(self) -> None:
        """Fire bullets guns blazing logic.
        
        Creates a bullet sets its position
        and moves it inside passed `self.fired_shots`.
        """
        # consider shooting functionalities of Starship
        # moving inside separate class as with Transmission
        bullet = arc.Sprite(":resources:images/space_shooter/laserRed01.png")
        bullet.change_y = self.BULLET_SPEED

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
            # touched left border
            all((
                self.starship.moving_left,
                self.border_reached_left
            )),
            # touched right border
            all((
                self.starship.moving_right,
                self.border_reached_right
            ))
        ))