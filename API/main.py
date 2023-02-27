from typing import List

from fastapi import FastAPI, File, UploadFile

from fastapi.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()

fichiers_locaux = []

@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

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

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
     file_path = os.path.join(os.getcwd(), file.filename)
     with open(file_path, "wb") as f:
         f.write(await file.read())
         return {"filename": file.filename}

def fichier_bon(file: UploadFile):
    return True #or file.endswith("t1.nii") or file.endswith("t2.nii") or file.endswith("t1ce.nii")

@app.post("/uploadfiles/")
async def create_upload_file(files: List[UploadFile]):
    fichiers_bons = []
    fichiers_mauvais = []
    for file in files:
        if(fichier_bon(file)):
            fichiers_bons.append(file)
        else:
            fichiers_mauvais.append(file)
    fichiers_locaux = fichiers_bons
    return {"cache_files":str(fichiers_locaux), "validated_files":str(fichiers_bons), "wrong_files":str(fichiers_mauvais)}

def filenames(files : List[UploadFile]):
    return {"filenames": [file.filename for file in files]}

def sendFilesToCalculatingMachine(files: List[UploadFile]):
    #TODO
    return

@app.post("/analyse/")
async def analysis():
    res = await sendFilesToCalculatingMachine(fichiers_locaux)
    return res

#def lire_fichier(fichier1, fichier2, fichier3, fichier4):
#    try:
#       with open("C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_seg_new.nii", 'r') as f:
#            contenu = f.read()
#            return contenu
#    except FileNotFoundError:
#        print(f"Le fichier est introuvable.")

#lire_fichier("C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_flair.nii","C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_t1.nii","C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_t2.nii","C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_flair.nii")
