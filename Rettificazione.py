import numpy as np
import cv2
import os
import matplotlib.pyplot as plt


def leggi_da_file_matrici(folder , nome_file):

    mtx = np.load(folder + nome_file)

    return mtx

# =======================================================================

path_folder = '/home/giuseppe/Scrivania'

Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'
#i = 1 # indice dell immagine destra e sinistra da considerare

# =======================================================================

im_left = cv2.imread(os.path.join(path_folder, "left/left%d.png"%1))
im_right = cv2.imread(os.path.join(path_folder, "right/right%d.png"%1))


# LETTURA DELLE MATRICI
mtx_left = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Sx.npy")
mtx_right = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Dx.npy")
dist_left = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Sx.npy")
dist_right = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Dx.npy")
R = leggi_da_file_matrici(Folder_save_calib , "/R.npy")
T = leggi_da_file_matrici(Folder_save_calib , "/T.npy")

# R1 --> output 3x3 matrix, rectification transform (rotation matrix) for the first camera
R1 = np.zeros((3,3))

# R2 --> Output 3x3 rectification transform (rotation matrix) for the second camera.
R2 = np.zeros((3,3))

# La vista di destra e di sinistra della telecamera stereo sono spostate l'una rispetto all'altra
# lungo l'asse x (e possono presentare un eventuale piccolo spostamento verticale, quindi lungo l asse y).
# Nelle immagini rettificate, le corrispondenti linee epipolari nelle fotocamere sinistra e destra
# sono orizzontali e hanno la stessa coordinata y. Per cui punti omologhi giacciono sulla stessa retta.
P1 = np.zeros((3,4))#output 3x4 matrix
P2 = np.zeros((3,4)) #output 3x4 matrix

Q = np.zeros((4,4)) #output 3x4 matrix


cv2.stereoRectify(
   mtx_left, #intrinsic parameters of the first camera
   dist_left,
   mtx_right,
   dist_right,
   (im_left.shape[1], im_right.shape[0]),
   R,T,
   R1,R2,P1,P2,
   Q,
   flags = cv2.CALIB_ZERO_DISPARITY) #last 4 parameters point to inizialized output variables


map1_x,map1_y=cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, (im_left.shape[1],im_left.shape[0]), cv2.CV_32FC1)
map2_x,map2_y=cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, (im_left.shape[1],im_left.shape[0]), cv2.CV_32FC1)

im_left_remapped=cv2.remap(im_left,map1_x,map1_y,cv2.INTER_CUBIC)
im_right_remapped=cv2.remap(im_right,map2_x,map2_y,cv2.INTER_CUBIC)

out=np.hstack((im_left_remapped,im_right_remapped))

for i in range(0,out.shape[0],30):
    cv2.line(out,(0,i),(out.shape[1],i),(0,255,255),3)

plt.figure(figsize=(10,4))
plt.imshow(out[...,::-1])
plt.show()


cv2.imwrite('/home/giuseppe/Scrivania/ret_right.png',im_right_remapped)
cv2.imwrite('/home/giuseppe/Scrivania/ret_left.png',im_left_remapped)
