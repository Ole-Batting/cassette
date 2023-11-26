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
    theme: str = 'github-dark'

    @property
    def shape(self):
        w, h = self.size
        return h, w

    @property
    def half_size(self):
        w, h = self.size
        return w // 2, h // 2

    @property
    def fontpx(self):
        return f"{self.font_size}px"


def load_config(path):
    with open(path, 'r') as config_file:
        config_dict = yaml.safe_load(config_file)
        config = Config(**config_dict)
    return config

