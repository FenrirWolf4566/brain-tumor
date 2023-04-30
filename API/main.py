from fastapi import FastAPI, UploadFile, Depends

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm

from variables import TMP_PATIENT_ID
from constants import TOKEN_URL

import auth

import services

# uvicorn main:app --reload

# Ce fichier correspond à la partie controller

app = FastAPI()

################################
#  Fonctionnalités principales #
################################

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:80",
    "http://0.0.0.0:80",
    "http://0.0.0.0:3000",
    "https://visualgliome.bdezordo.com/",
    "https://api.bdezordo.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/files/cancel")
def cancelfiles(me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if me['res_status'] == 'success':
        return services.cancelfiles(me,idPatient)
    return me

@app.get("/files",description="Get names of the loaded files concerning a patient")
def loadedfiles(me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if me['res_status'] == 'success':
        return services.loadedfiles(me,idPatient)
    return me


@app.post("/files/t1")
async def upload_file_t1(file: UploadFile, me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if(me['res_status']=='success'):
        return await services.create_file_t1(file,me,idPatient)
    return me

@app.post("/files/t2")
async def upload_file_t2(file: UploadFile, me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if(me['res_status']=='success'):
        return await services.create_file_t2(file,me,idPatient)
    return me

@app.post("/files/t1ce")
async def upload_file_t1ce(file: UploadFile, me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if(me['res_status']=='success'):
        return await services.create_file_t1ce(file,me,idPatient)
    return me

@app.post("/files/flair")
async def upload_file_flair(file: UploadFile, me=Depends(auth.get_current_user),idPatient=TMP_PATIENT_ID):
    if(me['res_status']=='success'):
        return await services.create_file_flair(file,me,idPatient)
    return me

@app.get("/analyse", responses={200: {"content": {"application/gzip"}}})
async def get_analyse(me=Depends(auth.get_current_user),patientId=TMP_PATIENT_ID):
    if me['res_status'] == 'success':
        return await services.get_analyse(me,patientId)
    return me


#############################
#     GESTION DE COMPTE     #
#############################

@app.post(TOKEN_URL)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await services.login(form_data)

@app.get("/account/disconnect",description="A success means that all the data about the user is deleted")
async def  logout(me=Depends(auth.get_current_user)):
    if me['res_status'] == 'success':
        return await services.logout(me)
    return me

@app.get("/account/me/")
async def whoami(me=Depends(auth.get_current_user)):
    return await services.whoami(me)