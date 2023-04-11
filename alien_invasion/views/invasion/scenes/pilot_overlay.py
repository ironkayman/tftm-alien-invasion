import arcade as arc

from alien_invasion import CONSTANTS

from ..sections import PlayerArea

class PilotOverlay(arc.Scene):
    """Starship's pilot overlay UI components."""

    def __init__(self, player_area: PlayerArea) -> None:
        super().__init__()
        # self.starship = player_area.starship

        # Render FPS formated with 2 decimal places
        self.fps = arc.Text(
            f"FPS: {arc.get_fps():.2f}",
            start_x=0,
            start_y=0,
            color=arc.color.GRAY_BLUE,
            font_size=12,
            font_name="Courier New",
            anchor_x='left',
            anchor_y='top',
        )
        # self.reactor = arc.Text(
        #     (
        #         f"{100*(self.starship.current_energy_capacity/self.starship.loadout.engine.energy_cap):.0f}%"
        #     ),
        #     start_x=self.starship.center_x - 60,
        #     start_y=self.starship.top + 12,
        #     color=arc.color.AERO_BLUE if not self.starship.free_falling else arc.color.MAYA_BLUE,
        #     font_size=12,
        #     font_name="Courier New",
        # )

    def update(self) -> None:
        self.fps.text = f"FPS: {arc.get_fps():.2f}"

        self.reactor.text = f"{100*(self.starship.current_energy_capacity/self.starship.loadout.engine.energy_cap):.0f}%"
        self.reactor.color = arc.color.AERO_BLUE if not self.starship.free_falling else arc.color.MAYA_BLUE

        return super().update()

    def draw(self) -> None:
        super().draw()
        # self.fps.draw()
        # self.reactor.draw()

        # if self.starship.state.index != 1:
        #     arc.draw_text(
        #         f"{100*(self.starship.hp/self.starship.max_hp):.0f}%",
        #         start_x=self.starship.center_x + 20,
        #         start_y=self.starship.top + 12,
        #         color=arc.color.TEA_GREEN,
        #         font_size=12,
        #         font_name="Courier New",
        #     )
        # else:
        #     arc.draw_text(
        #         f"Ω {22}%",
        #         start_x=self.starship.center_x + 20,
        #         start_y=self.starship.top + 12,
        #         color=arc.color.RED_DEVIL,
        #         font_size=12,
        #         font_name="Courier New",
        #     )
        # arc.draw_text(
        #     f"{self.starship.xp}",
        #     start_x=self.starship.center_x + 35,
        #     start_y=self.starship.center_y - 5,
        #     color=arc.color.PURPLE_HEART,
        #     font_size=12,
        #     font_name="Courier New",
        # )
