from fastapi import FastAPI
from app.routes import countdown, notifications, analytics, non_crud_endpoints

app = FastAPI()

# Register routers
app.include_router(countdown.router)
app.include_router(notifications.router)
app.include_router(analytics.router)
app.include_router(non_crud_endpoints.router)  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
