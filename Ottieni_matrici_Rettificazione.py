import numpy as np
import cv2


"""
Modulo per ottenere le matrici di rettificazione
"""

# === GESTIONE ============================================================

Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'  # cartella dove sono salvati i risultati delle matrici di rettificazione
Folder_to_save_rect = '/home/giuseppe/Scrivania/ResultRect' # cartella su cui salvare i risultati della rettificazione

# Nome delle due immagini da rettificare
nome_img_left = "/home/giuseppe/Scrivania/_ "
nome_img_right = "/home/giuseppe/Scrivania/_ "

# =======================================================================

def leggi_da_file_matrici(folder, nome_file):
   mtx = np.load(folder + nome_file)
   return mtx


def Salva_su_file(folder, nome_file, elemento_da_salvare):
   np.save(folder + nome_file, elemento_da_salvare)


im_left = cv2.imread(nome_img_left)
im_right = cv2.imread(nome_img_right)

# LETTURA MATRICI CALIBRAZIONE
mtx_left = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Sx.npy")
mtx_right = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Dx.npy")
dist_left = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Sx.npy")
dist_right = leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Dx.npy")
R = leggi_da_file_matrici(Folder_save_calib , "/R.npy")
T = leggi_da_file_matrici(Folder_save_calib , "/T.npy")


# GENERAZIONE MATRICI RETTIFICAZIONE
R1 = np.zeros((3,3)) # R1 --> output 3x3 matrix, rectification transform (rotation matrix) for the first camera
R2 = np.zeros((3,3)) # R2 --> Output 3x3 rectification transform (rotation matrix) for the second camera.

# La vista di destra e di sinistra della telecamera stereo sono spostate l'una rispetto all'altra
# lungo l'asse x (e possono presentare un eventuale piccolo spostamento verticale, quindi lungo l asse y).
# Nelle immagini rettificate, le corrispondenti linee epipolari nelle fotocamere sinistra e destra
# sono orizzontali e hanno la stessa coordinata y. Per cui punti omologhi giacciono sulla stessa retta.
P1 = np.zeros((3,4))#output 3x4 matrix
P2 = np.zeros((3,4)) #output 3x4 matrix
Q = np.zeros((4,4)) #output 3x4 matrix

cv2.stereoRectify( mtx_left, dist_left, mtx_right, dist_right, (640,480), R, T, R1, R2, P1, P2, Q, flags = cv2.CALIB_ZERO_DISPARITY)
#con il flag calib zero disparity facciamo in modo che i centri delle due telecamere coincidono tra loro --> cy1 == cy2
#questo dovrebbe grarantire che oggetti molto distanti tra loro hanno diparità zero.
#ricorda oggetti vicini hanno disparità alta oggetti lontani bassa

# SALVATAGGIO MATRICI PER RETTIFICAZIONE
Salva_su_file(Folder_to_save_rect, "/Matrice_R1.npy", R1)
Salva_su_file(Folder_to_save_rect, "/Matrice_R2.npy", R2)
Salva_su_file(Folder_to_save_rect, "/Matrice_P1.npy", P1)
Salva_su_file(Folder_to_save_rect, "/Matrice_P2.npy", P2)



