class ServiceException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__()


class UserAlreadyExists(Exception):
    ...


class UserNotFound(Exception):
    ...
