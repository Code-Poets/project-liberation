import argparse
import os
from typing import Optional
from typing import Tuple

import cv2
from numpy.core.multiarray import ndarray


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Image resizer.")
    parser.add_argument("--image-path", type=str)
    parser.add_argument("--new-resolution", type=str)
    return parser.parse_args()


def get_file_paths(image_path: str) -> Tuple[str, str, str, str]:
    file_path = os.path.join(os.getcwd(), image_path)
    file_directory = os.path.dirname(file_path)
    file = os.path.basename(file_path)
    file_name, image_extension = file.split(".")
    return (file_path, file_directory, file_name, image_extension)


def image_resize(image: ndarray, width: int, height: int, inter: Optional[int] = cv2.INTER_AREA) -> ndarray:
    (image_height, image_width) = image.shape[:2]
    image_ratio = float(image_height) / float(image_width)
    new_height = round(width * image_ratio)
    if new_height >= height:
        dimension = (width, new_height)
    else:
        new_width = round(height / image_ratio)
        dimension = (new_width, height)

    resized = cv2.resize(image, dimension, interpolation=inter)

    return resized


def resize_and_store_image(
    file_path: str, file_directory: str, file_name: str, image_extension: str, resolution: str
) -> None:
    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    (x, y) = resolution.split("x")
    resized_image = image_resize(image, width=int(x), height=int(y))
    (image_height, image_width) = resized_image.shape[:2]
    new_image_path = os.path.join(file_directory, f"{file_name}_{image_width}x{image_height}.{image_extension}")
    assert image_width >= int(x)
    assert image_height >= int(y)
    cv2.imwrite(new_image_path, resized_image)
    print(f'Image: "{file_name}.{image_extension}" has been successfully resized and stored in {new_image_path}.')


def main() -> None:
    arguments = parse_arguments()
    (file_path, file_directory, file_name, image_extension) = get_file_paths(arguments.image_path)
    resize_and_store_image(file_path, file_directory, file_name, image_extension, arguments.new_resolution)


if __name__ == "__main__":
    main()
