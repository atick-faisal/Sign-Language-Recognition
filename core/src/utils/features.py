import numpy as np
import pandas as pd
from scipy.signal import resample


def extract_flxion_features(
    data: pd.DataFrame,
    segment_length: int = 150,
    hand: str = "r"
) -> np.ndarray:
    features = []
    for i in range(5):
        df = np.sqrt(
            np.power(data[f"{hand}f{i}x"] - data[f"{hand}px"], 2) +
            np.power(data[f"{hand}f{i}y"] - data[f"{hand}py"], 2) +
            np.power(data[f"{hand}f{i}z"] - data[f"{hand}pz"], 2)
        )

        features.append(df)

    return resample(np.array(features).T, segment_length, axis=0)
