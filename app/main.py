import os
from dotenv import load_dotenv
from fastapi import FastAPI
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

user_service = UserService()
session_service = SessionService()
auth_service = AuthService(user_service, session_service)

app.include_router(AuthRouter(auth_service).router)
app.include_router(MeRouter().router)


if __name__ == "main":
    SQLModel.metadata.create_all(engine)
