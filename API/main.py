from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    for file in files:
        assert file.endswith("flair.nii")
        assert file.endswith("t1.nii")
        assert file.endswith("t2.nii")
        assert file.endswith("t1ce.nii")
    return {"filenames": [file.filename for file in files]}

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


#@app.post("/uploadfile/")
#async def create_upload_file(file: UploadFile):
    # file_path = os.path.join(os.getcwd(), file.filename)
    # with open(file_path, "wb") as f:
    #     f.write(await file.read())
    #return {"filename": file.filename}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, file0: UploadFile, file1: UploadFile, file2: UploadFile):
    assert file.endswith("flair.nii")
    assert file0.endswith("t1.nii")
    assert file1.endswith("t2.nii")
    assert file2.endswith("t1ce.nii")
    # file_path = os.path.join(os.getcwd(), file.filename)
    # with open(file_path, "wb") as f:
    #     f.write(await file.read())
    return {"filename": file.filename}


#def lire_fichier(fichier1, fichier2, fichier3, fichier4):
#    try:
#       with open("C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_seg_new.nii", 'r') as f:
#            contenu = f.read()
#            return contenu
#    except FileNotFoundError:
#        print(f"Le fichier est introuvable.")

#lire_fichier("C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_flair.nii","C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_t1.nii","C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_t2.nii","C:\\Users\\utilisateur\\Documents\\ESIR2\\S8\\PROJ-SI-S8\\brain-tumor\\exemples\\Sample_BRATZ\\BraTS2021_01572\\BraTS2021_01572_flair.nii")
