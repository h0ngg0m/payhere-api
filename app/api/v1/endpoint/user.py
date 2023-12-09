from fastapi import APIRouter

from app.api.depends import SessionDepends
from app.crud import crud_user
from app.schema.base import CommonResponse
from app.schema.user import UserCreate, UserResponse

router = APIRouter()


@router.post("", response_model=CommonResponse[UserResponse])
def create_user(db: SessionDepends, data: UserCreate):
    return CommonResponse(data=crud_user.create(db=db, data=data))
