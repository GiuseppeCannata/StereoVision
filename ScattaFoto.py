import cv2

cap = cv2.VideoCapture(0)

_, frame = cap.read()

imgLeft = frame[0:480, 0:640]
imgRight = frame[0:480, 641:1280]

cv2.imwrite('/home/giuseppe/Scrivania/Left.png', imgLeft)
cv2.imwrite('/home/giuseppe/Scrivania/Right.png', imgRight)



