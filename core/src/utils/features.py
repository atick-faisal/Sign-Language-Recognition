import numpy as np
import pandas as pd
from scipy.signal import resample

from config import Config


def extract_flxion_features(
    data: pd.DataFrame,
    segment_length: int = 150
) -> np.ndarray:
    features = pd.DataFrame()

    # ... Distance to thumb finger-tip
    features["drf0"] = np.sqrt(
        np.square(data["rf0x"] - data["rpx"]) +
        np.square(data["rf0z"] - data["rpz"])
    )

    # ... Distance to index finger-tip
    features["drf1"] = np.sqrt(
        np.square(data["rf1x"] - data["rpx"]) +
        np.square(data["rf1z"] - data["rpz"])
    )

    # ... Distance to middle finger-tip
    features["drf2"] = np.sqrt(
        np.square(data["rf2x"] - data["rpx"]) +
        np.square(data["rf2z"] - data["rpz"])
    )

    # ... Thumb coordineates wrt palm (for determining orientation)
    features["drf0x"] = data["rf0x"] - data["rpx"]
    features["drf0z"] = data["rf0z"] - data["rpz"]

    # Features v1.0
    # features["drf0x"] = data["rf0x"] - data["rpx"]
    # features["drf0y"] = data["rf0y"] - data["rpy"]
    # features["drf0z"] = data["rf0z"] - data["rpz"]

    # features["drf1x"] = data["rf1x"] - data["rpx"]
    # features["drf1y"] = data["rf1y"] - data["rpy"]
    # features["drf1z"] = data["rf1z"] - data["rpz"]

    # ... Min-Max scaling of distance features
    features = (features - Config.SCALER_MIN) / Config.SCALER_RANGE

    return resample(features.to_numpy(), segment_length, axis=0)
