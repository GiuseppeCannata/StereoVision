import cv2
from tkinter import *

def funz():

    cap = cv2.VideoCapture(0)

    while (True):
        # capture frame-by-frame
        _ , frame = cap.read()

        cv2.imshow('Preview', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # when everything done,release the capture
    cap.release()
    cv2.destroyAllWindows()