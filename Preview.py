import cv2

"""
Modulo per effettuare la preview della camera
"""

cap = cv2.VideoCapture(0)

while (True):
    # capture frame-by-frame
    _ , frame = cap.read()
    img_laser_L = frame[0:480, 0:640]
    img_laser_R = frame[0:480, 641:1280]

    cv2.imshow('PreviewR', img_laser_R)
    cv2.imshow('PreviewL', img_laser_L)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything done,release the capture
cap.release()
cv2.destroyAllWindows()