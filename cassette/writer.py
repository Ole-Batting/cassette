from typing import Union

import cv2
import numpy as np
from PIL import Image

from cassette.config import Config


class VideoWriter:
    def __init__(self, path: str, config: Config):
        self.path = path
        self.config = config
        self.shape = config.em_shape
        self.writer = cv2.VideoWriter(
            path + config.format,
            cv2.VideoWriter.fourcc(*config.codec),
            config.fps,
            config.em_size,
        )

    def write(self, frame: Union[np.ndarray, Image.Image]):
        if isinstance(frame, Image.Image):
            frame = frame.convert("RGB")
            frame = np.array(frame)
        assert frame.shape[:2] == self.shape, f"{frame.shape[:2]=} and {self.shape=} must match"
        self.writer.write(frame)

    def release(self):
        self.writer.release()
