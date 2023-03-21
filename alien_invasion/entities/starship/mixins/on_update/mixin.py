from .energy import on_update_energy_capacity
from .movement import on_update_movement
from .weapons import on_update_firing

class OnUpdateMixin():

    def _on_update_energy_capacity(
        self,
        delta_time: float,
        frame_energy_change: float,
    ):
        on_update_energy_capacity(self, delta_time, frame_energy_change)

    def _on_update_movement(
        self,
        delta_time: float
    ):
        on_update_movement(self, delta_time)

    def _on_update_firing(
        self,
        delta_time: float,
        frame_energy_change: float
    ):
        on_update_firing(self, delta_time, frame_energy_change)
