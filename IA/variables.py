import os

# DEFINE seg-areas  
SEGMENT_CLASSES = {
    0 : 'NOT tumor',
    1 : 'NECROTIC/CORE', # tumor CORE
    2 : 'EDEMA',         # Whole Tumor
    3 : 'ENHANCING'      # Propogation (original 4 -> converted into 3 later)
}

VOLUME_SLICES = 155 
VOLUME_START_AT = 0
IMG_SIZE=128
IMG_RESIZE=240
TRAIN_DATASET_PATH = os.path.join("IA", "dataset","training")
VALIDATION_DATASET_PATH = os.path.join("IA", "dataset","validation")

PATIENT_PATH = os.path.join("IA","doctor", "patients")
PREDICTION_PATH = os.path.join("IA","doctor", "prediction")
DOCTOR_PATH = os.path.join("IA","doctor")


