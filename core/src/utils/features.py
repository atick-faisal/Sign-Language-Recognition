import numpy as np
import pandas as pd
from scipy.signal import resample

from config import Config


def extract_flxion_features(
    data: pd.DataFrame,
    segment_length: int = 150
) -> np.ndarray:
    data["drf0x"] = data["rf0x"] - data["rpx"]
    data["drf0y"] = data["rf0y"] - data["rpy"]
    data["drf0z"] = data["rf0z"] - data["rpz"]

    data["drf1x"] = data["rf1x"] - data["rpx"]
    data["drf1y"] = data["rf1y"] - data["rpy"]
    data["drf1z"] = data["rf1z"] - data["rpz"]

    data = data[Config.DIST_FEATURES]

    # ... Min-Max scaling of distance features
    data = (data - Config.SCALER_MIN) / Config.SCALER_RANGE

    return resample(data.to_numpy(), segment_length, axis=0)
