from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends

from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from fastapi.responses import FileResponse

from pydantic import BaseModel


from datetime import datetime, timedelta
from typing import Union

from fastapi import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import os

app = FastAPI()

################################
#  Fonctionnalités principales #
################################

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



#############################
#     Authentification      #
#############################

## Détails pour la création du token
# Exécuter la ligne de commande suivante pour obtenir une clé secrète
# openssl rand -hex 32q
SECRET_KEY = "d520e683e9d5c4c47818f83d44a0112117e02bd6c2ec28f2120c48aa6b6efeae"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$XpffqqZIaTEERJL19DLq1.KbganP7S4s9pBRN77fmDAUKZ77iYlCy",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

#print(pwd_context.hash("bonjour"))