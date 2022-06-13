import cv2
import numpy as np
import pandas as pd

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .normalize import normalize
from .filters import LowPassFilter


def get_projection_image(
    data: pd.DataFrame,
    img_len: int
) -> np.ndarray:

    rpx = LowPassFilter.apply(data["rpx"].to_numpy())
    rpy = LowPassFilter.apply(data["rpy"].to_numpy())
    rpz = LowPassFilter.apply(data["rpz"].to_numpy())

    rf0x = LowPassFilter.apply(data["rf0x"].to_numpy())
    rf0y = LowPassFilter.apply(data["rf0y"].to_numpy())
    rf0z = LowPassFilter.apply(data["rf0z"].to_numpy())

    rf1x = LowPassFilter.apply(data["rf1x"].to_numpy())
    rf1y = LowPassFilter.apply(data["rf1y"].to_numpy())
    rf1z = LowPassFilter.apply(data["rf1z"].to_numpy())

    rpx = (normalize(rpx) * (img_len - 1)).astype("uint8")
    rpy = (normalize(rpy) * (img_len - 1)).astype("uint8")
    rpz = (normalize(rpz) * (img_len - 1)).astype("uint8")

    rf0x = (normalize(rf0x) * (img_len - 1)).astype("uint8")
    rf0y = (normalize(rf0y) * (img_len - 1)).astype("uint8")
    rf0z = (normalize(rf0z) * (img_len - 1)).astype("uint8")

    rf1x = (normalize(rf1x) * (img_len - 1)).astype("uint8")
    rf1y = (normalize(rf1y) * (img_len - 1)).astype("uint8")
    rf1z = (normalize(rf1z) * (img_len - 1)).astype("uint8")

    # img = np.zeros((img_len * 3 - 1, img_len * 3 - 1), dtype="uint8")

    # img[rpx, rpy] = 255
    # img[rpy + int(img_len), rpz] = 255
    # img[rpz + int(img_len * 2 - 1), rpx] = 255

    # img[rf0x, rf0y + int(img_len)] = 255
    # img[rf0y + int(img_len), rf0z + int(img_len)] = 255
    # img[rf0z + int(img_len * 2 - 1), rf0x + int(img_len)] = 255

    # img[rf1x, rf1y + int(img_len * 2 - 1)] = 255
    # img[rf1y + int(img_len), rf1z + int(img_len * 2 - 1)] = 255
    # img[rf1z + int(img_len * 2 - 1), rf1x + int(img_len * 2 - 1)] = 255

    # img = cv2.GaussianBlur(img, (5, 5), 0)

    fig = Figure(figsize=(2.24, 2.24))

    width, height = fig.get_size_inches() * fig.get_dpi()
    canvas = FigureCanvas(fig)
    ax = fig.gca()

    ax.plot(rpz[10:], rpx[10:], "-k", linewidth=3)
    ax.axis('off')
    fig.tight_layout()

    canvas.draw()       # draw the canvas, cache the renderer

    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')

    return image.reshape(int(height), int(width), 3)
