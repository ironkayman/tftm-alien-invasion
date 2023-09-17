import arcade as arc

from alien_invasion import CONSTANTS


class StarshipControls(arc.Section, arc.Scene):
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
        key_left: int,
        key_right: int,
        key_up: int,
        key_down: int,
        key_fire_primary: int,
        key_fire_secondary: int,
        key_on_pause: int,
        starship,
        parent_view,
        **kwargs
    ) -> None:
        """Area of a view in which ship is placed"""
        # Manual MRO resolution
        arc.Section.__init__(
            self,
            0,
            0,
            CONSTANTS.DISPLAY.WIDTH,
            CONSTANTS.DISPLAY.HEIGHT,
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
        self.starship = starship

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

    def on_update(self, delta_time: float) -> None:
        """Updates its sprites(lists)"""

        if self.on_pause:
            return

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process player-sprite related key press events."""
        # set the paddle direction and movement speed
        if symbol == self.key_on_pause:
            self.on_pause = not self.on_pause
            self._parent_view.on_pause = not self._parent_view.on_pause

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
