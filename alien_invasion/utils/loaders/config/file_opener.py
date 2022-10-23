from pathlib import Path
from json import load, JSONDecodeError

def reader() -> [dict, Exception]:
    def open_config() -> None:
        nonlocal config
        with open(config_file_path, mode='r', encoding='utf-8-sig') as config_wrap:
            config = load(config_wrap)

    config, error = ..., ...
    config_file_path = Path().cwd().joinpath('configs/config.json')

    try:
        open_config()
    except FileNotFoundError as err:
        print("no config found")
        error = err
    except JSONDecodeError as err:
        error = err
    return config, error