import cv2

def funz():
    cap = cv2.VideoCapture(0)

    _ , frame = cap.read()

    imgLeft = frame[0:480, 0:640]
    imgRight = frame[0:480, 641:1280]

    return imgLeft , imgRight
