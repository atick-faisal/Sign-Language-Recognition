import numpy as np
import pandas as pd
from scipy.signal import resample
import config


def extract_flxion_features(
    data: pd.DataFrame,
    segment_length: int = 150,
    hand: str = "r"
) -> np.ndarray:
    data["drf0x"] = data["rf0x"] - data["rpx"]
    data["drf0y"] = data["rf0y"] - data["rpy"]
    data["drf0z"] = data["rf0z"] - data["rpz"]

    data["drf1x"] = data["rf1x"] - data["rpx"]
    data["drf1y"] = data["rf1y"] - data["rpy"]
    data["drf1z"] = data["rf1z"] - data["rpz"]

    data = data[config.DIST_FEATURES]

    # ... Min-Max scaling of distance features
    data = (data - config.SCALER_MIN) / config.SCALER_RANGE

    # features = []
    # for i in range(5):
    #     df = np.sqrt(
    #         np.power(data[f"{hand}f{i}x"] - data[f"{hand}px"], 2) +
    #         # np.power(data[f"{hand}f{i}y"] - data[f"{hand}py"], 2) +
    #         np.power(data[f"{hand}f{i}z"] - data[f"{hand}pz"], 2)
    #     )

    #     features.append(df)

    # return resample(np.array(features).T, segment_length, axis=0)

    return resample(data.to_numpy(), segment_length, axis=0)
