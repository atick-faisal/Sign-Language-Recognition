import numpy as np
import pandas as pd
from scipy.signal import resample
import config


def extract_flxion_features(
    data: pd.DataFrame,
    segment_length: int = 150,
    hand: str = "r"
) -> np.ndarray:
    data[f"d{hand}f0x"] = data[f"{hand}f0x"] - data[f"{hand}px"]
    data[f"d{hand}f0y"] = data[f"{hand}f0y"] - data[f"{hand}py"]
    data[f"d{hand}f0z"] = data[f"{hand}f0z"] - data[f"{hand}pz"]

    data[f"d{hand}f1x"] = data[f"{hand}f1x"] - data[f"{hand}px"]
    data[f"d{hand}f1y"] = data[f"{hand}f1y"] - data[f"{hand}py"]
    data[f"d{hand}f1z"] = data[f"{hand}f1z"] - data[f"{hand}pz"]

    data = data[config.DIST_FEATURES]

    # ... Min-Max scaling of distance features
    data = (data - config.SCALER_MIN) / config.SCALER_RANGE

    return resample(data.to_numpy(), segment_length, axis=0)
