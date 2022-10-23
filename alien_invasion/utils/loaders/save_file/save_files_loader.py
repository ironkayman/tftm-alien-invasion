from typing import Generator
from json import loads, JSONDecodeError

from alien_invasion.constants import DIR_SAVES

SAVE_FILE_EXTENSION_PATTERN = '*.json'

def load_save_files() -> list[dict]:
  """
  """
  saves = []
  for save_file in DIR_SAVES.glob(SAVE_FILE_EXTENSION_PATTERN):
    with open(save_file) as contents:
      try:
        saves.append(loads(contents.read()))
      except JSONDecodeError as ex:
        print(f'Save {save_file.stem} not loaded due to: {ex}')
  print(saves)
  return saves