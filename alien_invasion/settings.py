from alien_invasion.utils.loaders import config_loader

CONFIG_DICT = config_loader()

KEYMAP = CONFIG_DICT['keymap']
STARSHIP = CONFIG_DICT['starship']