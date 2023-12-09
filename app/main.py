from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exception import CustomException

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)


@app.exception_handler(CustomException)
async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder(
            {"meta": {"code": exc.code, "message": exc.message}, "data": None}
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "meta": {
                    "code": HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "올바르지 않은 입력값입니다.",
                },
                "data": None,
            }
        ),
    )
