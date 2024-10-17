import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def rgb_to_cmyk(rgb):
    red, green, blue = rgb
    black = 1 - max(red, green, blue)
    if black == 1:
        cyan = magenta = yellow = 0
    else:
        cyan = (1 - red - black) / (1 - black)
        magenta = (1 - green - black) / (1 - black)
        yellow = (1 - blue - black) / (1 - black)
    return cyan, magenta, yellow


def split_image_to_cmyk(image_path):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size

    c_channel = np.zeros((height, width), dtype=np.float32)
    m_channel = np.zeros((height, width), dtype=np.float32)
    y_channel = np.zeros((height, width), dtype=np.float32)

    for x in range(width):
        for y in range(height):
            rgb = image.getpixel((x, y))
            cyan, magenta, yellow = rgb_to_cmyk([r / 255.0 for r in rgb])
            c_channel[y, x] = cyan * 255
            m_channel[y, x] = magenta * 255
            y_channel[y, x] = yellow * 255

    return c_channel, m_channel, y_channel


def display_channels(cyan, magenta, yellow):
    plt.figure(figsize=(10, 8))

    plt.subplot(1, 3, 1)
    plt.title('Cyan Channel')
    plt.imshow(cyan, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('Magenta Channel')
    plt.imshow(magenta, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('Yellow Channel')
    plt.imshow(yellow, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


image_path = f"images/{os.getenv('IMAGE_NAME')}"
cyan, magenta, yellow = split_image_to_cmyk(image_path)
display_channels(cyan, magenta, yellow)
