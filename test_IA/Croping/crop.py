import numpy as np
import nibabel as nib
import os
from tqdm import tqdm
import os

#https://nipy.org/nibabel/nibabel_images.html

# Example
path="test_IA/Croping/test_flair.nii.gz"
img = nib.load(path)
print(img)


