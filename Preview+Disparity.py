import cv2
import numpy as np
import src.Funzioni as funzioni


Folder_save_calib = '/home/giuseppe/Scrivania/ResultCalib'
Folder_save_rect = '/home/giuseppe/Scrivania/ResultRect'

# ==================================== LETTURA DELLE MATRICI  =========================

mtx_left = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Sx.npy")
mtx_right = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Intrinseca_Dx.npy")
dist_left = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Sx.npy")
dist_right = funzioni.leggi_da_file_matrici(Folder_save_calib , "/Matrice_Distorsione_Dx.npy")
R = funzioni.leggi_da_file_matrici(Folder_save_calib , "/R.npy")
T = funzioni.leggi_da_file_matrici(Folder_save_calib , "/T.npy")

R1 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/R1.npy")
R2 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/R2.npy")
P1 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/P1.npy")
P2 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/P2.npy")

# ======================================================================================


maxDisp = 128 #la massima disparità ci serve per riconoscere gli oggetti vicini
stereoProcessor = cv2.StereoSGBM_create(minDisparity=0, numDisparities=maxDisp, blockSize=9)

cap = cv2.VideoCapture(1)

while (True):

    # capture frame-by-frame
    _ , frame = cap.read()
    imgLeft = frame[0:480,0:640]
    imgRight = frame[0:480,641:1280]

    #Rectification
    map1_x, map1_y = cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, (640, 480) , cv2.CV_32FC1)
    map2_x, map2_y = cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, (640, 480),cv2.CV_32FC1)

    im_left_remapped = cv2.remap(imgLeft, map1_x, map1_y, cv2.INTER_CUBIC)
    im_right_remapped = cv2.remap(imgRight, map2_x, map2_y, cv2.INTER_CUBIC)

    gray_left = cv2.cvtColor(im_left_remapped, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(im_right_remapped, cv2.COLOR_BGR2GRAY)

    disparity = stereoProcessor.compute(gray_left, gray_right)
    #filtro per il rumore
    cv2.filterSpeckles(disparity, 0 , 4000, maxDisp)

    #se la disparity è zero(oggetti distanti)  sparali
    _, disparity = cv2.threshold(disparity, 0, maxDisp*16, cv2.THRESH_TOZERO)
    disparity_scaled = (disparity /16).astype(np.uint8)
    disparity = (disparity_scaled * (255. / maxDisp)).astype(np.uint8)


    cv2.imshow('Left', im_left_remapped)
    cv2.imshow('Right', im_right_remapped)
    cv2.imshow('Disparity', disparity)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything done,release the capture
cap.release()
cv2.destroyAllWindows()