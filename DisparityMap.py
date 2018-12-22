import numpy as np
import cv2

"""
Calcolo della disparity tra due immagini.
Successivamente la disparity calcolata viene salvata
"""

# === GESTIONE ===========================================================================

# nome delle immagini da prelevare per il calcolo della disparity
nome_left = '/home/giuseppe/Scrivania/ret_left2.png'
nome_right = '/home/giuseppe/Scrivania/ret_right2.png'

# nome della disparity da salvare
nome_disp = '/home/giuseppe/Scrivania/Disp2.png'

maxDisp = 128 # oggetti vicini alla camere
min_disp = 0 # oggetti distanti alla camera
block_size = 9 #dimansione della finestra che attraversa le immagini, deve essere dispari

# =====================================================================================


stereoProcessor = cv2.StereoSGBM_create(minDisparity=min_disp, numDisparities=maxDisp, blockSize=block_size)

# Load the left and right images in gray scale
imgLeft = cv2.imread(nome_left, 1)
imgRight = cv2.imread(nome_right, 1)

gray_left = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
gray_right = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

disparity = stereoProcessor.compute(gray_left, gray_right)
#filtro per il rumore
cv2.filterSpeckles(disparity, 0 , 4000, maxDisp)

#se la disparity è zero(oggetti distanti)  sparali
_, disparity = cv2.threshold(disparity, 0, maxDisp*16, cv2.THRESH_TOZERO)
disparity_scaled = (disparity /16).astype(np.uint8)
d = (disparity_scaled * (255. / maxDisp)).astype(np.uint8)
disparity = stereoProcessor.compute(imgLeft, imgRight)
cv2.filterSpeckles(disparity, 0, 4000, maxDisp)

_, disparity = cv2.threshold(disparity, 0, maxDisp * 16, cv2.THRESH_TOZERO)
disparity_scaled = (disparity / 16).astype(np.uint8)
d = (disparity_scaled * (255. / maxDisp)).astype(np.uint8)

cv2.imwrite(nome_disp, d)





