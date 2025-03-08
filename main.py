from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from routers import countdown, notifications, analytics
from routers import events

app = FastAPI(title="Event Countdown and Planner API")

# Mock token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "valid_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"user": "authenticated_user"}

# Register all routers with authentication
app.include_router(countdown.router, dependencies=[Depends(get_current_user)])
app.include_router(notifications.router, dependencies=[Depends(get_current_user)])
app.include_router(analytics.router, dependencies=[Depends(get_current_user)])
app.include_router(events.router, dependencies=[Depends(get_current_user)])

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Countdown API!"}
