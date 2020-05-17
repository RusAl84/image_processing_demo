import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.Qt import QFileDialog, QPixmap
import cv2
from eyeglasses_detection import face_detection, is_eye_exist
from open_or_close import is_eyes_opened
from blur import is_blured
from corelation import is_ratio_correct
from bright import is_too_bright, is_not_bright
from info_window import show_info


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.bright_value = str()
        self.correct_scale = str()
        self.path_2_image = str()
        self.is_eyes = str()
        self.is_eyeglasses = str()
        self.is_open = str()
        self.blured = str()

        self.blur_value = int()
        self.brightness_value = int()

        self.pixmap = QPixmap()
        self.pixmap_token = QPixmap()
        self.pixmap_logo = QPixmap()

        self.brightFlag = bool
        self.blurFlag = bool
        self.eyesFlag = bool
        self.eyes_openedFlag = bool
        self.scaleFlag = bool

        uic.loadUi('window.ui', self)
        self.pushButton.clicked.connect(self.browse_image)
        self.pushButton_2.clicked.connect(self.start_second_window)

    def start_second_window(self):
        self.open_second_window(self.path_2_image)

    def browse_image(self):
        self.textBrowser.clear()
        self.path_2_image = QFileDialog.getOpenFileName(self, 'Open File', './photo')[0]

        self.open_image_func()

    def open_second_window(self, path):
        show_info(path, self.blur_value, self.brightness_value)

    def open_image_func(self):
        self.open_image()

    def open_image(self):
        self.img = cv2.imread(self.path_2_image)
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.load_image()
        self.start(frame)

    def load_image(self):
        self.pixmap.load(self.path_2_image)
        pixmap = self.pixmap.scaled(461, 671)

        self.label.setPixmap(pixmap)

    def start(self, frame):
        flag, faces = face_detection(frame)
        self.eyeglasses_status(flag, faces, frame)
        self.is_blured()
        self.is_right_scale()
        self.is_bright()
        self.append_result()

    def eyeglasses_status(self, flag, faces, frame):
        if flag:
            self.eyesFlag = is_eye_exist(faces, frame)
            if self.eyesFlag:
                self.is_eyeglasses = '<font color="green">Нет</font>'
                self.is_eyes = '<font color="green">Видны</font>'
                self.close_open_eyes()
            else:
                self.is_eyeglasses = '<font color="green">Есть</font>'
                self.is_eyes = '<font color="red">Не видны</font>'
                self.is_open = '<font color="red">Не удалось определить</font>'

    def close_open_eyes(self):
        self.eyes_openedFlag = is_eyes_opened(self.img)
        if self.eyes_openedFlag:
            self.is_open = '<font color="green">Окрыты</font>'
        else:
            self.is_open = '<font color="red">Закрыты</font>'

    def is_blured(self):
        self.blurFlag, self.blur_value = is_blured(self.img)
        if self.blurFlag:
            self.blured = '<font color="red">Не соответствует</font>'
        else:
            self.blured = '<font color="green">Соответствует</font>'

    def is_right_scale(self):
        self.scaleFlag = is_ratio_correct(self.img)
        if self.scaleFlag:
            self.correct_scale = '<font color="green">Соответствует</font>'
        else:
            self.correct_scale = '<font color="red">Не соответсвует</font>'

    def is_bright(self):
        bright, light = is_too_bright(self.img)
        notbright, dark = is_not_bright(self.img)
        if bright:
            self.bright_value = '<font color="red">Избыток</font>'
            self.brightness_value = light
            self.brightFlag = False
        elif notbright:
            self.bright_value = '<font color="red">Недостаточно</font>'
            self.brightness_value = dark
            self.brightFlag = False
        else:
            self.bright_value = '<font color="green">Достаточно</font>'
            self.brightness_value = light
            self.brightFlag = True

    def access_token(self):
        green_token = './labels/green_gal.png'
        red_token = './labels/red_cross.png'

        if self.brightFlag and not self.blurFlag and self.eyesFlag and self.eyes_openedFlag and self.scaleFlag:
            self.pixmap_token.load(green_token)
            self.pixmap_token.scaled(191, 151)
            self.label_4.setPixmap(self.pixmap_token)
        else:
            self.pixmap_token.load(red_token)
            self.pixmap_token.scaled(191, 151)
            self.label_4.setPixmap(self.pixmap_token)

    def load_logo(self):
        self.pixmap_logo.load('./labels/unnamed.png')
        self.MyDocuments.setPixmap(self.pixmap_logo)


    def append_result(self):
        self.textBrowser.append(f'<h1>Наличие очков: {self.is_eyeglasses}</h1>'
                                f'<h1>Глаза: {self.is_eyes}</h1>'
                                f'<h1>Сотояние глаз: {self.is_open}'
                                f'<h1>Фон: {self.blured}</h1>'
                                f'<h1>Соотношение лица относительно фона: {self.correct_scale}</h1>'
                                f'<h1>Свет в изображении: {self.bright_value}</h1>')
        self.access_token()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("plastique")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())