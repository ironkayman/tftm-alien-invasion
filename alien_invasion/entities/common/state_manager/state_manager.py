from .state import State


class FinalStateReached(IndexError):
    pass


class StateManager:
    def __init__(
        self,
        states: list[dict[str, dict]],
    ) -> None:
        """

        Examples
        --------
        >>> states = StateManager([
            {
                state_name: str,
                state_data: dict,
                index: int
                registry_texture_id: str | None
            },
        ])
        >>> next(states)
        ...
        """
        self._states = states
        self._current_state = {}
        self._current_state_index = 0

    def __iter__(self):
        return iter(self._states)

    def __next__(self) -> tuple[State, IndexError | None]:
        err = None
        try:
            self._current_state = self._states[self._current_state_index]
        except IndexError as e:
            err = FinalStateReached
        else:
            self._current_state_index += 1
        return (State(**self._current_state), err)
