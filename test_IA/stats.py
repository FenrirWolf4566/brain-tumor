from nilearn import plotting
import pylab as plt
import numpy as np
import nibabel as nb

#https://peerherholz.github.io/workshop_weizmann/data/image_manipulation_nibabel.html

def parseValue(imageDirectory):
    img = nb.load(imageDirectory)
    data = img.get_fdata()
    #print(data.shape)
    # Nombre de pixels de chaque classe (values)
    classe=[0,0,0,0,0]
    for x in range(0,data.shape[0]-1):
        for y in range(0,data.shape[1]-1):
            for z in range(0,data.shape[2]-1):
                classe[int(data[x,y,z])]+=1
    # Total de pixels des classes 1, 2 et 4
    totalPixels= classe[1]+classe[2]+classe[4]
    # Calcule le pourcentage de pixel des classes 1, 2 et 4
    pourcentage = np.floor(np.array([classe[1]/totalPixels, classe[2]/totalPixels, classe[4]/totalPixels]) * 100) 
    return(classe,list(pourcentage))

def parseDir(dir):


print(parseValue("exemples\Sample_BRATZ\BraTS2021_01652\BraTS2021_01652_seg.nii.gz"))