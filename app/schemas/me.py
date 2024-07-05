from sqlmodel import SQLModel
from models.user import User


class MeResponseSchema(SQLModel):
    id: int
    email: str

    @staticmethod
    def from_user(user: User):
        return MeResponseSchema(
            id=user.id,
            email=user.email
        )
