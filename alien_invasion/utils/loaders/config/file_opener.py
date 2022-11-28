from typing import Tuple, Any
from types import EllipsisType

from pathlib import Path
from json import load, JSONDecodeError

def reader(file_path) -> Tuple[dict[str, Any]|EllipsisType, EllipsisType|FileNotFoundError|JSONDecodeError]:
    """Read JSON file at `file_path`.

    Arguments
    ---------
    file_path : Path
        absolute path to `.json`

    Returns
    -------
    Tuple[dict, EllipsisType]|
    Tuple[EllipsisType, FileNotFoundError|JSONDecodeError]
        Config (if present) and an exception (if present).
    """
    def open_config() -> None:
        """Reads config to nonlocal variable.

        Reads config JSON at `config_file_path`
        to nonlocal variable `config`.
        """
        nonlocal config

        with open(
            file_path,
            mode='r',
            encoding='utf-8-sig'
        ) as config_wrap:
            config = load(config_wrap)

    config, error = ..., ...

    try:
        open_config()
    except FileNotFoundError as err:
        print("no config found")
        error = err
        # create?
    except JSONDecodeError as err:
        error = err
        print(error)
        exit(0)
    return config, error