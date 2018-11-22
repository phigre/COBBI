import numpy as np
import pandas as pd
from scipy.signal import convolve2d

def mean_BIAS(a1, a2, ice_mask=None):
    if type(ice_mask) is pd.core.series.Series:
        dev = (a1 - a2)
        print(ice_mask.apply(np.sum))
        return dev.apply(np.sum) / ice_mask.apply(np.sum)

    if ice_mask is None:
        dev = a1 - a2
    else:
        dev = np.ma.masked_array(a1 - a2, mask=np.logical_not(ice_mask))
    return dev.mean()


def RMSE(a1, a2, ice_mask=None):
    if type(ice_mask) is pd.core.series.Series:
        dev = (a1 - a2)
        dev = dev * ~ice_mask
        dev_sq = dev ** 2
        m_dev_sq = dev_sq.apply(np.sum) / ice_mask.apply(np.sum)
        return np.sqrt(m_dev_sq)

    if ice_mask is None:
        dev = a1 - a2
    else:
        dev = np.ma.masked_array(a1 - a2, mask=np.logical_not(ice_mask))
    return np.sqrt((dev**2).mean())


def compute_inner_mask(ice_mask, full_array=False):
    conv_array = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])  # TODO
    if full_array:
        conv_array = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])  # TODO
    inner_mask = convolve2d(ice_mask, conv_array, mode='same') == \
                 conv_array.sum()
    return inner_mask