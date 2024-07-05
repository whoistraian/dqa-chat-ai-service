import typing as t
from sqlmodel import SQLModel, Field


class Thread(SQLModel, table=True):
    id: t.Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(foreign_key="user.id")
