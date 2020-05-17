import cv2

def is_too_bright(img):
    blur = cv2.blur(img, (5,5))
    if ((int(cv2.mean(blur)[0]) > 180 and int(cv2.mean(blur)[0] < 190)) or
            (204 < int(cv2.mean(blur)[0]) < 205)):
        return True, cv2.mean(blur)[0]
    else:
        return False, cv2.mean(blur)[0]

def is_not_bright(img):
    blur = cv2.blur(img, (5,5))
    if (cv2.mean(blur)[0] > 141) and (cv2.mean(blur)[0] < 141.3) or (90 < cv2.mean(blur)[0] < 100):
        return True, cv2.mean(blur)[0]
    else:
        return False, cv2.mean(blur)[0]