from dataclasses import dataclass

import arcade as arc

from alien_invasion import CONSTANTS
# from alien_invasion.utils.loaders import starship_loader

@dataclass(frozen=True)
class MovementArea:
    """Params of explorable by ship area."""
    left: int
    right: int
    bottom: int
    height: int


class Starship(arc.Sprite):
    def __init__(self, fired_shots: arc.SpriteList, area_coords: list):
        img = CONSTANTS.DIR_IMAGES / 'player_60x48.png'
        super().__init__(img)

        self.movement_borders = MovementArea(*area_coords)
        self.transmission = StarshipTransmission(self, self.movement_borders)

        # TODO: read speed from save file,
        # based on ship configuration
        self.SPEED = 10.5
        self.moving_left = False
        self.moving_right = False

        self.BULLET_SPEED = 5.5
        self.BULLET_COOLDOWN = 1
        self.firing_primary = False

        self.fired_shots: arc.SpriteList = fired_shots


    def update(self) -> None:
        """Update movement based on its self states."""
        super().update()

        def update_movement():
            # movement
            if self.moving_left and not self.transmission.throttle:
                self.change_x = -self.SPEED
            if self.moving_right and not self.transmission.throttle:
                self.change_x = self.SPEED

            # slow down while approching to left border
            if self.moving_left and self.transmission.throttle:
                self.change_x = -self.SPEED // 3
                if self.left < self.movement_borders.left - self.width * 0.3:
                    self.change_x = 0

            # slow down while approching to right border
            elif self.moving_right and self.transmission.throttle:
                self.change_x = self.SPEED // 3
                if self.right > self.movement_borders.right + self.width * 0.3:
                    self.change_x = 0

            motion = (self.moving_left, self.moving_right)
            if (all(motion) or not any(motion)):
                self.stop()

        def update_firing():
            # firing
            if self.firing_primary:
                self._fire_primary()

        # -------------------

        update_movement()
        update_firing()


    def _fire_primary(self) -> None:
        # if not self.firing_primary: return
        # Create a bullet
        # TODO: check primary weapon type
        bullet = arc.Sprite(":resources:images/space_shooter/laserRed01.png")
        # bullet.color = PLAYER_COLOR

        # Give the bullet a speed
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
        """Chack if ship touches left border."""
        return self.starship.left < self.area.left

    @property
    def border_reached_right(self) -> bool:
        """Check if ship touches right border."""
        return self.starship.right > self.area.right

    @property
    def throttle(self) -> bool:
        """Throttler manages movememnt considering surroundings"""

        if any((
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
        )):
            return True

        # dont throttle
        return False