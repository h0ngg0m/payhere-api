from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequestException(CustomException):  # 400
    code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class UnauthorizedException(CustomException):  # 401
    code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class ForbiddenException(CustomException):  # 403
    code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class NotFoundException(CustomException):  # 404
    code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ConflictException(CustomException):  # 409
    code = HTTPStatus.CONFLICT
    message = HTTPStatus.CONFLICT.description
