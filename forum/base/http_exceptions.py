from typing import Any

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    detail = "Unexpected error happened."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self, detail: Any = None, status_code: Any = None, *args: object
    ) -> None:
        detail = detail or self.detail
        status_code = status_code or self.status_code
        super().__init__(status_code, detail, *args)


class EmailTakenHTTPException(BaseHTTPException):
    detail = "The following email has been taken."
    status_code = status.HTTP_409_CONFLICT


class CredentialsHTTPException(BaseHTTPException):
    detail = "Wrong credentials."
    status_code = status.HTTP_403_FORBIDDEN


class InactiveUserHTTPException(BaseHTTPException):
    detail = "User is not active."
    status_code = status.HTTP_403_FORBIDDEN


class UserNotFoundHTTPException(BaseHTTPException):
    detail = "Cannot find the user."
    status_code = status.HTTP_404_NOT_FOUND


class PostNotFoundHTTPException(BaseHTTPException):
    detail = "Cannot find the post."
    status_code = status.HTTP_404_NOT_FOUND


class CommentNotFoundHTTPException(BaseHTTPException):
    detail = "Cannot find the comment."
    status_code = status.HTTP_404_NOT_FOUND


class IncorectLoginInfoHTTPException(BaseHTTPException):
    detail = "Wrong login info."
    status_code = status.HTTP_403_FORBIDDEN


class InternalServerHTTPException(BaseHTTPException):
    detail = "Internal server problems."
