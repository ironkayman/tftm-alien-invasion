from base_item import Item, ItemType

class ItemEngine(Item):
    """
    Parameters
    ----------
    model_name : str
        Model type name

    Attributes
    ----------
    energy_restored : int
        Energy restored per second.
    energy_cap : int
        Energy capacity, maximum for reactor.
    """

    item_type: ItemType = ItemType.ENGINE

    energy_restored: int
    energy_cap: int
