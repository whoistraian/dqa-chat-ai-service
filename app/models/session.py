import typing as t
from sqlmodel import SQLModel, Field


class Session(SQLModel, table=True):
    id: t.Optional[int] = Field(
        default=None,
        primary_key=True
    )
    token: str = Field(unique=True)

    user_id: int = Field(foreign_key="user.id")
