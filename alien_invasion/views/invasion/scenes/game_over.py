import arcade as arc

from alien_invasion import CONSTANTS


class GameOver(arc.Scene):
    """Game Over scene"""

    def __init__(self) -> None:
        super().__init__()

    def draw(self) -> None:
        # Render FPS formated with 2 decimal places
        arc.draw_text(
            "Game Over",
            start_x=CONSTANTS.DISPLAY.WIDTH // 3,
            start_y=CONSTANTS.DISPLAY.HEIGHT // 2.5,
            color=arc.color.GRAY_BLUE,
            font_size=42 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
        )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        return
