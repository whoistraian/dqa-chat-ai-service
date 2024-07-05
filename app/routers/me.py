import typing as t
from fastapi import APIRouter, Depends
from schemas.me import MeResponseSchema
from utils.get_current_authenticated_user import get_current_authenticated_user


class MeRouter:
    def __init__(self):
        self.router = APIRouter(
            prefix="/me", tags=["me"]
        )

        self.router.add_api_route("", self.get_me, methods=["GET"])

    def get_me(self, current_authenticated_user: t.Annotated[MeResponseSchema, Depends(get_current_authenticated_user)]) -> MeResponseSchema:
        return current_authenticated_user
