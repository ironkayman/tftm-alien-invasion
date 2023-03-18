from typing import cast
from random import random

import arcade as arc

from alien_invasion.utils.loaders.alien.config import AlienMoveset


def on_update_evade_bullets(self, delta_time) -> None:

    # workaround circular imports
    from ...alien import Alien
    self = cast(Alien, self)

    self._spacial_danger_ranges = self._starship.fired_shots

    # configure movement based on state's movesets
    movesets = self.config.states[self.state].movesets

    cl = arc.get_closest_sprite(self, self._spacial_danger_ranges)
    if not cl:
        # set default
        cl = [0, 600] # 600px
    for b in self._spacial_danger_ranges:
        if (isect := set(range(round(self.left - self.width * 0.4), round(self.right + self.width * 0.4))).intersection(range(round(b.left), round(b.right)))):
            self.change_x = self.SPEED * delta_time
            # if aggressive moveset present and dodge is active
            # stop dodging by chance not in favour of time past dodging
            if AlienMoveset.tracking in movesets and self.dodging:
                if random() < self._timer_dodge * 0.1 * cl[1]:
                    self.dodging = False
                    break
            self.dodging = True
            # try to fofge the bullet by changing direction
            # the bullet passed more of left side -> dodge to the right
            if (self.center_x - b.center_x) < 0:
                self.change_x *= -1
        else:
            self.dodging = False
            self._timer_dodge = 0
    # dodge timer reset proportianally to proximity to a bullet
    if self.dodging and self._timer_dodge > cl[1] / 800:
        self._timer_dodge = 0
        self.dodging = False
