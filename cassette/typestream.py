import argparse
import os

import cv2
import numpy as np
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from tqdm import tqdm

from cassette.config import load_config, Config
from cassette.utils import pad
from cassette.writer import VideoWriter


def cshi_image(code: str, output_file: str, cfg: Config) -> None:
    formatter = ImageFormatter(font_name=cfg.font_name, font_size=cfg.font_size, style=cfg.theme,
                               line_numbers=False)
    image_bytes = highlight(code, PythonLexer(), formatter)
    np_arr = np.asarray(bytearray(image_bytes), dtype="uint8")
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imwrite(f"{output_file}_{cfg.theme}.png", img_np)


def syntax_highlighted_image(code: str, cfg: Config) -> np.ndarray:
    formatter = ImageFormatter(font_name=cfg.font_name, font_size=cfg.font_size, style=cfg.theme,
                               line_numbers=False, image_pad=cfg.font_size, line_pad=cfg.font_size * 2 // 3)
    image_bytes = highlight(code, PythonLexer(), formatter)
    nparr = np.asarray(bytearray(image_bytes), dtype="uint8")
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np


def read_py_file(path: str) -> tuple[str, str, int]:
    with open(path, 'r') as py_file:
        py_str = py_file.read() + u'\xa0'
    lines = py_str.split("\n")
    lines_new = []
    start = 0
    n_chars = 0
    for l in lines[1:]:
        if "# !!" in l:
            cmd = l.split("# !!")[1]
            if cmd == "ignore":
                continue
            elif cmd == "start":
                start = n_chars
                continue
        else:
            n_chars += len(l) + 1
            lines_new.append(l)
    py_str = "\n".join(lines_new)
    return py_str, lines[0].replace("# !!", ""), start


class TypeStream:
    in_path: str
    out_path: str
    config: Config
    code_string: str
    render_mode: str
    render_mode_to_method: dict

    def __init__(self, in_path: str, out_folder: str, config_path: str):
        self.in_path = in_path
        self.out_folder = out_folder
        self.config = load_config(config_path)

        self.name = os.path.basename(self.in_path.replace('.', "_"))
        self.out_path = os.path.join(self.out_folder, self.name)
        print(self.out_path)

        self.code_string, self.render_mode, self.start_at = read_py_file(self.in_path)
        print(len(self.code_string), self.render_mode, self.start_at)
        self.render_mode_to_method = dict(
            image=self.final_frame,
            animate=self.animate,
        )

    def run(self):
        self.render_mode_to_method[self.render_mode]()

    def center(self, code):
        code = pad(code, self.config)
        return code

    def final_frame(self):
        code_image = syntax_highlighted_image(self.code_string, self.config)
        video_frame = self.center(code_image)
        cv2.imwrite(f"{self.out_path}.png", np.array(video_frame))

    def animate(self):
        videowriter = VideoWriter(self.out_path, self.config)

        for i in tqdm(range(self.start_at, len(self.code_string))):
            sub_string = self.code_string[:i]
            sub_lines = sub_string.split('\n')
            if all([s == ' ' for s in sub_lines[-1]]) and sub_lines[-1] != "":
                continue
            code_image = syntax_highlighted_image(sub_string + chr(9612), self.config)
            video_frame = self.center(code_image)
            videowriter.write(video_frame)
        videowriter.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-path", type=str, required=True, help="input file path")
    parser.add_argument("--out-path", type=str, required=True, help="output file path")
    parser.add_argument("--lq", dest="config", action="store_const",
                        const="cassette/configs/prototype.yaml", default="cassette/configs/production.yaml",
                        help="for quick prototyping")
    args = parser.parse_args()

    typestream = TypeStream(in_path=args.in_path, out_folder=args.out_path, config_path=args.config)
    typestream.run()
