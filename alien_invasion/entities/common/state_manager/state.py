from pathlib import Path
from enum import IntEnum, auto

from pydantic import (
    BaseModel,
    validator,
)

from ..loadout import Loadout

class AlienSize(IntEnum):
    """Allowed enemy sizes"""

    small = auto()
    medium = auto()
    large = auto()
    colossal = auto()
    unimaginable = auto()


class AlienType(IntEnum):
    """Allowed enemy types"""

    # Tier 1
    corporeal = auto()
    ancient = auto()
    # Tier 2
    possessed = auto()
    undead = auto()
    # Tier 3
    narrativistic = auto()
    metaphysic = auto()

class AlienMoveset(IntEnum):
    """Allowed movesets for an arbitrary state.

    Attributes
    ----------
    spiralling : int
        Flies across screen (left<->right) in overlapping circles.
    tracking : int
        Vaguely follows starship's x-axis and when needed dodges bullets.
    escaping : int
        Opposite of `tracking`, tries never to cross x-axis of a starship.
    """

    spiralling = auto()
    tracking = auto()
    escaping = auto()


class State(BaseModel):
    """Scheme for `Alien` states data strcture

    Attributes
    ----------
    name: str
        State name.
    movesets: set[AlienMoveset]
        Movesets available for this alien's state represented as Enums.
    hp: int
        HitPoints for this state.
    death_damage_cap: bool
        Does damage beyond hp = 0 is translated to damage to alen's nex state.
        `True` - damage is capped whch means that next state does not
        absorb this state's incoming damage.
        `False` - remaining from hp = 0 damage is absorbed by
        next alien's state if any present, dealng damage to its HP bar.
    texture: Path
        Path to a state's texure.
    """

    # required kwargs
    movesets: set[AlienMoveset]
    speed: int
    hp: int
    death_damage_cap: bool

    # meta
    name: str
    index: int

    # overrides of prev state, optional
    bullet_damage: int | None
    bullet_speed: int | None
    recharge_timeout: int | None

    # wrappers
    data: dict
    texture_path: Path


    @validator('movesets', pre=True)
    def get_movesets(cls, val) -> set[AlienMoveset]:
        """Turns moveset string names to Enums"""
        return set(map(lambda m: AlienMoveset[m], val))

    def __init__(self,
        name: str,
        index: int,
        texture_path: Path,
        data: dict,
    ) -> None:
        """Maps groups of entity's properties to a coherent data structure

        Parameters
        ----------
        name : str
            State's name.
        index : int
            State's position in queue.
        texture_path : Path
            Corresponding texture to a given state by its name att `state_name`.
        data : dict
            All data from `::state:state_name`.

        Examples
        --------
        >>> name
        'initial'
        >>> data
        {
            'movesets': ['tracking'],
            'speed': 90,
            'hp': 20,
            'death_damage_cap': False,
            'bullet_damage': 8,
            'bullet_speed': 800,
            'recharge_timeout': 300
        }
        >>> texture_path
        PosixPath('/home/kayman/git/mtt/tftm-alien-invasion/data/aliens/dummy_ufo/state.initial.png')
        """

        super().__init__(
            name=name,
            index=index,
            data=data,
            texture_path=texture_path,
            **data,
        )

