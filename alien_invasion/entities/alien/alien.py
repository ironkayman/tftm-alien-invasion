import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.loaders.alien import AlienConfig

class Alien(arc.Sprite):
    def __init__(self, config: AlienConfig):
        """Crearte instance of alien from given `config`
        """
        super().__init__()
        self.config = config
        for state in self.config.states:
            self.textures.append(arc.load_texture(
                file_name=state.texture,
                flipped_vertically=True,
                can_cache=True,
                hit_box_algorithm='Detailed',
            ))
        self.set_texture(0)
        self.set_position(CONSTANTS.CL_DISPLAY.WIDTH // 2, CONSTANTS.CL_DISPLAY.HEIGHT // 2)

    def update(self) -> None:
        """Update movement based on its self states."""
        super().update()
