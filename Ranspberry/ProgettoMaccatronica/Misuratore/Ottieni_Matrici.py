import Funzioni as funzioni

def ottieni():

    Folder_save_calib = '../ResultCalib'
    Folder_save_rect = '../ResultRect'


    mtx_left = funzioni.leggi_da_file_matrici(Folder_save_calib, "/Matrice_Intrinseca_Sx.npy")
    mtx_right = funzioni.leggi_da_file_matrici(Folder_save_calib, "/Matrice_Intrinseca_Dx.npy")
    dist_left = funzioni.leggi_da_file_matrici(Folder_save_calib, "/Matrice_Distorsione_Sx.npy")
    dist_right = funzioni.leggi_da_file_matrici(Folder_save_calib, "/Matrice_Distorsione_Dx.npy")
    R = funzioni.leggi_da_file_matrici(Folder_save_calib, "/R.npy")
    T = funzioni.leggi_da_file_matrici(Folder_save_calib, "/T.npy")

    R1 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/R1.npy")
    R2 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/R2.npy")
    P1 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/P1.npy")
    P2 = funzioni.leggi_da_file_matrici(Folder_save_rect, "/P2.npy")

    return mtx_left,mtx_right,dist_left,dist_right,R,T,R1,R2,P1,P2
