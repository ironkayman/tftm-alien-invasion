from typing import Callable
import arcade as arc
from arcade import Point, Vector, EmitController, Particle

class MetaSpawner(arc.Emitter):
    """
    """

    def __init__(
        self,
        **emitter_kwargs,
    ) -> None:
        super().__init__(
            **emitter_kwargs,
        )
