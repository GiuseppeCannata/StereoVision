import numpy as np
import cv2
import matplotlib.pyplot as plt

"""
Modulo per effettuare la rettificazione di due pair images
- Il modulo legge le matrici di calibrazioni ottenute con il modulo Ottieni_matrici_Rettificazione.py
"""

# =======================================================================

Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'  # cartella dove sono salvati i risultati delle matrici di rettificazione
Folder_save_rect = '/home/giuseppe/Scrivania/ResultRect' # cartella sono salvati i risultati della rettificazione

# Nome delle due immagini da rettificare
nome_img_left = "/home/giuseppe/Scrivania/_ "
nome_img_right = "/home/giuseppe/Scrivania/_ "

# Nome delle immagini da salvare
nome_img_left_ret = "/home/giuseppe/Scrivania/_ "
nome_img_right_ret = "/home/giuseppe/Scrivania/_ "

# =======================================================================

def leggi_da_file_matrici(folder, nome_file):
   mtx = np.load(folder + nome_file)
   return mtx

im_left = cv2.imread(nome_img_left)
im_right = cv2.imread(nome_img_right)

# LETTURA MATRICI CALIBRAZIONE
mtx_left = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Sx.npy")
mtx_right = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Dx.npy")
dist_left = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Sx.npy")
dist_right = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Dx.npy")

# LETTURA MATRICI RETTIFICAZIONE
R1 = leggi_da_file_matrici(Folder_save_rect , "/Matrice_R1.npy")
R2 = leggi_da_file_matrici(Folder_save_rect , "/Matrice_R2.npy")
P1 = leggi_da_file_matrici(Folder_save_rect , "/Matrice_P1.npy")
P2 = leggi_da_file_matrici(Folder_save_rect , "/Matrice_P2.npy")

# REMAP SULLO STESSO PIANO IMMAGINE PER LA VISUALIZZAZIONE
map1_x , map1_y = cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, (im_left.shape[1], im_left.shape[0]), cv2.CV_32FC1)
map2_x , map2_y = cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, (im_left.shape[1], im_left.shape[0]), cv2.CV_32FC1)

im_left_remapped = cv2.remap(im_left, map1_x, map1_y, cv2.INTER_CUBIC)
im_right_remapped = cv2.remap(im_right, map2_x, map2_y, cv2.INTER_CUBIC)

out = np.hstack((im_left_remapped, im_right_remapped))

for i in range(0,out.shape[0],30):
    cv2.line(out,(0,i),(out.shape[1],i),(0,255,255),3)

plt.figure(figsize=(10,4))
plt.imshow(out[...,::-1])
plt.show()

# Salvataggio immagini rettificate
cv2.imwrite(nome_img_left_ret ,im_right_remapped)
cv2.imwrite(nome_img_left_ret ,im_left_remapped)