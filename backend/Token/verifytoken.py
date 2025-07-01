from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

Token = os.getenv('TOKEN')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify(token: str):
    try:
        payload = jwt.decode(token, Token, algorithms='HS256')
        userId = payload.get('id')
        email = payload.get('email')
        if userId is None or email is None:
            return {"message": "Invalid Token"}
        return {"id": userId, "email": email}
    except JWTError:
        return None
