import numpy as np
"""
File dove sono presenti la lettura e scrittura su file .npy

"""
def leggi_da_file_matrici(folder, nome_file):
    mtx = np.load(folder + nome_file)
    return mtx

def Salva_su_file(folder, nome_file, elemento_da_salvare):
    np.save(folder+ nome_file, elemento_da_salvare)