import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.entities import Starship


class PlayerArea(arc.Section, arc.Scene):
    """Player ship area of movement.

    Handles and coordinates sprite lists
    contenets of which originated by player:

    - player's ship sprite `.ship`
    - player's ship sprite group
        of single ship sprite `.player`

    Ship can be moved left or right or shot;
    these events are handled in `on_key_press` / `on_key_release`
    """

    def __init__(
        self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        key_left: int,
        key_right: int,
        key_up: int,
        key_down: int,
        key_fire_primary: int,
        key_fire_secondary: int,
        key_on_pause: int,
        parent_view: arc.View,
        **kwargs
    ) -> None:
        """Area of a view in which ship is placed"""
        # Manual MRO resolution
        arc.Section.__init__(
            self,
            left,
            bottom,
            width,
            height,
            accept_keyboard_events={
                key_left,
                key_right,
                key_up,
                key_down,
                key_fire_primary,
                key_fire_secondary,
                key_on_pause,
            },
            **kwargs
        )
        arc.Scene.__init__(self)

        self._parent_view = parent_view
        self.on_pause = self._parent_view.on_pause

        # keys assigned to move the paddle
        self.key_left: int = key_left
        self.key_right: int = key_right
        self.key_up: int = key_up
        self.key_down: int = key_down
        # if movement if l/r, and white both pressed any
        # other key on arrowpad wont be registered
        # also up, left wont register righ, right up  wond register left
        self.key_fire_primary: int = key_fire_primary
        self.key_fire_secondary: int = key_fire_secondary

        self.key_on_pause = key_on_pause

        self.starship_bullets = arc.SpriteList()
        self.alien_bullets = arc.SpriteList()
        self.hit_effect_list = arc.SpriteList()

        # the player ship
        self.starship = Starship(
            fired_shots=self.starship_bullets,
            area_coords=[self.left, self.right, width, height],
            enemy_shots=self.alien_bullets,
            hit_effect_list=self.hit_effect_list,
        )
        self.starship.center_x = CONSTANTS.DISPLAY.WIDTH // 2
        self.starship.center_y = self.starship.height

    def on_update(self, delta_time: float) -> None:
        """Updates its sprites(lists)"""

        if self.on_pause:
            return

        if self.starship.can_reap():
            return
        # player update func considers its movement states
        # which were potentially changed
        self.starship.on_update(delta_time)
        self.starship_bullets.update()

    def draw(self) -> None:
        """Redraws its sprites"""
        self.starship_bullets.draw()

        if self.starship.can_reap():
            return

        self.starship.draw()
        self.starship.draw_hit_box(
            color=arc.color.BLUE_BELL,
            line_thickness=1.5,
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process player-sprite related key press events."""
        # set the paddle direction and movement speed
        if symbol == self.key_on_pause:
            self.on_pause = not self.on_pause
            self._parent_view.on_pause = self.on_pause

        if symbol == self.key_left:
            self.starship.moving_left = True
        elif symbol == self.key_right:
            self.starship.moving_right = True

        elif symbol == self.key_up:
            self.starship.moving_up = True
        elif symbol == self.key_down:
            self.starship.moving_down = True

        elif symbol == self.key_fire_primary:
            self.starship.firing_primary = True

        elif symbol == self.key_fire_secondary:
            if self.on_pause or self.starship.can_reap():
                self.window.show_view(self._parent_view.completion_callback_view)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Process player-sprite related key release events."""
        # since ship movement if based on change_x
        # stop it, since ship-sprite movement
        # is traggeable but not stoppable
        self.starship.stop()
        # trancate keys to ship movement state,
        # the rest is handled by the class itself
        # and its update method
        if symbol == self.key_left:
            self.starship.moving_left = False
        elif symbol == self.key_right:
            self.starship.moving_right = False

        elif symbol == self.key_up:
            self.starship.moving_up = False
        elif symbol == self.key_down:
            self.starship.moving_down = False

        elif symbol == self.key_fire_primary:
            self.starship.firing_primary = False
