from .base_item import Item, ItemType

class ItemThruster(Item):
    """
    Parameters
    ----------
    model_name : str
        Model type name

    Attributes
    ----------
    velocity : int
    energy_requirement : int
    """

    item_type: ItemType = ItemType.THRUSTER

    velocity: int
    energy_requirement: int