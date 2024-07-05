import os
from fastapi import APIRouter, Response
from services.auth import AuthService
from schemas.auth import AuthRequestSchema, AuthResponseSchema


class AuthRouter:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/auth", tags=["auth"])

        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])

    def register(self, auth_request: AuthRequestSchema) -> AuthResponseSchema:
        return self.auth_service.register(auth_request)

    def login(self, auth_request: AuthRequestSchema, response: Response) -> AuthResponseSchema:
        result = self.auth_service.login(auth_request)

        response.set_cookie(
            'token',
            result.token,
            secure=not bool(os.getenv('DEBUG')),
            httponly=True
        )

        return result
