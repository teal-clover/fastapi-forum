from fastapi import HTTPException


class EmailTakenException(HTTPException):
    pass


class CredentialsException(HTTPException):
    pass


class InactiveUserException(HTTPException):
    pass


class UserNotFoundException(HTTPException):
    pass


class IncorectLoginInfoException(HTTPException):
    pass
