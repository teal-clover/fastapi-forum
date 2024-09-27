class EmailTakenException(Exception):
    pass


class CredentialsException(Exception):
    pass


class InactiveUserException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class PostNotFoundException(Exception):
    pass


class CommentNotFoundException(Exception):
    pass


class IncorectLoginInfoException(Exception):
    pass


class InternalServerException(Exception):
    pass
