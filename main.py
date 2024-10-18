import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def rgb_to_cmyk(rgb: tuple):
    red, green, blue = rgb
    black = 1 - max(red, green, blue)
    if black == 1:
        cian = magenta = yellow = 0
    else:
        cian = (1 - red - black) / (1 - black)
        magenta = (1 - green - black) / (1 - black)
        yellow = (1 - blue - black) / (1 - black)
    return cian, magenta, yellow


def split_image_to_cmyk(image_path: str):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size
    # Создаем массивы для каналов
    c_channel = np.zeros((height, width), dtype=np.float32)
    m_channel = np.zeros((height, width), dtype=np.float32)
    y_channel = np.zeros((height, width), dtype=np.float32)
    # Проходим по каждому пикселу и вычисляем значения CMYK
    for x in range(width):
        for y in range(height):
            rgb = image.getpixel((x, y))
            cian, magenta, yellow = rgb_to_cmyk([r / 255.0 for r in rgb])
            c_channel[y, x] = cian * 255
            m_channel[y, x] = magenta * 255
            y_channel[y, x] = yellow * 255

    return c_channel, m_channel, y_channel


def display_channel(index: int, title: str, array: np.ndarray):
    plt.subplot(1, 3, index)
    plt.title(title)
    plt.imshow(array, cmap="gray")
    plt.axis("off")


def display_channels(cian: np.ndarray, magenta: np.ndarray, yellow: np.ndarray):
    plt.figure(figsize=(10, 8))

    display_channel(1, "Cian Channel", cian)
    display_channel(2, "Magenta Channel", magenta)
    display_channel(3, "Yellow Channel", yellow)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    image_path = f"images/{os.getenv('IMAGE_NAME')}"
    cian, magenta, yellow = split_image_to_cmyk(image_path)
    display_channels(cian, magenta, yellow)
