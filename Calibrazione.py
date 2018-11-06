import numpy as np
import cv2
import os
import matplotlib.pyplot as plt


# ==========================================================================

# percorso della cartella immagini, ci devono essere almeno 10 immagin
pathLeft = '/home/giuseppe/Scrivania/left'
pathRight = '/home/giuseppe/Scrivania/right'

Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'   # path della cartella dove verranno salvati i file di calibrazione

nCol = 9  # number of rows of chessboard -1
nRow = 6  # number of columns of chessboard -1
dimSquare = 25  # dimensione del quadrato della scacchiera

# ==========================================================================

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimSquare, 0.001)

# Per ogni punto 2D abbiamo necessità di definire i corrispettivi punti 3D.
# Il sistema di riferimento 3D che consideriamo è quello di avere X e Y che si intersecano nel corner mentre Z = 0.
# Questo significa che idealmente la scacchiera si sposterà l ungo l assi x e y
objp = np.zeros((nCol*nRow,3), np.float32)
objp[:,:2] = np.mgrid[0:nCol,0:nRow].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
all_3D_objpoints = [] # 3d point in real world space

# 2D point of left and right images
all_left_corners = []
all_right_corners = []

idx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]   # minimo 10 foto per la calibrazione

for i in idx:

    # acquire the images
    imgLeft = cv2.imread(os.path.join(pathLeft, "left%d.png"%i))
    imgRight = cv2.imread(os.path.join(pathRight, "right%d.png"%i))

    # conversion in to gray scale
    grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

    # Cerchiamo all interno delle immagini il pattern della scacchiera.
    # ret     --> restituisce un boolenano (True, False) se il pattern è stato o meno trovato all interno dell immagine
    # corners --> restituisce un array di array contenente i punti 2D , in coordinate pixel, dei corner della scacchiera trovata
    #             avendo una schacchiera 9x6 avremo 54 vettori di dimensione 1x2 --> [ coordin. x   coordinata y ]
    ret_left , left_corners = cv2.findChessboardCorners(grayLeft, (nCol, nRow))
    ret_right, right_corners = cv2.findChessboardCorners(grayRight, (nCol, nRow))

    # Se il pattern è stato trovato li aggiungiamo all array totale
    if ret_left and ret_right:

        all_left_corners.append(cv2.cornerSubPix(grayLeft, left_corners, (11, 11), (-1, -1), criteria))
        all_right_corners.append(cv2.cornerSubPix(grayRight, right_corners, (11, 11), (-1, -1), criteria))
        all_3D_objpoints.append(objp) #i punti 3D saranno sempre quelli

imgLeft = cv2.imread(os.path.join(pathLeft, "left1.png"))
imgRight = cv2.imread(os.path.join(pathRight, "right1.png"))

# conversion in to gray scale
grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

# Calcolo i parametri intrinseci ed estrinsecio della camera sia di destra sia di sinistra:
#                mtx   --> matrice dei parametri intrinseci
#                dist  --> matrice di distrosione
#                rvecs --> matrice di rotazione
#                tvecs --> matrice di traslazione
#
e1, mtx_left, dist_left, rvecs_left, tvecs_left = cv2.calibrateCamera(all_3D_objpoints, all_left_corners, (grayLeft.shape[1],grayLeft.shape[0]), None, None)
e2, mtx_right, dist_right, rvecs_right, tvecs_right = cv2.calibrateCamera(all_3D_objpoints, all_right_corners, (grayRight.shape[1],grayRight.shape[0]), None, None)

# Calibrazione Stereo camera
retval, _, _, _, _, R, T, E, F = cv2.stereoCalibrate( all_3D_objpoints,
                                                      all_left_corners,
                                                      all_right_corners,
                                                      mtx_left,
                                                      dist_left,
                                                      mtx_right,
                                                      dist_right,
                                                      (grayLeft.shape[1],grayLeft.shape[0]),
                                                      None,
                                                      None,
                                                      None,
                                                      None,
                                                      flags=cv2.CALIB_FIX_INTRINSIC, # mi concentro sulle matrici intrinseche
                                                      criteria= criteria)



def Salva_su_file(folder, nome_file, elemento_da_salvare):

    np.save(folder+ nome_file, elemento_da_salvare)


# ======================== Salvataggio matrici di calibrazione =======================

Salva_su_file(Folder_save_calib , "/Matrice_Intrinseca_Dx.npy", mtx_right)
Salva_su_file(Folder_save_calib , "/Matrice_Intrinseca_Sx.npy", mtx_left)
Salva_su_file(Folder_save_calib , "/Matrice_Distorsione_Dx.npy", dist_right)
Salva_su_file(Folder_save_calib , "/Matrice_Distorsione_Sx.npy", dist_left)

# =====================================================================================


# ======================== Salvataggio delle Stereocalibrazione =======================

Salva_su_file(Folder_save_calib , "/R.npy", R)
Salva_su_file(Folder_save_calib , "/T.npy", T)
Salva_su_file(Folder_save_calib , "/E.npy", E)
Salva_su_file(Folder_save_calib , "/F.npy", F)

# ====================================================================================



"""


# ----------------- rettificazione ---------------

def drawLine(line, image):
    a = line[0]
    b = line[1]
    c = line[2]

    # ax+by+c -> y=(-ax-c)/b
    # define an inline function to compute the explicit relationship
    def y(x): return (-a * x - c) / b

    x0 = 0  # starting x point equal to zero
    x1 = image.shape[1]  # ending x point equal to the last column of the image

    y0 = y(x0)  # corresponding y points
    y1 = y(x1)

    # draw the line
    cv2.line(image, (x0, int(y0)), (x1, int(y1)), (0, 255, 255), 3)  # draw the image in yellow with line_width=3

i=1
left_im = cv2.imread(os.path.join(pathLeft, "left%d.png"%i))
right_im = cv2.imread(os.path.join(pathRight, "right%d.png"%i))

print(mtx_left)
print(mtx_right)
print(dist_right)
print(R)
print(T)
print(dist_left)

left_corners = all_left_corners[i].reshape(-1,2)
right_corners = all_right_corners[i].reshape(-1,2)

cv2.circle(left_im,(left_corners[0,0],left_corners[0,1]),10,(0,0,255),10)
cv2.circle(right_im,(right_corners[0,0],right_corners[0,1]),10,(0,0,255),10)

lines_right = cv2.computeCorrespondEpilines(all_left_corners[i], 1,F)
lines_right = lines_right.reshape(-1,3) #reshape for convenience
drawLine(lines_right[0],right_im)

lines_left = cv2.computeCorrespondEpilines(all_right_corners[i], 2,F)
lines_left=lines_left.reshape(-1,3)
drawLine(lines_left[0],left_im)


R1=np.zeros((3,3)) #output 3x3 matrix
R2=np.zeros((3,3)) #output 3x3 matrix
P1=np.zeros((3,4))#output 3x4 matrix
P2=np.zeros((3,4)) #output 3x4 matrix

cv2.stereoRectify(
   mtx_left, #intrinsic parameters of the first camera
   dist_left,
   mtx_right,
   dist_right,
   (left_im.shape[1], left_im.shape[0]),
   R,T,
   R1,R2,P1,P2) #last 4 parameters point to inizialized output variables

map1_x,map1_y=cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, (left_im.shape[1],left_im.shape[0]), cv2.CV_32FC1)
map2_x,map2_y=cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, (left_im.shape[1],left_im.shape[0]), cv2.CV_32FC1)

im_left_remapped=cv2.remap(left_im,map1_x,map1_y,cv2.INTER_CUBIC)
im_right_remapped=cv2.remap(right_im,map2_x,map2_y,cv2.INTER_CUBIC)

out=np.hstack((im_left_remapped,im_right_remapped))

for i in range(0,out.shape[0],30):
    cv2.line(out,(0,i),(out.shape[1],i),(0,255,255),3)

plt.figure(figsize=(10,4))
plt.imshow(out[...,::-1])
plt.show()


cv2.imshow('e',im_left_remapped)
cv2.imshow('a',im_right_remapped)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
