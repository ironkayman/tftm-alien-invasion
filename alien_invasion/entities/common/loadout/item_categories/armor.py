from .base_item import Item, ItemType

class ItemArmor(Item):
    """
    Parameters
    ----------
    model_name : str
        Model type name
    """

    item_type: ItemType = ItemType.ARMOR

    armor: int
