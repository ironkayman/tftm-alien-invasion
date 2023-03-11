from typing import Tuple, Any
from types import EllipsisType

from json import load as json_load, JSONDecodeError
from toml import load as toml_load, TomlDecodeError


def reader(file_path) -> Tuple[dict[str, Any]|EllipsisType, EllipsisType|FileNotFoundError|JSONDecodeError|TomlDecodeError]:
    """Read JSON/TOML file at `file_path`.

    Arguments
    ---------
    file_path : Path
        absolute path to `.json`/`.toml`

    Returns
    -------
    Tuple[dict, EllipsisType]|
    Tuple[EllipsisType, FileNotFoundError|JSONDecodeError|TomlDecodeError]
        Config (if present) and an exception (if present).
    """
    def read_file() -> None:
        """Reads file to nonlocal variable.

        Reads file at `file_path`
        to nonlocal variable `config`.
        """
        nonlocal config

        with open(
            file_path,
            mode='r',
            encoding='utf-8-sig'
        ) as config_wrap:
            if file_path.suffix == '.json':
                config = json_load(config_wrap)
            elif file_path.suffix == '.toml':
                config = toml_load(config_wrap)

    config, error = ..., ...

    try:
        read_file()
    except FileNotFoundError as err:
        print("no config found")
        error = err
        # create?
    except (JSONDecodeError, TomlDecodeError) as err:
        error = err
        print(error)
        exit(0)
    return config, error