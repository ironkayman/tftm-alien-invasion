"""Alien class definition.
"""

import random
import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.entities import Starship
from alien_invasion.utils.loaders.alien.config import AlienMoveset

from alien_invasion.utils.loaders.alien import AlienConfig

class Alien(arc.Sprite):
    """Alien sprite class.

    Manages HP, states, emits hit-effects (from `hit_effect_list`).
    Created from configuration objects `AlienConfig` and
    `Particle`-like properties during its
    factory creation inside an `arc.Emitter`.

    Attributes
    ----------
    __hp_old: int
        State's HP before hit, modified by `property` `.hp`.
    __hp_curr: int
        State's HP after recieveing bullet damage.

    """

    __hp_old: int
    __hp_curr: int
    __current_state_index = 0

    def __init__(self,
        config: AlienConfig,
        hit_effect_list: arc.SpriteList,
        starship: Starship,
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
        self.__starship = starship
        self.config = config
        self.hp_pools = [s.hp for s in config.states]
        for state in self.config.states:
            self.textures.append(arc.load_texture(
                file_name=state.texture,
                flipped_vertically=True,
                can_cache=True,
                hit_box_algorithm='Simple',
            ))
        # set default first state texture
        self.texture = self.textures[self.__current_state_index]

        # Particle properties
        self.center_x = center_xy[0]
        self.center_y = center_xy[1]
        self.change_x = change_xy[0]
        self.change_y = change_xy[1]
        self.angle = angle
        self.scale = scale
        self.change_angle = change_angle
        self.alpha = alpha
        self.mutation_callback = mutation_callback

        self.__hp_curr = self.hp_pools[0]
        self.__hp_old = self.__hp_curr

        # prepare monkeypatched spritelist to replace
        # emitter's service ._particles spritelist
        self.__hit_effect_list = hit_effect_list
        # create hit-particles emitter
        self.__configure_emitter()

    def __configure_emitter(self):
        """Creates emitter for particles after being hit.
        """
        self.__hit_emitter = arc.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arc.EmitBurst(0), # no particle given at spawn
            particle_factory=lambda emitter: arc.LifetimeParticle(
                filename_or_texture=":resources:images/space_shooter/meteorGrey_tiny2.png",
                change_xy=arc.rand_vec_spread_deg(90, 20, 0.4),
                lifetime=random.uniform(0.4, 1.4),
                scale=0.3,
                alpha=200
            ),
        )
        # replace internal spritelist,
        # with enabled spacial haching
        self.__hit_emitter._particles = self.__hit_effect_list

    def _restart_hit_effect_emitter(self) -> arc.Emitter:
        """Recreate particle burst

        Since this emitter emits particles by
        configuration from `.emit_controller`, recreate emitter's controller
        by defining its new value, now with non-zero amount of particles
        when we see thnat emitter completes itself (`.is_complete`).

        Returns
        -------
        arc.Emitter
            Hit-particle emitter.
        """
        if self.__hit_emitter.rate_factory.is_complete():
            self.__hit_emitter.rate_factory = arc.EmitBurst(3)
        return self.__hit_emitter

    @property
    def hp(self) -> int:
        """Getter for HP"""
        return self.__hp_curr

    @hp.setter
    def hp(self, hp_new: int) -> None:
        """Setter and manager for alien's HP considering current `state`.
        """
        self.__hp_old = self.__hp_curr
        self.__hp_curr = hp_new

        if self.__hp_curr <= 0:
            if self.state < len(self.config.states) - 1:
                self.state += 1
                self.__hp_curr = self.config.states[self.state].hp
                # since hit emitter fires only at hd difference,
                # we increase old hp when swtching to a new state,
                # to bypass new hp being pulled from a new source
                self.__hp_old = self.__hp_curr + 1

    @property
    def state(self) -> int:
        """Gets aliens's current `state`

        Its a wrapper around current texture.
        Since textures are paired with state by Alien architecture
        and multiplicity of textures is `arc.Sprite` requires a selection of one,
        consider index of selected texture as a current state index.

        Returns
        -------
        int
            Current `State` index/texture index.
        """
        return self.__current_state_index

    @state.setter
    def state(self, value: int) -> None:
        """Set current texture index/state.

        Since textures and states are almost the same
        - see getter `.state`.
        """
        self.__current_state_index = value
        self.texture = self.textures[self.__current_state_index]

    def on_update(self, delta_time) -> None:
        """Particle's update method.

        Updates movement from allowed movesets by current `state`.
        """
        if self.mutation_callback:
            self.mutation_callback(self)

        movesets = self.config.states[self.cur_texture_index].movesets

        # logic for hit-particles emitter continued updates
        if self.__hp_old > self.__hp_curr:
            self._restart_hit_effect_emitter()
            self.__hp_old = self.__hp_curr
        if self.__hit_emitter:
            self.__hit_emitter.center_x = self.center_x
            self.__hit_emitter.center_y = self.center_y
        self.__hit_emitter.update()


        # configure movement based on state's movesets
        state = self.config.states[self.__current_state_index]
        if AlienMoveset.tracking in state.movesets:
            sx = self.__starship.center_x
            if self.center_x > sx:
                self.change_x = -self.__starship.loadout.thrusters.velocity * delta_time * 0.3
            elif self.center_x < sx:
                self.change_x = self.__starship.loadout.thrusters.velocity * delta_time * 0.3

        # self.change_x, self.change_y = *arc.rand_vec_spread_deg(-90, 12, 2.0),
        super().update()

    def can_reap(self) -> bool:
        """Determine if Particle can be deleted.

        Particle-specofoc method which acts as its deletion flag.

        Deletion is allowed either:

        1. when health reaches 0
        at the lst state's healthbar;
        2. when alien leaves viewport visible space
        by going below y-axis.

        Returns
        -------
        bool
            Allow parent emitter to delete this
            particle before the next update call.
        """
        return any((
            (self.__hp_curr <= 0 and self.state == len(self.config.states) - 1),
            self.top < 0,
        ))
