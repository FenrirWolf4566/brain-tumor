import json
from typing import List

from fastapi import FastAPI, File, Request, UploadFile, Depends

from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from fastapi.responses import FileResponse

from fastapi.security import OAuth2PasswordRequestForm

import os

from variables import TMP_PATIENT_ID
from constants import TOKEN_URL

import auth

import predict

import os
import gzip
import io
import tempfile

# uvicorn main:app --reload

app = FastAPI()

################################
#  Fonctionnalités principales #
################################

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


dossiers_patients = {} #dictionnaire contenant les dossiers temporaires de chaque docteur


def write_file(file_path, file_name,file: UploadFile = File(...)):
    Path(file_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(file_path,file_name)
    print("Upload File saved :"+file_path)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        return {"filename": file_name}
    


def write_niftii_file(file_path, file_name, file: UploadFile = File(...)):
    # Check if file is gzipped NIfTI (.nii.gz)
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

    # Check if file is NIfTI (.nii) or gzipped NIfTI (.nii.gz)
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


@app.get("/")
async def root():
    return {"message": "Hello World"}

def addFile(file : UploadFile, filetype : str,user:auth.User,idPatient=TMP_PATIENT_ID):
   if user['res_status']=='success':
        dossier_patient =dossiers_patients[user['id']][idPatient]
        res =write_niftii_file(dossier_patient.name,idPatient+f"_{filetype}.nii",file)
        if("res_status" in res and res['res_status']=='error'):  return res
        return loadedfiles(user)
   return user

@app.get("/files/cancel")
def cancelfiles(me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if me['res_status'] == 'success':
        dossier = dossiers_patients[me['id']][idPatient]
        dossier.cleanup()
        dossiers_patients[me['id']][idPatient] =tempfile.TemporaryDirectory()
        return loadedfiles(me,idPatient)
    return me

@app.get("/files")
def loadedfiles(me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if me['res_status'] == 'success':
        dossier =dossiers_patients[me['id']][idPatient]
        return {'loaded_files' : list(map(lambda x: x.split("_")[1].replace(".nii", ""), os.listdir(dossier.name)))}
    return me


@app.post("/files/t1")
async def create_file_t1(file: UploadFile, me=Depends(auth.get_current_user)):
    if(me['res_status']=='success'):
        return addFile(file,"t1",me)
    return me

@app.post("/files/t2")
async def create_file_t2(file: UploadFile, me=Depends(auth.get_current_user)):
    if me['res_status'] == 'success': 
        return addFile(file, "t2",me)
    else : return me

@app.post("/files/t1ce")
async def create_file_t1ce(file: UploadFile, me=Depends(auth.get_current_user)):
    if me['res_status'] == 'success':
        return addFile(file, "t1ce",me)
    else : return me

@app.post("/files/flair")
async def create_file_flair(file: UploadFile, me=Depends(auth.get_current_user)):
    if me['res_status'] == 'success': 
        return addFile(file, "flair",me)
    else : return me

def fichier_bon(file: UploadFile):
    return Path(file).suffix == 't1.nii.gz' or os.path.splitext(file)[1] == 't2.nii.gz' or os.path.splitext(file)[1] == 't1ce.nii.gz' or os.path.splitext(file)[1] == 'flair.nii.gz'


def filenames(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/analyse", responses={200: {"content": {"application/gzip"}}})
async def get_analyse(me=Depends(auth.get_current_user),patientId=TMP_PATIENT_ID):
    if me['res_status'] == 'success':
        patient_folder = dossiers_patients[me['id']][patientId]
        seg_file_path = await predict.predictsById(patient_folder.name,case=patientId) 
        return FileResponse(seg_file_path, media_type="application/gzip", filename="estimation_seg.nii")
    return me

#############################
#     GESTION DE COMPTE     #
#############################

@app.post(TOKEN_URL)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await auth.login_for_access_token(form_data)
    if res['res_status']=='success':
        me = await auth.get_current_user(res['access_token'])
        #eraseAllDossiersPatientDoctor(me['id'])
        if not doctorExists(me['id']): dossiers_patients[me['id']] = {TMP_PATIENT_ID : tempfile.TemporaryDirectory()}
    return res


@app.get("/account/me/")
async def whoami(me=Depends(auth.get_current_user)):
    return me

def doctorExists(id:int):
    return id in dossiers_patients

def eraseAllDossiersPatientDoctor(iddoctor:int):
    if iddoctor in dossiers_patients:
        for iddossier in dossiers_patients[iddoctor]:
            dossiers_patients[iddoctor][iddossier].cleanup()