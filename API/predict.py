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

    

def combine(core, edema, enhancing):
    predicted_classes = np.where(core < 0.4, 2, 3) 
    predicted_classes = np.where((enhancing < 0.4) & (predicted_classes == 2), 1, predicted_classes)
    predicted_classes = np.where((edema < 0.4) & (predicted_classes == 1), 0, predicted_classes)    
    #Créer un tableau qui superpose les trois classes 
    superposed_classes = np.zeros_like(core) 
    superposed_classes[predicted_classes == 1] = 1 
    superposed_classes[predicted_classes == 2] = 2 
    superposed_classes[predicted_classes == 3] = 3
    superposed_classes = np.where(superposed_classes == 2, 4, superposed_classes)
    superposed_classes = np.where(superposed_classes == 1, 2, superposed_classes)
    superposed_classes = np.where(superposed_classes == 3, 1, superposed_classes)
    superposed_classes = flip(superposed_classes)
    return superposed_classes


def flip(superposed_classes):
    flipped = np.zeros((100,240,240))
    process = np.zeros_like(superposed_classes)
    for i in range(superposed_classes.shape[0]):
        process[i,:,:] = np.rot90(superposed_classes[i,:,:], -1)
        process[i,:,:] = np.flip(superposed_classes[i,:,:], 0)
        flipped[i,:,:] = cv2.resize(superposed_classes[i,:,:],(240,240))
    return flipped


def saveNifti(image, case,path) :
    template_nii = nib.load(TEMPLATE_PATH)
    result = nib.Nifti1Image(image, template_nii.affine, template_nii.header)
    return saveNiftiFile(result,path,case+"_seg.nii")


# predictsById(case="01572")