import arcade as arc

from alien_invasion import CONSTANTS


class PilotOverlay(arc.Scene):
    """Starship's pilot overlay UI components."""
    def __init__(self) -> None:
        super().__init__()

        pass

    def draw(self) -> None:
        # Render FPS formated with 2 decimal places
        arc.draw_text(
            f"FPS: {arc.get_fps():.2f}",
            start_x=35,
            start_y=CONSTANTS.DISPLAY.HEIGHT - 35,
            color=arc.color.GRAY_BLUE,
            font_size=12,
            font_name="Courier New",
        )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        pass
