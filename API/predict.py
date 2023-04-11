# Importing the libraries
import os
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt 
import nibabel as nib
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from variables import *
from train_model import model


#############################################################################
# Prediction examples - Mock
#############################################################################




def loadNiftiFile(file_path):
    img = nib.load(file_path)
    return img.get_fdata()

def saveNiftiFile(data, file_path, file_name):
    Path(file_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(file_path,file_name)
    nib.save(data, file_path)
    print("Nifti File saved :"+file_path)
    return file_path


async def predictByPath(case_path,case):
    X = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE, 2))
    vol_path = os.path.join(case_path,f'{case}_flair.nii')
    flair=  loadNiftiFile(vol_path) 
    vol_path = os.path.join(case_path, f'{case}_t1ce.nii')
    ce= loadNiftiFile(vol_path)  
    for j in range(VOLUME_SLICES):
        X[j,:,:,0] = cv2.resize(flair[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        X[j,:,:,1] = cv2.resize(ce[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
    return  model.predict(X/np.max(X), verbose=1)


async def predictsById(patient_folder,case):
    """
    Combine and save the .nii of prediction
    """
    path = patient_folder 
    p = await predictByPath(path,case)
    core = p[:,:,:,2]
    edema= p[:,:,:,1]
    enhancing = p[:,:,:,3]
    predictionNii =  combine(core, edema, enhancing)
    return saveNifti(predictionNii, os.path.join(patient_folder,case),case)

    

def combine(core, edema, enhancing, threshold = 0.5):
    core = thesholding(core, threshold, 3) 
    edema = thesholding(edema, threshold, 1)
    enhancing = thesholding(enhancing, threshold, 2)
    image = np.maximum.reduce([core,edema,enhancing])
    image = np.where(image == 2, 4, image)
    image = np.where(image == 1, 2, image)
    image = np.where(image == 3, 1, image)
    return (image)


def thesholding(tab, threshold, contrast):
    """
    Fonction qui applique un seuil à un tableau numpy et renvoie un nouveau tableau
    avec des 0 pour les valeurs inférieures au seuil et des 1 pour les valeurs supérieures ou égales au seuil.
    """
    resultat = np.copy(tab)
    resultat[resultat < threshold] = 0
    resultat[resultat >= threshold] = contrast
    return resultat


def saveNifti(image, case,path) :
    template_nii = nib.load(TEMPLATE_PATH)
    result = nib.Nifti1Image(image, template_nii.affine, template_nii.header)
    return saveNiftiFile(result,path,case+"_seg.nii")


# predictsById(case="01572")