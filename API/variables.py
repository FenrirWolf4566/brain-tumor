#### VARIABLES UTILISEES POUR LA PREDICTION
VOLUME_SLICES = 155 
VOLUME_START_AT = 0
IMG_SIZE=128

import os


TMP_PATIENT_ID = "tmpid"
PATIENT_PATH =  os.path.join("niftis","patients")
PREDICTION_PATH = os.path.join("niftis","predictions")
TEMPLATE_PATH = os.path.join("niftis","template_seg.nii")

MODEL_PATH = "model/"