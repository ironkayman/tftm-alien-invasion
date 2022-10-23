import arcade as arc

from alien_invasion import CONSTANTS

class Alien(arc.Sprite):
    def __init__(self, *args, **kwargs):
        img = CONSTANTS.DIR_IMAGES / 'player_60x48.png'
        super().__init__(img, *args, **kwargs)

        # TODO: read speed from save file,
        # based on ship configuration
        # self.SPEED = 4.5

    def update(self) -> None:
        """Update movement based on its self states."""
        super().update()