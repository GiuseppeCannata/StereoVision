import cv2
import numpy as np

import GestioneLaser as laser
import ScattaFoto as scatta
import Ottieni_Matrici as matrici

def funz():
    
    #Scatto le immagini e detecto il laser
    laser.funz(1)  #accensione laser
    
    
    img_laser_L , img_laser_R = scatta.funz()

    #Rettificazione
    mtx_left,mtx_right,dist_left,dist_right,R,T,R1,R2,P1,P2 = matrici.ottieni();
    map1_x, map1_y = cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, (640, 480),
                                                 cv2.CV_32FC1)
    map2_x, map2_y = cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, (640, 480),
                                                 cv2.CV_32FC1)

    im_left_remapped = cv2.remap(img_laser_L, map1_x, map1_y, cv2.INTER_CUBIC)
    im_right_remapped = cv2.remap(img_laser_R, map2_x, map2_y, cv2.INTER_CUBIC)


    #individuare laser
    lower_red = np.array([0, 0 , 255])
    upper_red = np.array([240, 240, 255])
    maskL = cv2.inRange(im_left_remapped, lower_red, upper_red)
    maskR = cv2.inRange(im_right_remapped, lower_red, upper_red)
    
    (_, _, minLoc_L, maxLoc_L) = cv2.minMaxLoc(maskL)
    (_, _, minLoc_R, maxLoc_R) = cv2.minMaxLoc(maskR)
    
    cv2.circle(im_left_remapped, maxLoc_L, 20, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.circle(im_right_remapped, maxLoc_R, 20, (0, 0, 255), 2, cv2.LINE_AA)

    #print(maxLoc_L)
    #print(maxLoc_R)   
    disp = abs(maxLoc_R[0] - maxLoc_L[0])
    
    distanza = 5253 / disp
    
    
    print(distanza)
    
    laser.funz(0)  #spegnimento laser
    
    
    cv2.imshow('L', im_left_remapped )
    cv2.imshow('R', im_right_remapped )

    cv2.waitKey(0)
        

cv2.destroyAllWindows()       


