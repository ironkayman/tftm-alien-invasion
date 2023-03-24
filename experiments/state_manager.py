from typing import NamedTuple, Generator, Optional


def StateManager(states: list[dict[str, dict]]) -> Generator[tuple[int, str, dict], None, None]:
    """

    Examples
    --------
    >>> states = [
        {'initial': {...}},
    ]
    """
    for index, state in enumerate(states):
        yield index, *tuple(*state.items())  # type: ignore

class StateManager2:
    def __init__(
        self,
        states: list[dict[str, dict]],
        current_state: Optional[dict] = None,
        current_state_index: Optional[int] = None,
    ) -> None:
        """

        Examples
        --------
        >>> states = [
            {'initial': {...}},
        ]
        """
        self.__states = states
        self.__current_state: dict = current_state or {}
        self.__current_state_index: int = current_state_index or 0

    def __iter__(self):
        return self.__states

    def __next__(self) -> tuple[int, str, dict, IndexError|None]:
        err = None
        try:
            state_name, self.__current_state = [*self.__states[self.__current_state_index].items()][0]
            self.__current_state['index'] = self.__current_state_index
            self.__current_state['name'] = state_name
        except IndexError as e:
            err = e
        else:
            self.__current_state_index += 1
        return (
            self.__current_state,
            err
        )

    def next(self):
        return self.__next__()

sm = StateManager2(
    [
        {'initial': {'a': 1}},
        {'initial2': {'a2': 12}},
    ],
)

# v = next(sm)
# print(v)
# v2 = next(sm)
# print(v2)
# v3 = next(sm)
# print(v3)

v = sm.next()
print(v)
v1 = sm.next()
print(v1)
v2 = sm.next()
print(v2)
