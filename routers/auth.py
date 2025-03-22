from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "password": hashed_password}
    
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    db_user = fake_users_db.get(user.username)
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}
