from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from routers import countdown, notifications, analytics, events, auth  # Include auth.py
import jwt

app = FastAPI(title="Event Countdown and Planner API")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


app.include_router(auth.router, prefix="/auth")
app.include_router(countdown.router, dependencies=[Depends(get_current_user)])
app.include_router(notifications.router, dependencies=[Depends(get_current_user)])
app.include_router(analytics.router, dependencies=[Depends(get_current_user)])
app.include_router(events.router, dependencies=[Depends(get_current_user)])

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Countdown API!"}
