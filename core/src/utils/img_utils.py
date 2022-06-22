import cv2
import math
import numpy as np


def create_img_grid(
    images: list[np.ndarray],
    img_grid_size: int = 224,
    rgb_image: bool = True
) -> np.ndarray:
    n_images = len(images)
    grid_len = math.isqrt(n_images)
    img_size = math.floor(img_grid_size / grid_len)
    img_shape = (img_grid_size, img_grid_size, 3) if rgb_image else (
        img_grid_size, img_grid_size, 1)
    img = np.zeros(img_shape, dtype="uint8")

    counter = 0
    for i in range(grid_len):
        for j in range(grid_len):
            row_strat = i * img_size
            row_end = row_strat + img_size
            col_strat = j * img_size
            col_end = col_strat + img_size
            _img = images[counter]

            if _img.shape[0] != img_size:
                _img = cv2.resize(_img, (img_size, img_size))

            img[row_strat:row_end, col_strat:col_end, :] = _img
            counter = counter + 1

    return img


