import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.loaders.alien import AlienConfig

class Alien(arc.Sprite):
    def __init__(self, config: AlienConfig, **kwargs):
        """Crearte instance of alien from given `config`
        """
        print(123, config.__dict__)
        super().__init__(**kwargs)
        self.config = config
        for state in self.config.states:
            self.textures.append(arc.load_texture(
                file_name=state.texture,
                flipped_vertically=True,
                can_cache=True,
                hit_box_algorithm='Detailed',
            ))
        self.set_texture(0)

    @property
    def state(self) -> int:
        return self.cur_texture_index

    @state.setter
    def set_state(self, value: int) -> None:
        """Set current texture index/state.

        Since textures and states are almost the same.
        """
        self.set_texture(value)

    def on_update(self, delta_time: float = 1 / 60):
        """Update movement based on its self states."""
        movesets = self.config.states[self.cur_texture_index].movesets

        super().update()


# class AlienEmitable(arc.EternalParticle):

#     def __init__(self, config: AlienConfig, particle_props: dict):
#         """Crearte instance of alien from given `config`
#         """
#         # Manual MRO resolution

#         super().__init__(
#             filename_or_texture=config.states[0].texture,
#             change_xy=particle_props['change_xy'],
#             center_xy=particle_props.get('center_xy', (0.0, 0.0)),
#             angle=particle_props.get('angle', 0),
#             change_angle=particle_props.get('change_angle', 0),
#         )

#         self.config = config
#         for state in self.config.states:
#             self.textures.append(arc.load_texture(
#                 file_name=state.texture,
#                 flipped_vertically=True,
#                 can_cache=True,
#                 hit_box_algorithm='Detailed',
#             ))
#         self.set_texture(0)



class AlienEmitable(Alien):

    def __init__(self, config: AlienConfig, particle_props: dict):
        """Crearte instance of alien from given `config`
        """
        # Manual MRO resolution
        Alien.__init__(self, config,
            center_x=particle_props.get('center_xy', (0.0)),
            center_y=particle_props.get('center_xy', (0.0)),
            angle=particle_props.get('angle', 0),
        )
        self.change_x = particle_props['change_xy'][0]
        self.change_y = particle_props['change_xy'][1]
        self.change_angle = particle_props.get('change_angle', 0)

        # TODO: put in init kwargs
        # change_xy: Vector,
        # center_xy: Point = (0.0, 0.0),
        # angle: float = 0.0,
        # change_angle: float = 0.0,
        # scale: float = 1.0,
        # alpha: int = 255,
        # mutation_callback=None

    def can_reap(self):
        return False