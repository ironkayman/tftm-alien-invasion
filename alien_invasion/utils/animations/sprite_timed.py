from pathlib import Path
from abc import ABC

import arcade as arc


class SpriteTimed(arc.Sprite, ABC):
    def __init__(
        self,
        filename: Path,
        scale: float,
        timer_interval: float = 1.0,
        timer: float = 0.0,
    ) -> None:
        """Sprite with built-in timer"""
        super().__init__(filename, scale)

        self._timer = timer
        self._timer_interval = timer_interval

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._timer += delta_time
        if self._timer > self._timer_interval:
            self._timer = 0.0
            self.timed_update()
        return super().on_update(delta_time)

    def timed_update(self) -> None:
        raise NotImplementedError
