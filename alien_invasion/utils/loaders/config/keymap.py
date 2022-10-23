import arcade as arc

def load_keymap(config: dict) -> dict:
    """Load keymap from readable dict-like config.

    Parameters
    ----------
    config : dict
        Read config in a form of dict.

    Returns
    -------
    keymap_arcade : dict
        keymap section of a config with arcade constants
        for key numbers.
    """
    keymap_config = config['current_keymap']
    keymap_arcade = {}

    keys = [
        'start',
        'pause',
        'quit',
        'player_starship_movement_left',
        'player_starship_movement_right',
        'player_starship_fire_primary'
    ]
    for key in keys:
        keymap_arcade[key] = getattr(arc.key, keymap_config[key].upper())
    return keymap_arcade