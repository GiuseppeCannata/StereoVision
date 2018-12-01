import cv2
"""
File per effettuare la preview della camera

"""
cap = cv2.VideoCapture(1)

while(True):

    _, frame = cap.read()
    cv2.imshow('Frame',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
