from typing import List

from fastapi import FastAPI, File, UploadFile

from fastapi.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from fastapi.responses import FileResponse

import os

app = FastAPI()

fichiers_locaux = {}

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

async def write_file(file:UploadFile= File(...)):
    file_path = os.path.join(os.getcwd(), file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        return {"filename": file.filename}
     
@app.get("/")
async def root():
    return {"message": "Hello World"}

def addFile(file : UploadFile, filetype):
   fichiers_locaux[filetype]=file
   return loadedfiles()

@app.get("/files/cancel")
def cancelfiles():
    fichiers_locaux.clear()
    return fichiers_locaux

@app.get("/files")
def loadedfiles():
    nomsfichierslocaux = {}
    for key in fichiers_locaux.keys():
        nomsfichierslocaux[key] = fichiers_locaux[key].filename
    return  nomsfichierslocaux

@app.post("/files/t1")
async def create_file_t1(file:UploadFile):
    return  addFile(file,"t1")

@app.post("/files/t2")
async def create_file_t2(file:UploadFile):
    #assert fichier_bon(file)
    return  addFile(file,"t2")

@app.post("/files/t1ce")
async def create_file_t1ce(file:UploadFile):
    return  addFile(file,"t1ce")

@app.post("/files/flair")
async def create_file_flair(file:UploadFile):
    #assert fichier_bon(file)
    return  addFile(file,"flair")


def fichier_bon(file: UploadFile):
    return Path(file).suffix=='t1.nii.gz' or os.path.splitext(file)[1]=='t2.nii.gz' or os.path.splitext(file)[1]=='t1ce.nii.gz' or os.path.splitext(file)[1]=='flair.nii.gz'

def filenames(files : List[UploadFile]):
    return {"filenames": [file.filename for file in files]}

def sendFilesToCalculatingMachine(files: List[UploadFile]):
    #TODO
    return fichiers_locaux['t1']

@app.get("/analyse",responses={200:{
    "content":{"application/gzip"}
    }})
async def get_analyse():
    return FileResponse("brats_seg.nii.gz",media_type="application/gzip",filename="estimation_seg.nii.gz")