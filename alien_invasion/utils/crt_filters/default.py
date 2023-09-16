"""Default CRT Filter
"""

from arcade import Window
from arcade.experimental.crt_filter import CRTFilter
from pyglet.math import Vec2


def CRTFilterDefault(window: Window) -> CRTFilter:
    """Creates Default CRT Filter

    Parameters
    ----------
    window : Window
        `Window`-like object with
        attributes `width` and `height`.

    Returns
    -------
    CRTFilter
        Finalised CRT filter.
    """
    return CRTFilter(
        width=window.width,
        height=window.height,
        resolution_down_scale=5.0,
        hard_scan=-15.0,
        hard_pix=-10.0,
        display_warp=Vec2(0.0, 0.0),
        mask_dark=1.0,
        mask_light=1.5,
    )


def CRTFilterForeground(window: Window) -> CRTFilter:
    """Creates Default CRT Filter

    Parameters
    ----------
    window : Window
        `Window`-like object with
        attributes `width` and `height`.

    Returns
    -------
    CRTFilter
        Finalised CRT filter.
    """
    return CRTFilter(
        width=window.width,
        height=window.height,
        resolution_down_scale=3.5,
        hard_scan=-15.0,
        hard_pix=-10.0,
        display_warp=Vec2(0.0, 0.0),
        mask_dark=1.0,
        mask_light=1.5,
    )
