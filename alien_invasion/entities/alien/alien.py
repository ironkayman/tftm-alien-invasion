import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.loaders.alien import AlienConfig

class Alien(arc.Sprite):
    def __init__(self, config: AlienConfig):
        """Crearte instance of alien from given `config`
        """
        print(
            config.info, config.states
        )
        # super().__init__(img)

        # TODO: read speed from save file,
        # based on ship configuration
        # self.SPEED = 4.5

    def update(self) -> None:
        """Update movement based on its self states."""
        super().update()