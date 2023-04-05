#### VARIABLES UTILISEES POUR LA PREDICTION
VOLUME_SLICES = 100 
VOLUME_START_AT = 22
IMG_SIZE=128

import os
import tempfile

temp_folder = tempfile.TemporaryDirectory()

PATIENT_PATH =  os.path.join("niftis","patients")
PREDICTION_PATH = os.path.join("niftis","predictions")
TEMPLATE_PATH = os.path.join("niftis","template_seg.nii")

MODEL_PATH = "model/"