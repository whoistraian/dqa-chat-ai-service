import bcrypt
from services.user import UserService
from schemas.auth import AuthRequestSchema, AuthResponseSchema
from schemas.user import UserGetRequestSchema
from models.user import User
from services.session import SessionService
from fastapi import HTTPException


class AuthService:
    def __init__(self, user_service: UserService, session_service: SessionService):
        self.user_service = user_service
        self.session_service = session_service

    def register(self, auth_request: AuthRequestSchema) -> AuthResponseSchema:
        my_user = User(
            email=auth_request.email,
            password=auth_request.password
        )

        result = self.user_service.create_user(my_user)

        return AuthResponseSchema.from_user(result)

    def login(self, auth_request: AuthRequestSchema) -> AuthResponseSchema:
        my_user = self.user_service.get_user(
            UserGetRequestSchema(id=None, email=auth_request.email)
        )

        if not bcrypt.checkpw(auth_request.password.encode(), my_user.password.encode()):
            #! TODO: Add global exception handler
            raise HTTPException(status_code=401, detail="Invalid credentials")

        result = self.session_service.create_session(my_user.id)

        return AuthResponseSchema.from_user_session(result)
