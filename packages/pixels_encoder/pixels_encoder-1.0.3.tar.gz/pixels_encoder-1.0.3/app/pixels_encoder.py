import numpy as np
from PIL import Image

from .helpers import *
from .pixels_info import PixelsInfo
from .color import Color


class PixelsEncoder(object):
    def __init__(self, img_path: str):
        self.image = Image.open(img_path)

    def extract_info(self):
        indexes_to_colors = _unique_colors_map(self.image)
        pixel_indexes = _indexed_pixels(self.image, indexes_to_colors)
        return PixelsInfo(indexes_to_colors, pixel_indexes)

    def encode_pixels_info(self, file: str):
        self.extract_info().write_pixels_info(file)


def _indexed_pixels(image, indexes_to_colors: dict):
    def pixel_index(p):
        color = Color.with_full_format_tuple(p[0:3])
        return get([i for i, c in indexes_to_colors.items() if c == color], 0, default=-1)

    pixels = _image_pixels(image)
    pixels = list(map(lambda row: list(map(pixel_index, row)), pixels))
    return pixels


def _image_pixels(image):
    return np.asarray(_rgba_image(image)).tolist()


def _image_pixels_list(image):
    return list(_rgba_image(image).getdata())


def _unique_colors_map(image):
    pixels = _image_pixels_list(image)
    colors_map = {}
    for p in pixels:
        color = Color.with_full_format_tuple(p[0:3])
        if p[3] > 0 and color not in colors_map.values():
            colors_map[len(colors_map)] = color
    return colors_map


def _rgba_image(image):
    return image.convert('RGBA')
