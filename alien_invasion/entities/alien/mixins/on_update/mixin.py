from .moveset_stategy import on_update_plot_movement

class OnUpdateMixin:
    """Alien class mixins, triggered during .on_update calls
    """

    def _on_update_plot_movement(
        self,
        delta_time: float,
    ):
        on_update_plot_movement(self, delta_time)
