import numpy as np
import cv2
import os

"""
Permette di effettuare la calibrazione della propria camera e quindi di ottenere le matrici dei parametri intrinseci ed estrinseci.

-Cose importanti:

 1- Scattare le foto dalla propria StereoCamera e dividerle (solitamente una StereoCamera scatta un unica foto)
 2- Le immagini sia di destra che di sinistra che vengono utilizzate per la calibrazione devono essere nominate  
    come segue:
    
        left<numero_immagine>.png
        right<numero_immagine>.png
    
    Occhio! le immagini relative ad una stessa foto devono avere lo stesso numero cioè: FOTO-->LA DIVIDO--> Left1 e right1
            l estensione è .png
            
 3- Le immagini, sia di Sx che Rx, devono essere 10

"""
# == GESTIONE ===============================================================

# Percorso del DataSet delle immagini per effettuare la calibrazione
# Ci devono essere almeno 10 immagini per avere una buona calibrazione
# Siccome calibreremo una StereoCamera abbiamo i path delle immagini di Rx e Sx
pathLeft = '/home/giuseppe/Scrivania/left'
pathRight = '/home/giuseppe/Scrivania/right'

# Path della cartella dove verranno salvati i risultati della calibrazione
Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'

# Dati relativi alla scacchiera utilizzata
nCol = 9  # number of rows of chessboard -1
nRow = 6  # number of columns of chessboard -1
dimSquare = 25  # dimensione del quadrato della scacchiera

# ==========================================================================

def Salva_su_file(folder, nome_file, elemento_da_salvare):
    np.save(folder+ nome_file, elemento_da_salvare)

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


try:
    nR = os.list(pathRight)
    nL = os.list(pathLeft)

    if nR != 10:
        raise Exception("Numero minore di 10 nella cartella della camere di detra")
    if nL != 10:
        raise Exception("Numero minore di 10 nella cartella della camere di detra")

    # minimo 10 foto per la calibrazione
    idx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
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


    imgLeft = cv2.imread(os.path.join(pathLeft, "left%d.png"%i))
    imgRight = cv2.imread(os.path.join(pathRight, "right%d.png"%i))

    # conversion in to gray scale
    grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)
    print(grayLeft)
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

except Exception as e:
    print(e.message)
