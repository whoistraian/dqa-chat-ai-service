import typing as t
from fastapi import Cookie, HTTPException
from schemas.me import MeResponseSchema
from utils.engine import engine
from services.session import SessionService


def get_current_authenticated_user(token: t.Annotated[t.Optional[str], Cookie()]) -> MeResponseSchema:
    session_service = SessionService()

    if not token or not session_service.get_session_by_token(token):
        return HTTPException(status_code=401, detail="Not authenticated")

    _, user = session_service.get_user_by_token(token)
    return MeResponseSchema.from_user(user)
