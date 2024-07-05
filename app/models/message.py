import typing as t
from sqlmodel import SQLModel, Field


class Message(SQLModel, table=True):
    id: t.Optional[int] = Field(
        default=None,
        primary_key=True
    )

    thread_id: int = Field(foreign_key="thread.id")
