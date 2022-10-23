from alien_invasion.utils.loaders import config_loader, load_save_files

KEYMAP = config_loader()['keymap']
SAVES = load_save_files()