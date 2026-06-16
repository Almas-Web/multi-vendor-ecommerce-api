from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from apis.base import api_router

from db.models.user import User
from repositories.user import UserRepository

import os

from utils.const import UPLOAD_FOLDER


# CREATE APP
def start_application():

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )

    return app


app = start_application()


# CORS SETUP

origins = [
    "http://localhost:3000",  # Frontend during development
    "https://your-frontend-domain.com",  # Production frontend
    "*",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"], 
)


# INCLUDE ROUTES
app.include_router(api_router)


# STATIC FILES SETUP
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=UPLOAD_FOLDER),
    name="static"
)


# HOME ROUTE
@app.get("/")
def home():
    return {"msg": "Hello World"}


# PROTECTED ROUTE
@app.get("/protected")
async def protected_route(
    current_user: User = Depends(UserRepository.get_current_user)
):
    return {
        "message": f"Hello {current_user.email}, you are authorized!"
    }