import typing as t
from sqlmodel import SQLModel
from models.user import User
from models.session import Session as UserSession


class AuthRequestSchema(SQLModel):
    email: str
    password: str


class AuthResponseSchema(SQLModel):
    id: int
    token: t.Optional[str]

    @staticmethod
    def from_user(user: User):
        return AuthResponseSchema(
            id=user.id,
            token=None
        )

    @staticmethod
    def from_user_session(response: t.Tuple[UserSession, User]):
        user_session, user = response

        return AuthResponseSchema(
            id=user.id,
            token=user_session.token
        )
