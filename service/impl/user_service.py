import re
from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import Depends

from constants.constants import Constants
from database.database import MainSession
from database.models import User, Role
from exceptions.user import InvalidEmailError, PasswordsMatchError, EmailExistsError, UserDoesntExistError
from exceptions.auth import InvalidPasswordError
from schemas.auth import TokenResponse
from schemas.role import RoleResponse
from schemas.user import UserRegistrationRequest, UserResponse, UserLoginRequest
from service.impl.auth_service import AuthService
from service.meta.user_service_meta import UserServiceMeta

# Main app database instance
db = MainSession()

# Load environment variables
load_dotenv()

# Auth service instance
auth_service = AuthService()

# Constants instance
constants = Constants()


class UserService(UserServiceMeta):
    """
        User service class

        Implements UserServiceMeta class methods.
        Used to registrate and login users in application.

    """
    def validate_email(self, email: str) -> bool:
        """
        Validate given email.

        Parameters:
            email (str): Email to validate

        Returns:
            bool: A boolean indicating if the email is valid.
        """
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    def validate_password(self, password: str, confirm_password: str) -> bool:
        """
        Validate if password and it's confirmation matches.

        Parameters:
            password (str): Entered password
            confirm_password (str): Confirmed password

        Returns:
            bool: A boolean indicating if passwords match.
        """
        return password == confirm_password

    def register_user(
            self,
            user: UserRegistrationRequest
    ) -> TokenResponse:
        """
        Register a new user in application.

        Parameters:
            user (UserRegistrationRequest): User registration request

        Returns:
            TokenResponse: A jwt token containing the user information.

        Raises:
            InvalidEmailError: Raise if the provided email is invalid
            PasswordsMatchError: Raise if the provided password is invalid
            EmailExistsError: Raise if the provided email is already registered
        """
        if not self.validate_email(user.email):
            raise InvalidEmailError

        if not self.validate_password(user.password, user.confirm_password):
            raise PasswordsMatchError

        if db.query(User).filter(User.email == user.email).first() is not None:
            raise EmailExistsError

        user_role = db.query(Role).filter(Role.name == "user").first()

        new_user = User(
            email=user.email,
            name=user.name,
            password=auth_service.hash_password(user.password),
            role=user_role
        )
        db.add(new_user)
        db.commit()

        new_user_role = RoleResponse(
            id=new_user.role.id,
            name=new_user.role.name
        )

        user_registration_response = UserResponse(
            email=new_user.email,
            name=new_user.name,
            public_id=new_user.public_id,
            role=new_user_role,
        )

        token_response = TokenResponse(
            token=auth_service.tokenize(user_registration_response.model_dump())
        )

        return token_response

    def login_user(
            self,
            user: UserLoginRequest
    ) -> TokenResponse:
        """
        Login a user in application.

        Parameters:
            user (UserRegistrationRequest): User registration request

        Returns:
            TokenResponse: A jwt token containing the user information.

        Raises:
            InvalidEmailError: Raise if the provided email is invalid
            UserDoesntExistError: Raise if user with provided email doesn't exist
            InvalidPasswordError: Raise if the provided password is invalid
        """
        if not self.validate_email(user.email):
            raise InvalidEmailError

        matching_user = db.query(User).filter(User.email == user.email).first()

        if matching_user is None:
            raise UserDoesntExistError

        if not auth_service.verify_password(user.password, matching_user.password):
            raise InvalidPasswordError

        matching_user_role = RoleResponse(
            id=matching_user.role.id,
            name=matching_user.role.name
        )

        user_logging_response = UserResponse(
            email=matching_user.email,
            name=matching_user.name,
            public_id=matching_user.public_id,
            role=matching_user_role,
        )

        token_response = TokenResponse(
            token=auth_service.tokenize(user_logging_response.model_dump())
        )

        return token_response

