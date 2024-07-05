import bcrypt
import typing as t
from fastapi import HTTPException
from models.user import User
from schemas.user import UserResponseSchema, UserGetRequestSchema
from sqlmodel import Session, select
from utils.engine import engine


class UserService:
    def __get_user_by_id(self, id: int) -> t.Optional[UserResponseSchema]:
        with Session(engine) as session:
            statement = select(User).where(User.id == id)
            result = session.exec(statement).one_or_none()

            if not result:
                return None

            return UserResponseSchema.from_user(result)

    def __get_user_by_email(self, email: str) -> t.Optional[UserResponseSchema]:
        with Session(engine) as session:
            statement = select(User).where(User.email == email)
            result = session.exec(statement).one_or_none()

            if not result:
                return None

            return UserResponseSchema.from_user(result)

    def get_user(self, user_request: UserGetRequestSchema, safe: bool = False) -> UserResponseSchema:
        my_user = None

        if user_request.id:
            my_user = self.__get_user_by_id(user_request.id)
        elif user_request.email:
            my_user = self.__get_user_by_email(user_request.email)

        if not my_user and not safe:
            raise HTTPException(status_code=404, detail="User not found.")

        if not my_user:
            return None

        return UserResponseSchema.from_user(my_user)

    def create_user(self, user: User) -> UserResponseSchema:
        if self.get_user(user_request=UserGetRequestSchema(id=None, email=user.email), safe=True):
            raise HTTPException(status_code=400, detail="User already exists.")

        #! TODO: Add password validation

        user.password = bcrypt.hashpw(
            user.password.encode(),
            bcrypt.gensalt()
        ).decode()

        with Session(engine) as session:
            session.add(user)
            session.commit()

            session.refresh(user)

            return UserResponseSchema.from_user(user)
