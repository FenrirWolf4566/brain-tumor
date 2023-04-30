import json
from typing import List

from pathlib import Path

import os

from fastapi import Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm

from variables import TMP_PATIENT_ID

from fastapi.responses import FileResponse

import auth

import predict

import os
import gzip
import io
import tempfile

dossiers_patients = {} #dictionnaire contenant les dossiers temporaires de chaque docteur


#############################
#     ECRITURE ET ENVOI     #
#        DE FICHIERS        # 
#############################

def write_file(file_path, file_name,file: UploadFile = File(...)):
    Path(file_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(file_path,file_name)
    print("Upload File saved :"+file_path)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        return {"filename": file_name}
    


def write_niftii_file(file_path, file_name, file: UploadFile = File(...)):
    # Decompresses file if it is a .gz file
    filename, file_extension = os.path.splitext(file.filename)
    if file_extension == '.gz':
        with gzip.open(file.file, 'rb') as f_in:
            f_out = io.BytesIO()
            while True:
                chunk = f_in.read(4096)
                if not chunk:
                    break
                f_out.write(chunk)
            f_out.seek(0)
            file_to_write = UploadFile(filename=filename[:-3], file=f_out)
    else:
        file_to_write = file

    # Check if file to save is NIfTI (.nii) 
    _, ext = os.path.splitext(file_name)
    if ext not in ['.nii', '.nii.gz']:
        # If a temporary file was created, close it
        if file_to_write != file:
            file_to_write.file.close()
        return {"res_status":"error", "detail":"File is not a .nii or .nii.gz"}

    # Write file
    result = write_file(file_path, file_name, file_to_write)

    # If a temporary file was created, close it
    if file_to_write != file:
        file_to_write.file.close()

    return result



def addFile(file : UploadFile, filetype : str,user:auth.User,idPatient=TMP_PATIENT_ID):
   if user['res_status']=='success':
        dossier_patient =dossiers_patients[user['id']][idPatient]
        res =write_niftii_file(dossier_patient.name,idPatient+f"_{filetype}.nii",file)
        if("res_status" in res and res['res_status']=='error'):  return res
        return  loadedfiles(user)
   return user

def cancelfiles(me:auth.User,idPatient=TMP_PATIENT_ID):
    dossier = dossiers_patients[me['id']][idPatient]
    dossier.cleanup()
    dossiers_patients[me['id']][idPatient] =tempfile.TemporaryDirectory()
    return loadedfiles(me,idPatient)

def loadedfiles(me=auth.User,idPatient=TMP_PATIENT_ID):
    dossier =dossiers_patients[me['id']][idPatient]
    return {'loaded_files' : list(map(lambda x: x.split("_")[1].replace(".nii", ""), os.listdir(dossier.name))),'res_status':'success'}
    

async def create_file_t1(file: UploadFile, me=auth.User,idPatient=TMP_PATIENT_ID):
    return addFile(file,"t1",me,idPatient)

async def create_file_t2(file: UploadFile, me=auth.User,idPatient=TMP_PATIENT_ID):
    return addFile(file,"t2",me,idPatient)

async def create_file_t1ce(file: UploadFile, me=auth.User,idPatient=TMP_PATIENT_ID):
    return addFile(file,"t1ce",me,idPatient)

async def create_file_flair(file: UploadFile, me=auth.User,idPatient=TMP_PATIENT_ID):
    return addFile(file,"flair",me,idPatient)


def filenames(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


async def get_analyse(me=auth.User,patientId=TMP_PATIENT_ID):
    # l'analyse a seulement lieu si tous les fichiers sont chargés
    patient_folder = dossiers_patients[me['id']][patientId]
    current_load = loadedfiles(me,patientId)['loaded_files']
    if all(filetype in current_load for filetype in ['t1','t1ce','t2','flair']):
        seg_file_path = await predict.predictsById(patient_folder.name,case=patientId) 
        return FileResponse(seg_file_path, media_type="application/gzip", filename="estimation_seg.nii")
    return {'res_status':'error','detail':'You need to upload the 4 files in order to process the segmentation.'}



#############################
#     GESTION DE COMPTE     #
#############################

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await auth.login_for_access_token(form_data)
    if res['res_status']=='success':
        me = await auth.get_current_user(res['access_token'])
        #eraseAllDossiersPatientDoctor(me['id'])
        if not doctorExists(me['id']): dossiers_patients[me['id']] = {TMP_PATIENT_ID : tempfile.TemporaryDirectory()}
    return res

async def logout(me=Depends(auth.get_current_user)):
    eraseAllDossiersPatientDoctor(me['id'])
    if me['id'] not in dossiers_patients: return {'res_status':'success'}
    else : return {'res_status':'error'}
    

async def whoami(me=Depends(auth.get_current_user)):
    return me

def doctorExists(id:int):
    return id in dossiers_patients

def eraseAllDossiersPatientDoctor(iddoctor:int):
    if iddoctor in dossiers_patients:
        for iddossier in dossiers_patients[iddoctor]:
            # erasing folder and its contents
            dossiers_patients[iddoctor][iddossier].cleanup()
        # removing doctor's id from the dossiers_patients dictionary
        del dossiers_patients[iddoctor]