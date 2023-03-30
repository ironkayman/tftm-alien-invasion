from .base_item import Item, ItemType

class ItemWeapon(Item):
    """
    Parameters
    ----------
    model_name : str
        Model type name

    Attributes
    ----------
    energy_per_bullet : int
        Enegry of ship's reactor consumed for a single bullet.
    recharge_timeout : int
        Time between bullet launches in `ms`.
    speed : int
        Pixels of space traversed per sec.
    """

    item_type: ItemType = ItemType.WEAPON

    bullet_damage: int
    energy_per_bullet: int
    recharge_timeout: int
    speed: int

