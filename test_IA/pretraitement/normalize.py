import nibabel as nib
import numpy as np
import os 

def normImg(imageFile):
    img = nib.load(imageFile)
    data = img.get_fdata()
    mean = getMean(data)
    std = np.std(data)
    data = normalize(data,mean,std)
    xform = np.eye(4) * 2
    img = nib.nifti1.Nifti1Image(data, xform)
    name = np.split(imageFile)[-1]
    chemin=os.getcwd()
    os.chdir(chemin)
    nib.save(img, 'pre'+name)
    return

# Return the mean intensity of the image
def getMean(data):
    sum = 0
    for x in range(0,data.shape[0]-1):
        for y in range(0,data.shape[1]-1):
            for z in range(0,data.shape[2]-1):
                sum += data[x,y,z]
    return sum /(data.shape[0]*data.shape[1]*data.shape[2])

# return the normalized image
def normalize(data,mean,std):
    for x in range(0,data.shape[0]-1):
        for y in range(0,data.shape[1]-1):
            for z in range(0,data.shape[2]-1):
                data[x,y,z] = (data[x,y,z]-mean)/std
    return data