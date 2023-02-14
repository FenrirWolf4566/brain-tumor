from nilearn import plotting
import pylab as plt
import numpy as np
import nibabel as nb
import os
from tqdm import tqdm
import shutil

#https://peerherholz.github.io/workshop_weizmann/data/image_manipulation_nibabel.html


"""
parseValue : parse les pixels de la segmentation et compte les occurences des classes (1 2 ou 4) - la classe 3 étant inéxistante
             renvoie une liste d'occucence et une liste de poucentage
             ([8633066, 23, 151302, 0, 12243], [0.0, 92.0, 7.0])
"""
def parseValue(imageDirectory):
    img = nb.load(imageDirectory)
    data = img.get_fdata()
    #print(data.shape)
    # Nombre de pixels de chaque classe (values)
    classe=[0,0,0,0,0]
    for x in range(0,data.shape[0]-1):
        for y in range(0,data.shape[1]-1):
            for z in range(0,data.shape[2]-1):
                classe[int(data[x,y,z])]+=1
    # Total de pixels des classes 1, 2 et 4
    totalPixels= classe[1]+classe[2]+classe[4]
    # Calcule le pourcentage de pixel des classes 1, 2 et 4
    pourcentage = np.floor(np.array([classe[1]/totalPixels, classe[2]/totalPixels, classe[4]/totalPixels]) * 100) 
    return(classe,list(pourcentage))
#print(parseValue("..\exemples\Sample_BRATZ\BraTS2021_01652\BraTS2021_01652_seg.nii.gz"))
#print(parseValue("..\exemples\Sample_BRATZ\BraTS2021_01575\BraTS2021_01575_seg.nii.gz"))
#print(parseValue("..\exemples\Sample_BRATZ\BraTS2021_01637\BraTS2021_01637_seg.nii.gz"))


"""
ecartPourcent : calcule et renvoie l'écart du max et min des pourcentages
                [30.0, 49.0, 20.0]
"""
def ecartPourcent(l_pourcentage):
    max_pourcent=max(l_pourcentage)
    min_pourcent=min(l_pourcentage)
    return(max_pourcent-min_pourcent)



"""
parseBRATS : renvoie un dictionnaire "nom_du_fichier : ecart_pourcentage"
"""
def parseBRATS(chemin):
    chemin_base=os.getcwd()
    os.chdir(chemin)
    list_dir=os.listdir()
    os.chdir(chemin_base)
    dictionnaire_BRATS={}
    for element in tqdm(list_dir[:10]):
        #print(chemin+"\\"+element+"\\"+element+"_seg.nii.gz")
        set_pourcentage=parseValue(chemin+"\\"+element+"\\"+element+"_seg.nii.gz")
        pourcentage=ecartPourcent(set_pourcentage[1])
        dictionnaire_BRATS[str(element)]=str(pourcentage)
    return(dictionnaire_BRATS)

#print(parseBRATS("..\exemples\Sample_BRATZ"))


"""
sortBRATS : créer une liste des noms de fichier que doit contenir le trainingset
            size : pourcentage demandé pour faire le trainingset
"""
def sortBRATS(chemin, size = float(30)):
    dictionnaire=parseBRATS(chemin)
    sortedDictionnaire=dict(sorted(dictionnaire.items(), key=lambda item: item[1]))
    dicoSize=len(sortedDictionnaire)
    #print(sortedDictionnaire)
    trainingSet=[]
    for element in range(0,int(dicoSize*size/100)):
        trainingSet.append(list(sortedDictionnaire)[element])
    return(trainingSet, sortedDictionnaire)
#print(sortBRATS("..\exemples\Sample_BRATZ", float(40)))


"""
separateBRATS : crée un répertoire "trainingSet" et "testSet" et séparer les fichiers du dataset en fconction de la répartition
"""
def separateBRATS(chemin):
    trainingSet,sortedDictionnaire=sortBRATS(chemin, float(50))
    print(sortedDictionnaire)
    pathTrain = os.path.join("","trainingSet")
    if(not os.path.exists(pathTrain)) :
        os.mkdir(pathTrain)
    pathTest = os.path.join("","testSet")
    if(not os.path.exists(pathTest)) :
        os.mkdir(pathTest)
    source=chemin+"\\"
    destinationTrain="trainingSet"
    destinationTest="testSet"
    for element in tqdm(sortedDictionnaire, desc ="Traning Set completion ..."):
        if(element in trainingSet):
            shutil.copytree(source+"\\"+element,destinationTrain+"\\"+element)
        else:           
            shutil.copytree(source+"\\"+element,destinationTest+"\\"+element)
separateBRATS("..\exemples\Sample_BRATZ")


