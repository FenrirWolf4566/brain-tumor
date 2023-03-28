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
import data_loader


#############################################################################
# Prediction examples - Mock
#############################################################################

# mri type must one of 1) flair 2) t1 3) t1ce 4) t2 ------- or even 5) seg
# returns volume of specified study at `path`
def imageLoader(path):
    image = nib.load(path).get_fdata()
    X = np.zeros((self.batch_size*VOLUME_SLICES, *self.dim, self.n_channels))
    for j in range(VOLUME_SLICES):
        X[j +VOLUME_SLICES*c,:,:,0] = cv2.resize(image[:,:,j+VOLUME_START_AT], (IMG_SIZE, IMG_SIZE));
        X[j +VOLUME_SLICES*c,:,:,1] = cv2.resize(ce[:,:,j+VOLUME_START_AT], (IMG_SIZE, IMG_SIZE));
    return np.array(image)


# load nifti file at `path`
# and load each slice with mask from volume
# choose the mri type & resize to `IMG_SIZE`
def loadDataFromDir(path, list_of_files, mriType, n_images):
    scans = []
    masks = []
    for i in list_of_files[:n_images]:
        fullPath = glob.glob( i + '/*'+ mriType +'*')[0]
        currentScanVolume = imageLoader(fullPath)
        currentMaskVolume = imageLoader( glob.glob( i + '/*seg*')[0] ) 
        # for each slice in 3D volume, find also it's mask
        for j in range(0, currentScanVolume.shape[2]):
            scan_img = cv2.resize(currentScanVolume[:,:,j], dsize=(IMG_SIZE,IMG_SIZE), interpolation=cv2.INTER_AREA).astype('uint8')
            mask_img = cv2.resize(currentMaskVolume[:,:,j], dsize=(IMG_SIZE,IMG_SIZE), interpolation=cv2.INTER_AREA).astype('uint8')
            scans.append(scan_img[..., np.newaxis])
            masks.append(mask_img[..., np.newaxis])
    return np.array(scans, dtype='float32'), np.array(masks, dtype='float32')
        

"""
def predictByPath(case_path,case):
    files = next(os.walk(case_path))[2]
    X = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE, 2))
    y = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE))
    
    vol_path = os.path.join(case_path, f'BraTS2021_{case}_flair.nii');
    flair=nib.load(vol_path).get_fdata()
    
    vol_path = os.path.join(case_path, f'BraTS2021_{case}_t1ce.nii');
    ce=nib.load(vol_path).get_fdata() 
    
 #   vol_path = os.path.join(case_path, f'BraTS20_Training_{case}_seg.nii');
 #   seg=nib.load(vol_path).get_fdata()  

    
    for j in range(VOLUME_SLICES):
        X[j,:,:,0] = cv2.resize(flair[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        X[j,:,:,1] = cv2.resize(ce[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        #y[j,:,:] = cv2.resize(seg[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        
  #  model.evaluate(x=X,y=y[:,:,:,0], callbacks= callbacks)
    return model.predict(X/np.max(X), verbose=1)
"""

"""
def predictsById(case, start_slice = 60):
    # Combine and save the .nii of prediction
    path = f"{TRAIN_DATASET_PATH}\BraTS2021_{case}"
    gt = nib.load(os.path.join(path, f'BraTS2021_{case}_seg.nii')).get_fdata()
    origImage = nib.load(os.path.join(path, f'BraTS2021_{case}_flair.nii')).get_fdata()
    p = predictByPath(path,case)

    # Prob les class ne correspondet pas 
    core = p[:,:,:,1]
    edema= p[:,:,:,2]
    enhancing = p[:,:,:,3]

    #core = p[:,:,:,2]
    #edema= p[:,:,:,1]
    #enhancing = p[:,:,:,3]

    # Combine
    predictionNii = combine(core, edema, enhancing)
    # Save
    saveNifti(predictionNii, case)
"""


def predictByPath(case_path,case):
    files = next(os.walk(case_path))[2]
    X = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE, 2))
    y = np.empty((VOLUME_SLICES, IMG_SIZE, IMG_SIZE))
    
    vol_path = os.path.join(case_path, f'{case}_flair.nii');
    flair=nib.load(vol_path).get_fdata()
    
    vol_path = os.path.join(case_path, f'{case}_t1ce.nii');
    ce=nib.load(vol_path).get_fdata() 
    
    for j in range(VOLUME_SLICES):
        X[j,:,:,0] = cv2.resize(flair[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        X[j,:,:,1] = cv2.resize(ce[:,:,j+VOLUME_START_AT], (IMG_SIZE,IMG_SIZE))
        
    return model.predict(X/np.max(X), verbose=1)


def predictsById(case, start_slice = 60):
    """
    Combine and save the .nii of prediction
    """
    path = f"{PATIENT_PATH}\{case}"
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
    template_nii = nib.load(os.path.join("doctor", "template_seg.nii"))
    result = nib.Nifti1Image(image, template_nii.affine, template_nii.header)
    nib.save(result, os.path.join("doctor", "prediction", "{}.nii".format(case)))


train_ids, val_ids, test_ids = data_loader.load_data()

predictsById(case="01572")
