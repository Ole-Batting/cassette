from dataclasses import dataclass

import yaml


@dataclass
class Config:
    codec: str = "avc1"
    format: str = ".mp4"
    fps: int = 60
    size: tuple[int, int] = (3840, 2160)
    font_name: str = 'Menlo'
    font_size: int = 14
    theme: str = 'native'
    em_width: int = 80
    em_height: int = 10

    @property
    def shape(self):
        w, h = self.size
        return h, w

    @property
    def em_size(self):
        return self.em_width * self.font_size, self.em_height * self.font_size


def load_config(path):
    with open(path, 'r') as config_file:
        config_dict = yaml.safe_load(config_file)
        config = Config(**config_dict)
    return config

