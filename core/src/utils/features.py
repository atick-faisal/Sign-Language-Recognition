import numpy as np
import pandas as pd
from scipy.signal import resample

from config import Config


def extract_flxion_features(
    data: pd.DataFrame,
    segment_length: int = 150
) -> np.ndarray:
    features = pd.DataFrame()

    # Features v1.0
    features["drf0x"] = data["rf0x"] - data["rpx"]
    features["drf0y"] = data["rf0y"] - data["rpy"]
    features["drf0z"] = data["rf0z"] - data["rpz"]

    features["drf1x"] = data["rf1x"] - data["rpx"]
    features["drf1y"] = data["rf1y"] - data["rpy"]
    features["drf1z"] = data["rf1z"] - data["rpz"]

    # Features v1.1
    # features["drf0x"] = data["rf0x"] - data["rpx"]
    # features["drf0z"] = data["rf0z"] - data["rpz"]

    # features["drf1x"] = data["rf1x"] - data["rpx"]
    # features["drf1z"] = data["rf1z"] - data["rpz"]

    # ... Features v2.0 (Failed)
    # ... Distance to thumb finger-tip
    # features["drf0"] = np.sqrt(
    #     np.square(data["rf0x"] - data["rpx"]) +
    #     np.square(data["rf0z"] - data["rpz"])
    # )

    # # ... Distance to index finger-tip
    # features["drf1"] = np.sqrt(
    #     np.square(data["rf1x"] - data["rpx"]) +
    #     np.square(data["rf1z"] - data["rpz"])
    # )

    # # ... Distance to middle finger-tip
    # features["drf2"] = np.sqrt(
    #     np.square(data["rf2x"] - data["rpx"]) +
    #     np.square(data["rf2z"] - data["rpz"])
    # )

    # # ... Thumb coordineates wrt palm (for determining orientation)
    # features["drf0x"] = data["rf0x"] - data["rpx"]
    # features["drf0z"] = data["rf0z"] - data["rpz"]

    # # ... Features 3.0
    # dist_features = pd.DataFrame()
    # diff_features = pd.DataFrame()

    # # ... Distance to thumb finger-tip
    # dist_features["drf0"] = np.sqrt(
    #     np.square(data["rf0x"] - data["rpx"]) +
    #     np.square(data["rf0z"] - data["rpz"])
    # )

    # # ... Distance to index finger-tip
    # dist_features["drf1"] = np.sqrt(
    #     np.square(data["rf1x"] - data["rpx"]) +
    #     np.square(data["rf1z"] - data["rpz"])
    # )

    # # ... Distance to middle finger-tip
    # dist_features["drf2"] = np.sqrt(
    #     np.square(data["rf2x"] - data["rpx"]) +
    #     np.square(data["rf2z"] - data["rpz"])
    # )

    # # ... Thumb coordineates wrt palm (for determining orientation)
    # diff_features["drf0x"] = data["rf0x"] - data["rpx"]
    # diff_features["drf0z"] = data["rf0z"] - data["rpz"]

    # # dist_features = dist_features / dist_features.max(axis=0)

    # features = pd.concat([dist_features, diff_features], axis=1)

    # ... Min-Max scaling of distance features
    features = (features - Config.SCALER_MIN) / Config.SCALER_RANGE

    # ... Z-score normalization
    # features = (features - Config.SCALER_MEAN) / Config.SCALER_STD

    return resample(features.to_numpy(), segment_length, axis=0)
