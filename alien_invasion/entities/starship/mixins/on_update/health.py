"""
"""

import arcade as arc

from typing import cast

def on_update_manage_healh(
    self,
    delta_time: float,
):
    """Manage health.
    """

    # workaround circular imports
    from ...starship import Starship
    self = cast(Starship, self)

    # in main constructor: count all equiped armor,
    # create from these values total health
    collisions = arc.check_for_collision_with_list(self, self.alien_shots)
    for collision in collisions:
        self.hp -= 9
        collision.remove_from_sprite_lists()
