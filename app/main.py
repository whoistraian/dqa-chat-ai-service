import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from utils.engine import engine

from models.user import User
from models.session import Session as UserSession
from models.thread import Thread
from models.message import Message

from routers.auth import AuthRouter
from routers.me import MeRouter

from services.user import UserService
from services.session import SessionService
from services.auth import AuthService

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_service = UserService()
session_service = SessionService()
auth_service = AuthService(user_service, session_service)

api_router = APIRouter(prefix="/api")
api_router.include_router(AuthRouter(auth_service).router)
api_router.include_router(MeRouter().router)

app.include_router(api_router)

if __name__ == "main":
    SQLModel.metadata.create_all(engine)
