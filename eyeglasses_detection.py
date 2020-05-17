import cv2

eye_cascPath = './haarcasde/haarcascade_eye_tree_eyeglasses.xml'  #eye detect model
face_cascPath = './haarcasde/haarcascade_frontalface_alt.xml'  #face detect model

faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)


def face_detection(frame):
    faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5,)

    if len(faces) > 0:
        return True, faces
    else:
        return False


def is_eye_exist(faces, frame):
    frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]

    eyes = eyeCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5,)

    if len(eyes) == 0:
        return False
    else:
        return True