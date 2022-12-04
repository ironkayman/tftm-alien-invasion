import arcade as arc

from alien_invasion import CONSTANTS


class PilotOverlay(arc.Section):
    """Starship's pilot overlay UI components."""
    def __init__(
        self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        **kwargs,
    ) -> None:
        super().__init__(
            left,
            bottom,
            width,
            height,
            **kwargs
        )

        pass

    def on_draw(self) -> None:
        # Render FPS formated with 2 decimal places
        arc.draw_text(
            f"FPS: {arc.get_fps():.2f}",
            start_x=35,
            start_y=self.window.height - 35,
            color=arc.color.GRAY_BLUE,
            font_size=12,
            font_name="Courier New",
        )