import numpy as np
from scipy.signal import butter, lfilter


class LowPassFilter(object):
    def butter_lowpass(
        cutoff: int,
        fs: int,
        order: int
    ):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype="low", analog=False)
        return b, a

    def apply(
        data: np.ndarray,
        cutoff: int = 6,
        fs: int = 100,
        order: int = 2
    ) -> np.ndarray:
        b, a = LowPassFilter.butter_lowpass(cutoff, fs, order)
        y = lfilter(b, a, data)
        return y
