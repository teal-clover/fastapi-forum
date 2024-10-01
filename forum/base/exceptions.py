from typing import Any


class BaseException(Exception):
    message = "Unexpected error happened."

    def __init__(self, message: Any = None, *args: object) -> None:
        message = message or self.message
        super().__init__(message, *args)


class EmailTakenException(BaseException):
    message = "The following email has been taken."


class CredentialsException(BaseException):
    message = "Wrong credentials."


class InactiveUserException(BaseException):
    message = "User is not active."


class UserNotFoundException(BaseException):
    message = "Cannot find the user."


class PostNotFoundException(BaseException):
    message = "Cannot find the post."


class CommentNotFoundException(BaseException):
    message = "Cannot find the comment."


class IncorectLoginInfoException(BaseException):
    message = "Wrong login info."


class InternalServerException(BaseException):
    message = "Internal server problems."
