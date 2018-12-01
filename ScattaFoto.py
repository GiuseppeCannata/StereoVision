import cv2

"""
Effettua uno scatto

"""

# ==========================================

#Assegnare i nomi che si vogliono dare alle immagini
nome_left = '/home/giuseppe/Scrivania/Left.png'
nome_right = '/home/giuseppe/Scrivania/Right.png'

# ==========================================
cap = cv2.VideoCapture(0)

_, frame = cap.read()

imgLeft = frame[0:480, 0:640]
imgRight = frame[0:480, 641:1280]

cv2.imwrite(nome_left, imgLeft)
cv2.imwrite(nome_right, imgRight)



