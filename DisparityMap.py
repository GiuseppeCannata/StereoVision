import numpy as np
import cv2
from matplotlib import pyplot as plt



def Salva_su_file(folder, nome_file, elemento_da_salvare):
    np.save(folder + nome_file, elemento_da_salvare)

# !!!!!!!
maxDisp = 128
stereoProcessor = cv2.StereoSGBM_create(minDisparity=0, numDisparities=maxDisp, blockSize=9)

# Load the left and right images in gray scale
imgLeft = cv2.imread('/home/giuseppe/Scrivania/ret_left2.png', 1)
imgRight = cv2.imread('/home/giuseppe/Scrivania/ret_right2.png', 1)

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

cv2.imwrite('/home/giuseppe/Scrivania/Disp2.png',d)

Folder = '/home/giuseppe/Scrivania'
Salva_su_file(Folder, "/Matrice_disp2.npy", d)




"""

# Normalize the image for representation !!!!!
#http://www.dmi.unict.it/fstanco/Multimedia/FS%20Lez%205%20-%20filtraggio%20nel%20dominio%20spaziale.pdf alla sezione normalizzazione

min = disparity.min()
max = disparity.max()
disparity = np.uint8(255 * (disparity - min) / (max - min))
disparity = disparity/16.0


cont = 0
for i in range(110,310):
    for j in range(350,550):
         cont = cont + disparity[i,j]
        
z = cont / ((550-350)*(310-110))
depth = (65 * 1.6 )/ z
print(depth)

img = np.zeros((3,3))
Q = np.load('/home/giuseppe/Scrivania/ResultCalib/Q.npy')
cv2.reprojectImageTo3D(disparity,Q, img)

plt.imshow(M1,'gray')
plt.show()

#depth = (65 * 3.6 )/ ((disparity[215,340] * 10) / 37.796)

#print(depth)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
"""
#*******************************************
#***** Parameters for the StereoVision *****
#*******************************************

# Create StereoSGBM and prepare all parameters
window_size = 3
min_disp = 2
num_disp = 130-min_disp
stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
    numDisparities = num_disp,
    blockSize = window_size,
    uniquenessRatio = 10,
    speckleWindowSize = 100,
    speckleRange = 32,
    disp12MaxDiff = 5,
    P1 = 8*3*window_size**2,
    P2 = 32*3*window_size**2)

# Used for the filtered image
stereoR=cv2.ximgproc.createRightMatcher(stereo) # Create another stereo for right this time

# WLS FILTER Parameters
lmbda = 80000
sigma = 1.8
visual_multiplier = 1.0

wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
wls_filter.setLambda(lmbda)
wls_filter.setSigmaColor(sigma)
"""

