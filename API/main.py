from typing import List

from fastapi import FastAPI, File, UploadFile

from fastapi.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

import os

app = FastAPI()

fichiers_locaux = []

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/files/t1")
async def create_file_t1(file: bytes = File()):
    fichiers_locaux.append(file)
    return {"file_size": len(file)}

async def write_file(file: bytes = File()):
     file_path = os.path.join(os.getcwd(), file.filename)
     with open(file_path, "wb") as f:
         f.write(await file.read())
         return {"filename": file.filename}

def fichier_bon(file: UploadFile):
    return Path(file).suffix=='t1.nii.gz' or os.path.splitext(file)[1]=='t2.nii.gz' or os.path.splitext(file)[1]=='t1ce.nii.gz' or os.path.splitext(file)[1]=='flair.nii.gz'

def filenames(files : List[UploadFile]):
    return {"filenames": [file.filename for file in files]}

def sendFilesToCalculatingMachine(files: List[UploadFile]):
    #TODO
    return

@app.post("/analyse/")
async def analysis():
    res = await sendFilesToCalculatingMachine(fichiers_locaux)
    return res
