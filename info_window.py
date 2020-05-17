import PySimpleGUI as sg
from PIL import Image
from corelation import white_nd_black
import cv2
from graph_for_color import draw_graph


def scale_tree_image(path_to_image):
    size = 276, 360
    img = Image.open(path_to_image)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save('./needed_image.png', "PNG")
    return img


def get_sizes_of_image(path_to_image):
    img = Image.open(path_to_image)
    width, height = img.size
    return width, height


def masking_picture(path):
    img = cv2.imread(path)
    lower_white = (240, 240, 240)

    highest_white = (255, 255, 255)
    operated_img = cv2.inRange(img, lower_white, highest_white)
    cv2.imwrite('image1.png', operated_img)
    size = 276, 360
    img = Image.open('image1.png')
    img.thumbnail(size, Image.ANTIALIAS)
    img.save('./image1.png', "PNG")


def show_info(path_to_image, blur_value, brightness_value):
    draw_graph(path_to_image)

    white, black = white_nd_black(path_to_image)
    scale_tree_image(path_to_image)
    width, height = get_sizes_of_image(path_to_image)

    resolution = 'Разрешение загруженной фотографии: ' + str(width) + ' x ' + str(height)
    ratio_of_black_and_white = f'Количество белых и черных пикселей: {white} x {black}'

    white_percent = round(white / (white + black), 2) * 100
    black_percent = 100 - white_percent

    masking_picture(path_to_image)
    frame_with_images = [
        [sg.Image('./needed_image.png'), sg.Image('./image1.png')],
        [sg.Text('Информация о фотографии')],
        [sg.Text(text=resolution)],
        [sg.Text(text=ratio_of_black_and_white)]
    ]

    frame_with_text_for_bars = [
        [sg.Text(f'отношение черного и белого = {black_percent}% {white_percent}%'),
         sg.ProgressBar(max_value=100, orientation='h', size=(20, 20), bar_color=('black', 'white'),
                        key='progress_black_white')],
        [sg.Text(f'коэффициент яркости = {int(brightness_value)}')],
        [sg.Text(f'коэффициент размытия = {int(blur_value)}')]
    ]
    frame_with_graphs = [

        [sg.Image('./graph0.png'),
         sg.Image('./graph1.png')],
        [sg.Image('./graph2.png')],
        [sg.Frame('Значения', layout=frame_with_text_for_bars)]
    ]
    final_layout = [
        [sg.Frame(title='Информация об изобажении', layout=frame_with_images),
         sg.Frame(title='Графики цвета', layout=frame_with_graphs)],
        [sg.Exit('Выйти в главное меню')]
    ]
    window = sg.Window('Дополнительная информация').Layout(final_layout)
    progress_black_white = window['progress_black_white']

    while True:
        event, values = window.read(timeout=0)
        progress_black_white.UpdateBar(int(black_percent))
        if event is None or event == 'Выйти в главное меню':
            window.Close()
            break

