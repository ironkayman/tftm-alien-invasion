import arcade as arc

from alien_invasion import CONSTANTS

from ..sections import PlayerArea

class PilotOverlay(arc.Scene):
    """Starship's pilot overlay UI components."""
    def __init__(self, player_area: PlayerArea) -> None:
        super().__init__()
        self.starship = player_area.starship

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

        arc.draw_text(
            (
                f"Reactor: {self.starship.current_energy_capacity:.1f}/"
                f"{self.starship.loadout.engine.energy_cap}"
            ),
            start_x=35,
            start_y=CONSTANTS.DISPLAY.HEIGHT - 70,
            color=arc.color.GRAY_BLUE,
            font_size=12,
            font_name="Courier New",
        )

        arc.draw_text(
            f"HP ({self.starship.state}): {self.starship.hp}",
            start_x=35,
            start_y=CONSTANTS.DISPLAY.HEIGHT - 105,
            color=arc.color.GRAY_BLUE,
            font_size=12,
            font_name="Courier New",
        )

    def on_update(self, delta_time: float = 1 / 60) -> None:
        pass
