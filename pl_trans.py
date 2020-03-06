from pl_py import StreakImage
from typing import Union, List
import numpy as np


def calc_trans(
    im: Union[StreakImage, List[StreakImage]],
    wl_min: int = None,
    wl_max: int = None,
    t_min: int = None,
    t_max: int = None,
):
    """Calculate transients for each object of type StreakImage in im.
    
    params:
        im: StreakImage or list of StreakImage
        bot, top: wavelength borders for transient calculation
    """
    if isinstance(im, StreakImage):
        calc_transient(im, wl_min, wl_max, t_min, t_max)
    elif isinstance(im, List):
        for image in im:
            calc_transient(image, wl_min, wl_max, t_min, t_max)


def calc_transient(
    image: StreakImage,
    wl_min: int = None,
    wl_max: int = None,
    t_min: int = None,
    t_max: int = None,
):
    """Calculate transients for image.

    params:
        image: StreakImage
        wl_min, wl_max: wavelength borders for transient calculation
        t_min, t_max: time borders for transient calculation
    """

    if not wl_min:
        wl_min = image.data.columns.min()
    if not wl_max:
        wl_max = image.data.columns.max()
    if not t_min:
        t_min = image.data.index.min()
    if not t_max:
        t_max = image.data.index.max()

    df = image.data.loc[t_min:t_max, wl_max:wl_min]
    trans = np.sum(a=df, axis=1)
    image.transient = trans


def subtract_bg(image: StreakImage, bg: StreakImage):
    """Subtract bg from image.
    Checks if bg is already subtracted and raises error if so.

    params:
        image: StreakImage to subtract bg from.
        bg: The bg to subtract.
    """
    if not image.bg_sub_corr:
        image.data = image.data - bg.data
        image.bg_sub_corr = True
    else:
        raise ValueError("Background already subtracted.")

