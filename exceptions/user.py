class InvalidEmailError(Exception):
    pass


class PasswordsMatchError(Exception):
    pass


class EmailExistsError(Exception):
    pass


class UserDoesntExistError(Exception):
    pass
