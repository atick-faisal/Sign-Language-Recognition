from xml.dom import InvalidAccessErr
import numpy as np


def normalize(x: np.ndarray) -> np.ndarray:
    try:
        return (x - np.min(x)) / (np.max(x) - np.min(x))
    except ZeroDivisionError:
        return x
