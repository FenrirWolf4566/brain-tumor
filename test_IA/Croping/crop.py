import numpy as np
import nibabel as nib
import os
from tqdm import tqdm
import os
import matplotlib.pyplot as plt

#https://nipy.org/nibabel/nibabel_images.html

# Example
path="test_IA/Croping/test_flair.nii.gz"
img = nib.load(path)
#print(img)
# Longueur largeur profondeur


def cropping(img,size=90):
    cropped_img = img.slicer[32:-32, ...]
    print("Basic shape : ",img.shape)
    print("New shape : ",cropped_img.shape)
    return(cropped_img)


def showSlice(img):
    plot_nifti=img.get_fdata()
    plot_nifti = plot_nifti[:,:,59]
    plt.imshow(plot_nifti)
    plt.show()


cro=cropping(img)
#showSlice(img)