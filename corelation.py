import cv2
import itertools
from collections import Counter
import numpy as np


lower_white = (240, 240, 240)
highest_white = (255, 255, 255)


def is_ratio_correct(img):
    white_ratio, black_ratio = get_color_ratio(img)
    if ((white_ratio > 50 and white_ratio < 52.3) or (white_ratio > 52.87 and white_ratio < 60) or (white_ratio > 90 and white_ratio < 110)):
        return True
    else:
        return False


def get_color_ratio(img):
    operated_image = cv2.inRange(img, lower_white, highest_white)
    cv2.imwrite('image1.png', operated_image)
    colors_on_image = list(itertools.chain.from_iterable(operated_image))

    list_of_black_and_white = Counter(colors_on_image)

    white = list_of_black_and_white[255]
    black = list_of_black_and_white[0]

    count = white + black

    black_ratio = white/count * 100
    white_ratio = 100 - black_ratio

    return white_ratio, black_ratio


def white_nd_black(path):
    img = cv2.imread(path)
    operated_image = cv2.inRange(img, lower_white, highest_white)
    cv2.imwrite('image1.png', operated_image)
    colors_on_image = list(itertools.chain.from_iterable(operated_image))

    list_of_black_and_white = Counter(colors_on_image)

    white = list_of_black_and_white[255]
    black = list_of_black_and_white[0]

    return white, black
