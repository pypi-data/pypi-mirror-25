import io
import json

from .json_encoder import Frozen, PrettyJSONEncoder


class PixelsInfo(object):
    def __init__(self, indexes_to_colors, pixel_indexes):
        self.indexes_to_colors = indexes_to_colors
        self.pixel_indexes = pixel_indexes

    def to_json(self):
        colors_info_json = dict([(k, str(v)) for (k, v) in self.indexes_to_colors.items()])
        return {
            "color_scheme": colors_info_json,
            "pixel_map": [Frozen(row) for row in self.pixel_indexes]
        }

    def write_pixels_info(self, file: str):
        with io.open(file, 'w', encoding='utf8') as file:
            json_str = json.dumps(self.to_json(), indent=4, cls=PrettyJSONEncoder)
            file.write(json_str)
