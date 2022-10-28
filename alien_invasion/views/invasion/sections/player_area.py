import arcade as arc

from alien_invasion import CONSTANTS
from alien_invasion.entities import Starship

class PlayerArea(arc.Section):
    """Player ship area of movement.
    
    Handles and coordinates sprite lists
    contenets of which originated by player:

    - player's ship sprite `.ship`
    - player's ship sprite group
        of single ship sprite `.player`

    Ship can be moved left or right or shot;
    these events are handled in `on_key_press` / `on_key_release`
    """
    
    def __init__(self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        key_left: int,
        key_right: int,
        key_fire_primary: int,
        **kwargs
    ) -> None:
        """Area of a view in which ship is placed"""
        super().__init__(
            left, bottom, width, height,
            accept_keyboard_events={
                key_left,
                key_right,
                key_fire_primary,
                arc.key.B,
            },
            **kwargs
        )

        # keys assigned to move the paddle
        self.key_left: int = key_left
        self.key_right: int = key_right
        # if movement if l/r, and white both pressed any
        # other key on arrowpad wont be registered
        # also up, left wont register righ, right up  wond register left
        self.key_fire_primary: int = key_fire_primary

        self.player = arc.SpriteList()
        self.player_bullet_list: arc.SpriteList = arc.SpriteList()

        # the player ship
        self.ship = Starship(
            fired_shots=self.player_bullet_list,
            area_coords=[self.left, self.right, width, height]
        )
        self.ship.center_x = self.window.width / 2
        self.ship.center_y = self.ship.height

        self.player.append(self.ship)

    def on_update(self, delta_time: float) -> None:
        """Updates its sprites(lists)"""

        def purge_bullets_left_screen_area() -> None:
            """Processes bullets"""
            # remove all out of window player bullets
            for player_bullet in self.player_bullet_list:
                if player_bullet.bottom > self.window.height:
                    player_bullet.remove_from_sprite_lists()

        def prevent_starship_moving_outside_veiw() -> None:
            """check if player ship reaches view boundaries"""

            starship = self.player[0]
            if starship.left < self.left:
                starship.moving_left = False
                # consider ship axis step movement, return him partially to screen
                # this solution prevents jittering at high ship speed
                if starship.left < self.left - starship.width // 2:
                    starship.left = self.left - starship.width * 0.3

            if starship.right > self.right:
                starship.moving_right = False
                # hitbox_rightmost_axis_value = max(starship.get_adjusted_hit_box(), key=lambda point: point[0])[0]
                if starship.right > self.right + starship.width // 2:
                    starship.right = self.right + starship.width * 0.3

        # prevent_starship_moving_outside_veiw()
        # player update func considers its movement states
        # which were potentially changed
        self.player.update()
        self.player_bullet_list.update()

        purge_bullets_left_screen_area()

    def on_draw(self) -> None:
        """Redraws its sprites"""
        self.player.draw()
        self.player_bullet_list.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process player-sprite related key press events."""
        # set the paddle direction and movement speed
        # if symbol: breakpoint()
        print(symbol)
        if symbol == self.key_left:
            self.ship.moving_left = True
        elif symbol == self.key_right:
            self.ship.moving_right = True
        elif symbol == self.key_fire_primary:
            self.ship.firing_primary = True
        elif symbol == arc.key.B:
            breakpoint()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Process player-sprite related key release events."""
        # since ship movement if based on change_x
        # stop it, since ship-sprite movement
        # is traggeable but not stoppable
        self.ship.stop()
        # trancate keys to ship movement state,
        # the rest is handled by the class itself
        # and its update method
        if symbol == self.key_left:
            self.ship.moving_left = False
        elif symbol == self.key_right:
            self.ship.moving_right = False
        elif symbol == self.key_fire_primary:
            self.ship.firing_primary = False
