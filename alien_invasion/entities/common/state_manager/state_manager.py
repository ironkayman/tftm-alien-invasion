from .state import State

class StateManager:
    def __init__(
        self,
        states: list[dict[str, dict]],
    ) -> None:
        """

        Examples
        --------
        >>> states = StateManager([
            {'initial': {
                state_name: str,
                state_data: dict,
                texture_path: Path,
                index: int
            }},
        ])
        >>> next(states)
        ...
        """
        self._states = states
        self._current_state = {}
        self._current_state_index = 0

    def __iter__(self):
        return self._states

    class FinalStateReached(IndexError):
        pass

    def __next__(self) -> tuple[State, IndexError|None]:
        err = None
        try:
            state_name, self._current_state = [*self._states[self._current_state_index].items()][0]
            self._current_state['index'] = self._current_state_index
            self._current_state['name'] = state_name
        except IndexError as e:
            err = StateManager.FinalStateReached
        else:
            self._current_state_index += 1
        return (
            State(**self._current_state),
            err
        )
