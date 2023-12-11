from sqlalchemy.orm import Session

from app.core.exception import ConflictException
from app.core.security import get_password_hash, verify_password
from app.model.user import User
from app.schema.user import UserCreate, UserResponse


def get_by_tel(*, db: Session, tel: str) -> User | None:
    return db.query(User).filter_by(tel=tel).first()


def create(*, db: Session, data: UserCreate) -> UserResponse:
    same_tel_user: User = get_by_tel(db=db, tel=data.tel)

    if same_tel_user:
        raise ConflictException(f"'{data.tel}'는 이미 사용 중인 휴대폰 번호입니다.")

    user: User = User.new(data)
    user.password = get_password_hash(user.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.from_orm(user)


def authenticate(*, db: Session, tel: str, password: str) -> User | None:
    user = get_by_tel(db=db, tel=tel)

    if not user:
        return None

    if not verify_password(plain_password=password, hashed_password=user.password):
        return None

    user.login()
    db.commit()
    return user


def logout(*, db: Session, user: User) -> None:
    user.logout()
    db.commit()
