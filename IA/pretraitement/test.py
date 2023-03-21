import nibabel as nib
import numpy as np


"""
Create an nifti image
"""
data = np.random.random((20, 20, 20))
xform = np.eye(4) * 2
img = nib.nifti1.Nifti1Image(data, xform)
print(type(img))
nib.save(img, 'scaled_image.nii')