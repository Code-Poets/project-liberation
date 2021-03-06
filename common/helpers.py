import os
import random
from typing import List
from typing import Optional

import cv2
import numpy as np


def create_image(
    height: int,
    width: int,
    image_name: str,
    images_directory: str,
    rgb_color: Optional[List[int]] = None,
    return_relative_path: bool = False,
) -> str:
    tmp_dir = "tmp/"
    file_name = f"{image_name}.jpg"
    file_path = os.path.abspath(os.path.join(images_directory, tmp_dir, file_name))
    image = np.zeros((height, width, 3), np.uint8)
    if rgb_color is None:
        rgb_color = [0, 0, 0]
        for index, _ in enumerate(rgb_color):
            rgb_color[index] = random.randint(0, 255)
    # OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    image[:] = color
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    cv2.imwrite(file_path, image)
    if return_relative_path:
        return os.path.join(tmp_dir, file_name)
    return file_path
