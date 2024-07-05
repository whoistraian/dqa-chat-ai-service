import typing as t
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: t.Optional[int] = Field(
        default=None,
        primary_key=True
    )

    email: str = Field(unique=True)
    password: str
