# Importing the libraries
import os
import cv2
import glob
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


def predictByPath(case_path,case):
    X = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE, 2))
    
    vol_path = case_path+"/" f'{case}_flair.nii'
    flair=nib.load(vol_path).get_fdata()
    
    vol_path = os.path.join(case_path, f'{case}_t1ce.nii')
    ce=nib.load(vol_path).get_fdata() 
    
    for j in range(VOLUME_SLICES):
        X[j,:,:,0] = cv2.resize(flair[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        X[j,:,:,1] = cv2.resize(ce[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        
    return model.predict(X/np.max(X), verbose=1)


def predictsById(case):
    """
    Combine and save the .nii of prediction
    """
    path = f"{PATIENT_PATH}/{case}"
    p = predictByPath(path,case)
    core = p[:,:,:,2]
    edema= p[:,:,:,1]
    enhancing = p[:,:,:,3]
    predictionNii = combine(core, edema, enhancing)
    saveNifti(predictionNii, case)
    

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


def saveNifti(image, case) :
    template_nii = nib.load(TEMPLATE_PATH)
    result = nib.Nifti1Image(image, template_nii.affine, template_nii.header)
    nib.save(result, PREDICTION_PATH+"/"+"{}".format(case)+"_seg.nii")
    print("FICHIER SAUVE"+PREDICTION_PATH+"/"+"{}".format(case)+"_seg.nii")


# predictsById(case="01572")