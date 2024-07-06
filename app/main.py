from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel
from langserve import add_routes

from models.user import User
from models.session import Session as UserSession

from routers.auth import AuthRouter
from routers.me import MeRouter

from services.user import UserService
from services.session import SessionService
from services.auth import AuthService
from services.chat import ChatService

from utils.engine import engine


load_dotenv()

app = FastAPI()

user_service = UserService()
session_service = SessionService()
auth_service = AuthService(user_service, session_service)

app.include_router(AuthRouter(auth_service).router)
app.include_router(MeRouter().router)

add_routes(app,
           ChatService().get_rag_chain(),
           enable_feedback_endpoint=True,
           )

if __name__ == "main":
    SQLModel.metadata.create_all(engine)
