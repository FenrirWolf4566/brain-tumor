# Importing libraries
import data_loader
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import keras
import keras.backend as K
import tensorflow as tf
from tensorflow import keras
from train_model import model
from data_generator import *
from variables import *
from predict import *

"""
Ensemble des métriques qui permettent d'évaluer le modèle
    - Dice loss function,
    - Computing Precision,
    - Computing Sensitivity,
    - Computing Specificity.
"""


#############################################################################
# DICE LOSS FUNCTION 
#############################################################################

# dice loss as defined above for 4 classes
def dice_coef(y_true, y_pred, smooth=1.0):
    class_num = 4
    for i in range(class_num):
        y_true_f = K.flatten(y_true[:,:,:,i])
        y_pred_f = K.flatten(y_pred[:,:,:,i])
        intersection = K.sum(y_true_f * y_pred_f)
        loss = ((2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth))
   #     K.print_tensor(loss, message='loss value for class {} : '.format(SEGMENT_CLASSES[i]))
        if i == 0:
            total_loss = loss
        else:
            total_loss = total_loss + loss
    total_loss = total_loss / class_num
#    K.print_tensor(total_loss, message=' total dice coef: ')
    return total_loss

def dice_coef_necrotic(y_true, y_pred, epsilon=1e-6):
    intersection = K.sum(K.abs(y_true[:,:,:,1] * y_pred[:,:,:,1]))
    return (2. * intersection) / (K.sum(K.square(y_true[:,:,:,1])) + K.sum(K.square(y_pred[:,:,:,1])) + epsilon)

def dice_coef_edema(y_true, y_pred, epsilon=1e-6):
    intersection = K.sum(K.abs(y_true[:,:,:,2] * y_pred[:,:,:,2]))
    return (2. * intersection) / (K.sum(K.square(y_true[:,:,:,2])) + K.sum(K.square(y_pred[:,:,:,2])) + epsilon)

def dice_coef_enhancing(y_true, y_pred, epsilon=1e-6):
    intersection = K.sum(K.abs(y_true[:,:,:,3] * y_pred[:,:,:,3]))
    return (2. * intersection) / (K.sum(K.square(y_true[:,:,:,3])) + K.sum(K.square(y_pred[:,:,:,3])) + epsilon)

# 
def precision(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

# Computing Sensitivity      
def sensitivity(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    return true_positives / (possible_positives + K.epsilon())

# Computing Specificity
def specificity(y_true, y_pred):
    true_negatives = K.sum(K.round(K.clip((1-y_true) * (1-y_pred), 0, 1)))
    possible_negatives = K.sum(K.round(K.clip(1-y_true, 0, 1)))
    return true_negatives / (possible_negatives + K.epsilon())

#############################################################################
# Model evaluation 
#############################################################################
print("deja appel de méthode de predict by id")
train_ids, val_ids, test_ids = data_loader.load_data()

case = test_ids[0][-5:]
print("Patient : ",test_ids[0][-5:])
path = f"{TRAIN_DATASET_PATH}\BraTS2021_{case}"
gt = nib.load(os.path.join(path, f'BraTS2021_{case}_seg.nii')).get_fdata()
print(" /////\\\\\\\ Test")
p = predictByPath(path,case)

# Prob les class ne correspondent pas
#core = p[:,:,:,1]
#edema= p[:,:,:,2]
#enhancing = p[:,:,:,3]
core = p[:,:,:,2]
edema= p[:,:,:,1]
enhancing = p[:,:,:,3]

i=40 # slice at
eval_class = 1 #     0 : 'NOT tumor',  1 : 'ENHANCING',    2 : 'CORE',    3 : 'WHOLE'

gt[gt != eval_class] = 1 # use only one class for per class evaluation 

resized_gt = cv2.resize(gt[:,:,i+VOLUME_START_AT], (IMG_SIZE, IMG_SIZE))

#plt.figure()
#f, axarr = plt.subplots(1,2) 
#axarr[0].imshow(resized_gt, cmap="gray")
#axarr[0].title.set_text('ground truth')
#axarr[1].imshow(p[i,:,:,eval_class], cmap="gray")
#axarr[1].title.set_text(f'predicted class: {SEGMENT_CLASSES[eval_class]}')
#plt.show()

model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adam(learning_rate=0.001), metrics = ['accuracy',tf.keras.metrics.MeanIoU(num_classes=4), dice_coef, precision, sensitivity, specificity, dice_coef_necrotic, dice_coef_edema, dice_coef_enhancing] )
# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(test_generator, batch_size=100, callbacks = callbacks)
print("test loss, test acc:", results)