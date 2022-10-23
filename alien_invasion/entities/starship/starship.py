import arcade as arc

from alien_invasion import CONSTANTS
# from alien_invasion.utils.loaders import starship_loader

class Starship(arc.Sprite):
    def __init__(self, fired_shots: arc.SpriteList,):
        img = CONSTANTS.DIR_IMAGES / 'player_60x48.png'
        super().__init__(img)

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

        # essential functions
        # movement
        if self.moving_left:
            self.change_x = -self.SPEED
        if self.moving_right:
            self.change_x = self.SPEED
        # firing
        if self.firing_primary:
            self._fire_primary()

        # movement: consider both keys pressed
        motion = (self.moving_left, self.moving_right)
        if all(motion) or not any(motion):
            self.stop()

    def _fire_primary(self) -> arc.Sprite:
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
