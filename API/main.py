from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # file_path = os.path.join(os.getcwd(), file.filename)
    # with open(file_path, "wb") as f:
    #     f.write(await file.read())
    return {"filename": file.filename}