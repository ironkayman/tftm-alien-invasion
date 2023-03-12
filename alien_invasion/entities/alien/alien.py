import random
from copy import deepcopy
import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.utils.loaders.alien import AlienConfig

class Alien(arc.Sprite):

    __hp_old: int|None = None
    __hp_curr: int|None = None

    def __init__(self,
        config: AlienConfig,
        hit_effect_list: arc.SpriteList,
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

        self.__hp_curr = self.hp_pools[0]
        self.__hp_old = self.__hp_curr

        self.__hit_effect_list = hit_effect_list
        self.__configure_emitter()

    def __configure_emitter(self):
        self.__hit_emitter = arc.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arc.EmitBurst(0), # no particle given at spawn
            particle_factory=lambda emitter: arc.LifetimeParticle(
                filename_or_texture=":resources:images/space_shooter/meteorGrey_tiny2.png",
                # center_xy=(self.center_x, self.center_y),
                change_xy=arc.rand_vec_spread_deg(90, 20, 0.2),
                lifetime=random.uniform(1.0, 3.0),
                scale=0.3,
                alpha=200
            ),
        )
        self.__hit_emitter._particles = self.__hit_effect_list

    def _restart_hit_effect_emitter(self) -> arc.Emitter:
        if self.__hit_emitter.rate_factory.is_complete():
            self.__hit_emitter.rate_factory = arc.EmitBurst(3)
        return self.__hit_emitter

    @property
    def hp(self) -> int:
        return self.__hp_curr

    @hp.setter
    def hp(self, hp_new: int) -> None:
        self.__hp_old = self.__hp_curr
        self.__hp_curr = hp_new

        if hp_new <= 0:
            if self.state < len(self.config.states) - 1:
                self.state += 1
                hp_new = self.config.states[self.state].hp

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
            self._restart_hit_effect_emitter()
            self.__hp_old = self.__hp_curr
        if self.__hit_emitter:
            self.__hit_emitter.center_x = self.center_x
            self.__hit_emitter.center_y = self.center_y
            self.__hit_emitter.update()
        if self.__hit_emitter.get_count():
            print(self.__hit_emitter.get_count(), end=': ')
            print(self.__hit_emitter._particles[-1].change_x, self.__hit_emitter._particles[-1].change_y)
        super().update()


    def can_reap(self) -> bool:
        """Determine if Particle can be deleted"""
        return any((
            (self.__hp_curr <= 0 and self.state == len(self.config.states) - 1),
            self.top < 0,
        ))
