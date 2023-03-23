from base64 import b64encode
from secrets import token_bytes


TOKEN_URL="/account/auth"
SECRET_KEY = b64encode(token_bytes(32)).decode()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30