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
from scipy import ndimage
from scipy.spatial.transform import Rotation


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
        #y[j +VOLUME_SLICES*c] = seg[:,:,j+VOLUME_START_AT];
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
        
#brains_list_test, masks_list_test = loadDataFromDir(VALIDATION_DATASET_PATH, test_directories, "flair", 5)

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

def combine(core, edema, enhancing):

    '''core = thesholding(core, 0.4, 3)
    enhancing = thesholding(enhancing, 0.45, 2)
    edema = thesholding(edema, 0.45, 1)'''
    # Créer un tableau qui contient la classe prédite pour chaque élément 
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
    '''image = np.maximum.reduce([core,edema,enhancing])
    image = np.where(image == 2, 4, image)
    image = np.where(image == 1, 2, image)
    image = np.where(image == 3, 1, image)
    return (image)'''
    return superposed_classes

def flip(superposed_classes):
    print("first",np.shape(superposed_classes))
    resized = ndimage.zoom(superposed_classes, (1,240/128,240/128))
    print("after resize ",np.shape(superposed_classes))
    flipped = np.transpose(resized, (2,1,0))
    print("after transpose ",np.shape(flipped))
    return flipped

def showPredictsById(case, start_slice = 60):
    path = f"{TRAIN_DATASET_PATH}\BraTS2021_{case}"
    gt = nib.load(os.path.join(path, f'BraTS2021_{case}_seg.nii')).get_fdata()
    origImage = nib.load(os.path.join(path, f'BraTS2021_{case}_flair.nii')).get_fdata()
    p = predictByPath(path,case)

    # Prob les class ne correspondet pas 
    #core = p[:,:,:,1]
    #edema= p[:,:,:,2]
    #enhancing = p[:,:,:,3]
    #arr_rotated = np.transpose(arr, (1, 0, 2))[:, :, ::-1, :][:, :, ::-1, :]
    core = p[:,:,:,2]
    edema = p[:,:,:,1]
    enhancing = p[:,:,:,3]

    #plt.figure(figsize=(18, 50))
    f, axarr = plt.subplots(1,3, figsize = (36, 100)) 

    for i in range(2): # for each image, add brain background
        axarr[i].imshow(cv2.resize(origImage[:,:,start_slice+VOLUME_START_AT], (IMG_SIZE, IMG_SIZE)), cmap="gray", interpolation='none')

    background = np.rot90(cv2.resize(origImage[:,:,start_slice+VOLUME_START_AT], (240, 240)),-1)
    background = np.fliplr(background)
    axarr[2].imshow(background, cmap="gray", interpolation='none')
    
    axarr[0].imshow(cv2.resize(origImage[:,:,start_slice+VOLUME_START_AT], (IMG_SIZE, IMG_SIZE)), cmap="gray")
    axarr[0].title.set_text('Original image flair')

    #axarr[1].imshow(curr_gt, cmap="Reds", interpolation='none', alpha=0.3) # ,alpha=0.3,cmap='Reds'
    #axarr[1].title.set_text('Ground truth')
    

    # Core
    #axarr[2].imshow(edema[start_slice,:,:], cmap="OrRd", interpolation='none', alpha=0.3)
    #axarr[2].title.set_text(f'{SEGMENT_CLASSES[1]} predicted')

    # Enhancing
    #axarr[3].imshow(enhancing[start_slice,:,], cmap="OrRd", interpolation='none', alpha=0.3)
    #axarr[3].title.set_text(f'{SEGMENT_CLASSES[3]} predicted')

    # Whole
    #axarr[4].imshow(core[start_slice,:,], cmap="OrRd", interpolation='none', alpha=0.3)
    #axarr[4].title.set_text(f'{SEGMENT_CLASSES[2]} predicted')

    #Asswhole
    axarr[1].imshow(combine(core, edema, enhancing)[start_slice,:,:], cmap="OrRd", interpolation='none', alpha=0.3)
    axarr[1].title.set_text(f'prédiction')


    img = combine(core, edema, enhancing)
    resize = flip(img)[:,:,start_slice]

    axarr[2].imshow(resize, cmap="OrRd", interpolation='none', alpha=0.3)
    axarr[2].title.set_text(f'prédiction augmentée')
    plt.show()

train_ids, val_ids, test_ids = data_loader.load_data()

print("Patient : ",test_ids[0][-5:])
showPredictsById(case=test_ids[0][-5:])
#showPredictsById(case=test_ids[1][-5:])
#showPredictsById(case=test_ids[2][-5:])
#showPredictsById(case=test_ids[3][-5:])
#showPredictsById(case=test_ids[4][-5:])
#showPredictsById(case=test_ids[5][-5:])
#showPredictsById(case=test_ids[6][-5:])


# mask = np.zeros((10,10))
# mask[3:-3, 3:-3] = 1 # white square in black background
# im = mask + np.random.randn(10,10) * 0.01 # random image
# masked = np.ma.masked_where(mask == 0, mask)

# plt.figure()
# plt.subplot(1,2,1)
# plt.imshow(im, 'gray', interpolation='none')
# plt.subplot(1,2,2)
# plt.imshow(im, 'gray', interpolation='none')
# plt.imshow(masked, 'jet', interpolation='none', alpha=0.7)
# plt.show()



