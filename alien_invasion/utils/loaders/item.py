from pathlib import Path
from json import loads

from alien_invasion import CONSTANTS
from .config.file_opener import reader

def search(name):
    """
    Raises
    ------
    IndexError
        No ite was found at `glob`
    """
    search_root = CONSTANTS.DIR_DATA / 'starship'
    return tuple(search_root
        .glob(f'*/{name}.json'))[0]

def load_item_as_dict(name: str) -> object:
    """ """
    try:
        found_path = search(name)
    except IndexError:
        print(f"no item found: {name}")
        exit(0)
    sw = reader(found_path)
    if sw[1] is not Ellipsis:
        print('at path', found_path, sw[1])
        exit(0)
    return sw[0]