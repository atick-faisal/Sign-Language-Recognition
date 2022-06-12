import numpy as np
import pandas as pd

from .normalize import normalize


def get_projection_image(
    data: pd.DataFrame,
    img_len: int
) -> np.ndarray:

    rpx = data["rpx"].to_numpy()
    rpy = data["rpy"].to_numpy()
    rpz = data["rpz"].to_numpy()

    rf0x = data["rf0x"].to_numpy()
    rf0y = data["rf0y"].to_numpy()
    rf0z = data["rf0z"].to_numpy()

    rf1x = data["rf1x"].to_numpy()
    rf1y = data["rf1y"].to_numpy()
    rf1z = data["rf1z"].to_numpy()

    rpx = (normalize(rpx) * (img_len - 1)).astype("uint8")
    rpy = (normalize(rpy) * (img_len - 1)).astype("uint8")
    rpz = (normalize(rpz) * (img_len - 1)).astype("uint8")

    rf0x = (normalize(rf0x) * (img_len - 1)).astype("uint8")
    rf0y = (normalize(rf0y) * (img_len - 1)).astype("uint8")
    rf0z = (normalize(rf0z) * (img_len - 1)).astype("uint8")

    rf1x = (normalize(rf1x) * (img_len - 1)).astype("uint8")
    rf1y = (normalize(rf1y) * (img_len - 1)).astype("uint8")
    rf1z = (normalize(rf1z) * (img_len - 1)).astype("uint8")

    img = np.zeros((img_len * 3 - 1, img_len * 3 - 1), dtype="uint8")

    img[rpx, rpy] = 1
    img[rpy + int(img_len), rpz] = 1
    img[rpz + int(img_len * 2 - 1), rpx] = 1

    img[rf0x, rf0y + int(img_len)] = 1
    img[rf0y + int(img_len), rf0z + int(img_len)] = 1
    img[rf0z + int(img_len * 2 - 1), rf0x + int(img_len)] = 1

    img[rf1x, rf1y + int(img_len * 2 - 1)] = 1
    img[rf1y + int(img_len), rf1z + int(img_len * 2 - 1)] = 1
    img[rf1z + int(img_len * 2 - 1), rf1x + int(img_len * 2 - 1)] = 1

    return img
