import numpy as np
import cv2
import os
import src.Funzioni as funzioni
import matplotlib.pyplot as plt

"""
FIle per effettura la rettificazione di due pair immagini

"""
# =======================================================================

Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'  # cartella dove salvare  i risultati delle matrici di rettificazione
Folder_to_save_rect = '/home/giuseppe/Scrivania/ResultRect' # cartella su cui salvare i risultati della rettificazione

# Nome delle due immagini da rettificare
nome_img_left = "/home/giuseppe/Scrivania/"
nome_img_right = "/home/giuseppe/Scrivania/"

# =======================================================================

im_left = cv2.imread(nome_img_left)
im_right = cv2.imread(nome_img_right)


# LETTURA DELLE MATRICI
mtx_left = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Sx.npy")
mtx_right = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Dx.npy")
dist_left = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Sx.npy")
dist_right = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Dx.npy")
R = funzioni.leggi_da_file_matrici(Folder_save_calib , "/R.npy")
T = funzioni.leggi_da_file_matrici(Folder_save_calib , "/T.npy")

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
   (640,480),
   R,T,
   R1,R2,P1,P2,
   Q,
   flags = cv2.CALIB_ZERO_DISPARITY)
#con il flag calib zero disparity facciamo in modo che i centri delle due telecamere coincidono tra loro --> cy1 == cy2
#questo dovrebbe grarantire che oggetti molto distanti tra loro hanno diparità zero.
#ricorda oggetti vicini hanno disparità alta oggetti lontani bassa


funzioni.Salva_su_file(Folder_to_save_rect, "/Matrice_R1.npy", R1)
funzioni.Salva_su_file(Folder_to_save_rect, "/Matrice_R2.npy", R2)
funzioni.Salva_su_file(Folder_to_save_rect, "/Matrice_P1.npy", P1)
funzioni.Salva_su_file(Folder_to_save_rect, "/Matrice_P2.npy", P2)


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

#TODO: migliorere l interfaccia il nome del file
cv2.imwrite('/home/giuseppe/Scrivania/ret_right2.png',im_right_remapped)
cv2.imwrite('/home/giuseppe/Scrivania/ret_left2.png',im_left_remapped)
