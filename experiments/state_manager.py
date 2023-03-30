from typing import NamedTuple, Generator, Optional


# def StateManager_proto(states: list[dict[str, dict]]) -> Generator[tuple[int, str, dict], None, None]:
#     """

#     Examples
#     --------
#     >>> states = [
#         {'initial': {...}},
#     ]
#     """
#     for index, state in enumerate(states):
#         yield index, *tuple(*state.items())  # type: ignore

class StateManager:
    def __init__(
        self,
        states: list[dict[str, dict]],
    ) -> None:
        """

        Examples
        --------
        >>> states = StateManager([
            {'initial': {...}},
        ])
        """
        self.__states = states
        self.__current_state = {}
        self.__current_state_index = 0

    def __iter__(self):
        return self.__states

    def __next__(self) -> tuple[dict, IndexError|None]:
        err = None
        try:
            state_name, self.__current_state = [*self.__states[self.__current_state_index].items()][0]
            self.__current_state['index'] = self.__current_state_index
            self.__current_state['name'] = state_name
            self.__apply_overrides()
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

    def __apply_overrides(self) -> None:
        return


sm = StateManager(
    [
        {'initial': {'a': 1}},
        {'initial2': {'a2': 12}},
    ],
)

v = next(sm)
print(v)
v = next(sm)
print(v)
v = next(sm)
print(v)
