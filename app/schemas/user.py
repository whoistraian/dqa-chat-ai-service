import typing as t
from sqlmodel import SQLModel
from models.user import User


class UserResponseSchema(SQLModel):
    id: int
    email: str
    password: str

    @staticmethod
    def from_user(user: User):
        return UserResponseSchema(
            id=user.id,
            email=user.email,
            password=user.password
        )


class UserGetRequestSchema(SQLModel):
    id: t.Optional[int]
    email: t.Optional[str]
