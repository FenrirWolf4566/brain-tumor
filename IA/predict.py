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
from scipy import ndimage
from scipy.ndimage import label, generate_binary_structure

def predictByPath(case_path,case):

    X = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE, 2))  
    vol_path = os.path.join(case_path, f'{case}_flair.nii');
    flair=nib.load(vol_path).get_fdata()
    
    vol_path = os.path.join(case_path, f'{case}_t1ce.nii');
    ce=nib.load(vol_path).get_fdata() 
    
    for j in range(VOLUME_SLICES):
        X[j,:,:,0] = cv2.resize(flair[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        X[j,:,:,1] = cv2.resize(ce[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        
    return model.predict(X/np.max(X), verbose=1)


def predictsById(case):
    """
    Combine and save the .nii of prediction
    """
    path = f"{PATIENT_PATH}\{case}"
    p = predictByPath(path,case)
    core = p[:,:,:,2]
    edema= p[:,:,:,1]
    enhancing = p[:,:,:,3]
    predictionNii = combine(core, edema, enhancing)
    saveNifti(predictionNii)
    

def combine(core, edema, enhancing):
    # Créer un tableau qui contient la classe prédite pour chaque élément 
    predicted_classes = np.where(core < 0.4, 2, 4) 
    predicted_classes = np.where((enhancing < 0.4) & (predicted_classes == 2), 1, predicted_classes)
    predicted_classes = np.where((edema < 0.4) & (predicted_classes == 1), 0, predicted_classes)    
    # Créer un tableau copie qui superpose les trois classes 
    superposed_classes = np.zeros_like(core) 
    superposed_classes[predicted_classes == 1] = 1 
    superposed_classes[predicted_classes == 2] = 2 
    superposed_classes[predicted_classes == 4] = 4
    # Mise en forme du tableau
    superposed_classes = superposed_classes.astype(int)
    superposed_classes = flip(predicted_classes)
    superposed_classes = filter(superposed_classes,count_connected_voxels(superposed_classes)-2)
    print("Values : ", np.unique(superposed_classes))
    return superposed_classes

NAME = "pred"

def saveNifti(image) :
    template_nii = nib.load(os.path.join("IA","doctor", "template_seg.nii"))
    result = nib.Nifti1Image(image, template_nii.affine, template_nii.header)
    nib.save(result, os.path.join(PREDICTION_PATH,NAME+".nii"))

def flip(superposed_classes):
    # Resize de l'image pour le visualiseur
    resized = ndimage.zoom(superposed_classes, (1,240/128,240/128))
    # Fixing the pixels value caused by resizing
    resized = np.where(resized == 3, 2, resized)
    resized = np.where(resized == 5, 4, resized)
    resized = np.where(resized == 6, 4, resized)
    resized = np.where(resized == 7, 1, resized)
    resized = np.where(resized == -1, 0, resized)
    # Réorganisation des colonnes pour être comforme au visualiseur
    flipped = np.transpose(resized, (1,2,0))
    return flipped

def filter(arr, num_pixels):
    # Choix de la calsse à étudier
    region_mask = arr == 1
    # Calcul du nombre de voxels connectés 
    num_connected = np.sum(label(region_mask, generate_binary_structure(3, 2))[0] > 1)
    if num_connected < num_pixels:
        arr[region_mask] = 0
    return arr


def count_connected_voxels(arr):
    # Choix de la calsse à étudier
    mask = arr == 1
    struct = np.ones((3, 3, 3), dtype=bool)
    struct[1, 1, 1] = False
    eroded = np.zeros_like(mask)
    count = 0
    while np.any(mask):
        eroded[:] = np.logical_and(mask, np.logical_not(eroded))
        if np.sum(eroded) > 0:
            count += 1
        mask[:] = np.logical_and(mask, np.logical_not(eroded))
    return count
