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
            start_x=CONSTANTS.DISPLAY.SCALE_RELATION // 11,
            start_y=CONSTANTS.DISPLAY.HEIGHT * 10/11,
            color=arc.color.GRAY_BLUE,
            font_size=12 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
            anchor_x='left',
            anchor_y='top',
        )
        arc.draw_text(
            (
                f"{100*(self.starship.current_energy_capacity/self.starship.loadout.engine.energy_cap):.0f}%"
            ),
            start_x=self.starship.center_x - 60 * CONSTANTS.DISPLAY.SCALE_RELATION,
            start_y=self.starship.top + 12 * CONSTANTS.DISPLAY.SCALE_RELATION,
            color=arc.color.AERO_BLUE if not self.starship.free_falling else arc.color.MAYA_BLUE,
            font_size=12 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
        )

        if self.starship.state.index != 1:
            arc.draw_text(
                f"{100*(self.starship.hp/self.starship.max_hp):.0f}%",
                start_x=self.starship.center_x + 20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                start_y=self.starship.top + 12 * CONSTANTS.DISPLAY.SCALE_RELATION,
                color=arc.color.TEA_GREEN,
                font_size=12 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
            )
        else:
            arc.draw_text(
                f"Ω {22}%",
                start_x=self.starship.center_x + 20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                start_y=self.starship.top + 12 * CONSTANTS.DISPLAY.SCALE_RELATION,
                color=arc.color.RED_DEVIL,
                font_size=12 * CONSTANTS.DISPLAY.SCALE_RELATION,
                font_name="Courier New",
            )
        arc.draw_text(
            f"{self.starship.xp}",
            start_x=self.starship.center_x + 35 * CONSTANTS.DISPLAY.SCALE_RELATION,
            start_y=self.starship.center_y - 5 * CONSTANTS.DISPLAY.SCALE_RELATION,
            color=arc.color.PURPLE_HEART,
            font_size=12 * CONSTANTS.DISPLAY.SCALE_RELATION,
            font_name="Courier New",
        )
