import random
import string
import typing as t
from sqlmodel import Session, select
from models.user import User
from models.session import Session as UserSession
from schemas.me import MeResponseSchema
from utils.engine import engine


class SessionService:
    def __generate_token(self,
                         size=6,
                         chars=string.ascii_uppercase +
                         string.digits +
                         string.ascii_lowercase +
                         string.punctuation
                         ) -> str:
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    def get_session_by_token(self, token: str) -> t.Optional[UserSession]:
        with Session(engine) as session:
            statement = select(UserSession).where(UserSession.token == token)
            result = session.exec(statement).one_or_none()

            return result

    def get_user_by_token(self, token: str) -> t.Tuple[UserSession, User]:
        with Session(engine) as session:
            statement = select(UserSession, User).where(
                UserSession.token == token).join(User)
            result = session.exec(statement).one()

            return result

    def create_session(self, user_id: int) -> t.Tuple[UserSession, User]:
        session_token: str = self.__generate_token(size=32)

        while self.get_session_by_token(session_token):
            session_token = self.__generate_token(size=32)

        user_session = UserSession(
            user_id=user_id,
            token=session_token
        )

        with Session(engine) as session:
            session.add(user_session)
            session.commit()

            session.refresh(user_session)

        return self.get_user_by_token(user_session.token)
