from .moveset_stategy import on_update_plot_movement
from .evade_bullets import on_update_evade_bullets
from .fire_bullets import on_update_fire_bullets


class OnUpdateMixin:
    """Alien class mixins, triggered during .on_update calls

    Attributes
    ----------
    _spacial_danger_ranges : list[range]
        Ranges of danger-zones containing starship's bullets and itself.
    """

    def _on_update_evade_bullets(self, delta_time: float) -> None:
        on_update_evade_bullets(self, delta_time)

    def _on_update_plot_movement(self,delta_time: float) -> None:
        on_update_plot_movement(self, delta_time)

    def _on_update_fire_bullets(self,delta_time: float) -> None:
        on_update_fire_bullets(self, delta_time)
