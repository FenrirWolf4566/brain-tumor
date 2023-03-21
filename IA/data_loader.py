# Import libraries
import os
from sklearn.model_selection import train_test_split
from variables import *

#############################################################################
# Load data
#############################################################################

# lists of directories with studies
train_directories = [f.path for f in os.scandir(TRAIN_DATASET_PATH) if f.is_dir()]

def pathListIntoIds(dirList):
    """
    Change names of directories into ids
    """
    x = []
    for i in range(0,len(dirList)):
        x.append(dirList[i][dirList[i].rfind('/')+1:])
    return x


def load_data():
    """
    Split data into train, validation and test sets
    """
    train_and_test_ids = pathListIntoIds(train_directories); 
    val_ids = pathListIntoIds(VALIDATION_DATASET_PATH)
    train_ids, test_ids = train_test_split(train_and_test_ids,test_size=0.15)
    return train_ids, val_ids, test_ids


