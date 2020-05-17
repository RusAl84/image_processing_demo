import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np
from pixels_info import PixelsInfo


def draw_graph(path):
    pix = PixelsInfo(path)
    pix.iterate_pixels()

    red = pix.get_red_pixs()
    green = pix.get_green_pixs()
    blue = pix.get_blue_pixs()
    colors = [red, green, blue]
    words_for_colors = ['red', 'green', 'blue']
    for n, pix in enumerate(colors):
        plt.figure(figsize=(16, 10), facecolor='black')
        sns_plot = sns.kdeplot(pix, color=words_for_colors[n], shade=True)
        plt.savefig(f'./graph{n}.png',
                    dpi=300,
                    format='png',
                    bbox_inches='tight')
        scale_graph_image(n)
        plt.close()


def scale_graph_image(n):
    size = 400, 200
    img = Image.open(f'./graph{n}.png')
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(f'./graph{n}.png', "PNG")


