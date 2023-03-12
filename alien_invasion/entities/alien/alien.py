import random
from copy import deepcopy
import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.loaders.alien import AlienConfig

class Alien(arc.Sprite):

    __hp_old: int = 0
    __hp_curr: int = 0

    def __init__(self,
        config: AlienConfig,
        # Particle-oriented properties
        change_xy: arc.Vector = (0.0, 0.0),
        center_xy: arc.Point = (0.0, 0.0),
        angle: float = 0.0,
        change_angle: float = 0.0,
        scale: float = 1.0,
        alpha: int = 255,
        mutation_callback=None,
    ):
        """Crearte instance of alien from given `config`
        """
        super().__init__()
        self.config = config
        self.hp_pools = [s.hp for s in config.states]
        for state in self.config.states:
            self.textures.append(arc.load_texture(
                file_name=state.texture,
                flipped_vertically=True,
                can_cache=True,
                hit_box_algorithm='Simple',
            ))
        self.set_texture(0)

        self.center_x = center_xy[0]
        self.center_y = center_xy[1]
        self.change_x = change_xy[0]
        self.change_y = change_xy[1]
        self.angle = angle
        self.change_angle = change_angle
        self.alpha = alpha
        self.mutation_callback = mutation_callback

        self.__hit_emitter = arc.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arc.EmitBurst(5),
            particle_factory=lambda emitter: arc.LifetimeParticle(
                filename_or_texture=":resources:images/pinball/pool_cue_ball.png",
                change_xy=arc.rand_in_circle((0.0, 0.0), 2.0),
                lifetime=random.uniform(1.0 - 1.0, 1.0),
                scale=1.0,
                alpha=32
            )
        )

    @property
    def hp(self) -> int:
        self.__hp_curr = self.hp_pools[self.state]
        return self.__hp_curr

    @hp.setter
    def hp(self, hp_new: int) -> None:
        hp_old = self.hp_pools[self.state]
        self.hp_pools[self.state] = hp_new

        self.__hp_old = hp_old
        self.__hp_curr = hp_new

        if hp_new <= 0:
            if self.state < len(self.config.states) - 1:
                self.state += 1
            else:
                self.kill()

    @property
    def state(self) -> int:
        return self.cur_texture_index

    @state.setter
    def set_state(self, value: int) -> None:
        """Set current texture index/state.

        Since textures and states are almost the same.
        """
        self.set_texture(value)

    def update(self) -> None:
        """Update movement based on its self states."""
        if self.mutation_callback:
            self.mutation_callback(self)

        movesets = self.config.states[self.cur_texture_index].movesets

        if self.__hp_old > self.__hp_curr:
            # print(self.__hp_old, self.__hp_curr)
            self.__hp_old = self.__hp_curr

            self.__hit_emitter.center_x = self.center_x
            self.__hit_emitter.center_y = self.center_y

            self.__hit_emitter.update()
            # self.__hit_emitter.draw()

        super().update()


    def can_reap(self) -> bool:
        """Determine if Particle can be deleted"""
        return False
