import arcade as arc

from alien_invasion import CONSTANTS

from alien_invasion.settings import KEYMAP


class GameOver(arc.Scene):
    """Game Over scene"""

    def __init__(self) -> None:
        super().__init__()
        self.label = arc.Text(
            text="Game Over",
            start_x=CONSTANTS.DISPLAY.WIDTH * 0.545,
            start_y=CONSTANTS.DISPLAY.HEIGHT * 0.485,
            color=arc.color.WHITE_SMOKE,
            font_size=44 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
        )
        self.exit = arc.Text(
            text=f"Press 'x' to return",
            start_x=CONSTANTS.DISPLAY.WIDTH * 0.585,
            start_y=CONSTANTS.DISPLAY.HEIGHT * 0.38,
            color=arc.color.WHITE_SMOKE,
            font_size=16 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
        )

    def draw(self) -> None:
        arc.draw_lrtb_rectangle_filled(
            left=CONSTANTS.DISPLAY.WIDTH * 0.613,
            right=CONSTANTS.DISPLAY.WIDTH * 0.87,
            top=CONSTANTS.DISPLAY.HEIGHT,
            bottom=0,
            color=(214, 10, 54)
        )
        self.label.draw()
        self.exit.draw()
