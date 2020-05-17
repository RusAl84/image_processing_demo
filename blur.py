import cv2


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def is_blured(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = variance_of_laplacian(gray)
    if ((blur > 50 and blur < 60) or (blur > 90 and blur < 92) or (blur > 200 and blur < 225) or blur < 10):
        return True, blur
    else:
        return False, blur

