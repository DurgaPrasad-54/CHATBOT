from fastapi import FastAPI, Depends, HTTPException, status
from pymongo import MongoClient
from pydantic import BaseModel
import bcrypt
from jose import jwt,JWTError
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from Token.verifytoken import verify
from Models.model import User,UserLog
load_dotenv()

MongoUrl = os.getenv('MONGOURL')
Token=os.getenv('TOKEN')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

Client = MongoClient(MongoUrl)
db = Client['Chatbot']
Model = db['users']
   
@app.post("/register")

def Register(user:User):
    existing = Model.find_one({"email":user.email})
    if(existing):
        return{"message":"user already exist please login"}
    hashed = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt())
    userdata={
        'username':user.username,
        'email':user.email,
        'password':hashed
    }
    users =  Model.insert_one(userdata)
    if(users):
        return {"message":"User Created"}
    else:
        return {"message":"User creation failed"}
    
@app.post("/login")
def Login(user: UserLog):
    users = Model.find_one({'email':user.email})
    if not users:
        return {"message":"user not exist please register"}
    if(bcrypt.checkpw(user.password.encode('utf-8'),users['password'])):
        token = jwt.encode({"id":str(users['_id']),"email":users['email']},Token,algorithm="HS256")
        return {"message":"login successfully","Token":token}
    else:
        return {"message":"incorrect password"}

@app.get('/chat')
def chat(token:str = Depends(oauth2_scheme)):
    user = verify(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message":"Welcome"}
    
    
    