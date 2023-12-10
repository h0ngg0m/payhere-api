from sqlalchemy.orm import Mapped

from app.core.db.orm import Base, mapped_int_pk
from app.schema.user import UserCreate


class User(Base):
    __tablename__ = "user"

    id: Mapped[mapped_int_pk]
    tel: Mapped[str]
    password: Mapped[str]
    logout_flag: Mapped[bool]

    @staticmethod
    def new(data: UserCreate) -> "User":
        return User(**data.dict(exclude={"id"}))

    def login(self) -> None:
        self.logout_flag = False

    def logout(self) -> None:
        self.logout_flag = True
