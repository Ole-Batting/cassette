import cv2


class VideoWriter:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.writer = cv2.VideoWriter(
            f"videos/{name}{config.format}",
            cv2.VideoWriter.fourcc(*config.codec),
            config.fps,
            config.size,
        )

    def write(self, frame):
        assert frame.shape[:2] == self.config.shape, f"{frame.shape[:2]=} and {self.config.shape=} must match"
        self.writer.write(frame)

    def release(self):
        self.writer.release()
