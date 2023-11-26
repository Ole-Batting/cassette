import cv2
import numpy as np
from cairosvg import svg2png
from html2image import Html2Image
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter, SvgFormatter, ImageFormatter

from cassette.config import load_config


def cshi_html(code, output_file, config):
    formatter = HtmlFormatter(font_name=config.font_name, font_size=config.font_size//2, style=config.theme, full=True)
    html_str = highlight(code, PythonLexer(), formatter)
    hti = Html2Image()
    hti.screenshot(html_str=html_str, save_as=f"{output_file}_html.png", size=config.half_size)


def cshi_svg(code, output_file, config):
    formatter = SvgFormatter(fontfamily=config.font_name, fontsize=config.fontpx, style=config.theme, full=True)
    svg_str = highlight(code, PythonLexer(), formatter)
    svg2png(svg_str, parent_width=config.size[0], parent_height=config.size[1], write_to=f"{output_file}_svg.png",
            output_width=config.size[0], output_height=config.size[1])


def cshi_image(code, output_file, config):
    formatter = ImageFormatter(font_name=config.font_name, font_size=config.font_size, style=config.theme,
                               line_numbers=False)
    image_bytes = highlight(code, PythonLexer(), formatter)
    nparr = np.asarray(bytearray(image_bytes), dtype="uint8")
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite(f"{output_file}_image.png", img_np)





if __name__ == "__main__":
    # Example usage
    python_code = """
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

    """
    from pygments.styles import get_all_styles
    print(list(get_all_styles()))

    config = load_config("configs/prototype.yaml")

    cshi_image(python_code, 'highlighted_code', config)

    # import timeit
    # n = 20
    #
    # res = timeit.timeit(
    #     stmt="func(python_code, 'highlighted_code', config)",
    #     globals=dict(func=cshi_html, python_code=python_code, config=config),
    #     number=n,
    # )
    # print(res / n)
    #
    # res = timeit.timeit(
    #     stmt="func(python_code, 'highlighted_code', config)",
    #     globals=dict(func=cshi_svg, python_code=python_code, config=config),
    #     number=n,
    # )
    # print(res / n)
    #
    # res = timeit.timeit(
    #     stmt="func(python_code, 'highlighted_code', config)",
    #     globals=dict(func=cshi_image, python_code=python_code, config=config),
    #     number=n,
    # )
    # print(res / n)
