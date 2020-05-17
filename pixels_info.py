from PIL import Image


class PixelsInfo:
    def __init__(self, path):
        self.blue_pix_list = list()
        self.green_pix_list = list()
        self.red_pix_list = list()

        self.img = Image.open(path)
        self.height = self.img.size[1]
        self.width = self.img.size[0]

    def iterate_pixels(self):
        pix = self.img.load()
        for x in range(self.width):
            for y in range(self.height):
                red, green, blue = pix[x, y]
                self.red_pix_list.append(red)
                self.green_pix_list.append(green)
                self.blue_pix_list.append(blue)

    def get_red_pixs(self):
        return self.red_pix_list

    def get_green_pixs(self):
        return self.green_pix_list

    def get_blue_pixs(self):
        return self.blue_pix_list
