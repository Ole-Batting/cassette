import numpy as np
import yaml
from PIL import Image

from cassette.config import Config


def superimpose(img1: Image.Image, img2: Image.Image) -> Image.Image:
    out = img1.copy()
    h1 = (img1.height - img2.height) // 2
    w1 = (img1.width - img2.width) // 2
    out.paste(img2, (w1, h1))
    return out


def pad_width(img: np.ndarray, cfg: Config) -> np.ndarray:
    h, w = img.shape[:2]
    ew, eh = cfg.em_size
    if w < ew:
        out = (np.ones((h, ew, 3)) * img[0, 0]).astype(np.uint8)
        out[:h, :w] = img
        img = out
    return img


def pad_height(img, config):
    h, w = img.shape[:2]
    ew, eh = config.em_size
    if h < eh:
        out = (np.ones((eh, w, 3)) * img[0, 0]).astype(np.uint8)
        out[:h, :w] = img
        img = out
    elif h > eh:
        img = img[-eh:]
    return img


def pad(img, config):
    img = pad_width(img, config)
    img = pad_height(img, config)
    return img


def awgn(shape, scale):
    rnd = np.random.default_rng()
    return rnd.normal(0, scale, shape)
